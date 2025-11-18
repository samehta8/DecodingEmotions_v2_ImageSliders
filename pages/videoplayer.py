"""
Video player page - Main rating interface.
Displays videos with customizable rating scales and optional metadata/pitch visualization.
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
import duckdb
import random
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from utils.config_loader import load_rating_scales
from utils.data_persistence import save_rating, get_rated_videos_for_user
from utils.styling import apply_compact_layout, set_video_height, set_spacing

def display_video_with_mode(video_file_path, playback_mode='loop'):
    """
    Display video with specified playback mode.

    Parameters:
    - video_file_path: Path to the video file
    - playback_mode: 'loop' or 'once'
        - 'loop': Autoplay, loop enabled, controls visible
        - 'once': Autoplay, no loop, no controls (plays once only)
    """
    if not os.path.exists(video_file_path):
        st.error(f"Video file not found: {video_file_path}")
        return

    if playback_mode == 'loop':
        # Loop mode: autoplay with controls and looping
        st.video(video_file_path, autoplay=True, loop=True)

    elif playback_mode == 'once':
        # Once mode: autoplay without controls, no loop, plays once only
        # Read video file and encode as base64
        with open(video_file_path, 'rb') as f:
            video_bytes = f.read()
        video_base64 = base64.b64encode(video_bytes).decode()

        # Create HTML5 video player without controls
        video_html = f"""
        <video
            width="100%"
            autoplay
            muted
            style="max-width: 100%; height: auto;"
            onended="this.pause();"
        >
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <style>
            video::-webkit-media-controls {{
                display: none !important;
            }}
            video::-webkit-media-controls-enclosure {{
                display: none !important;
            }}
        </style>
        """
        components.html(video_html, height=500)

    else:
        # Fallback to default
        st.video(video_file_path)

def show():
    """Display the video player screen."""
    user = st.session_state.user
    config = st.session_state.config

    if not config:
        st.error("Configuration not loaded. Please restart the application.")
        return

    # Initialize video player state
    if 'video_initialized' not in st.session_state:
        initialize_video_player(config)

    # Check if there are videos to rate
    if not st.session_state.get('videos_to_rate'):
        show_completion_message()
        return

    # Load current video
    current_video_index = st.session_state.get('current_video_index', 0)
    videos = st.session_state.videos_to_rate

    if current_video_index >= len(videos):
        show_completion_message()
        return

    current_video = videos[current_video_index]
    action_id = os.path.splitext(current_video)[0]

    # Display the rating interface
    display_rating_interface(action_id, current_video, config)

def initialize_video_player(config):
    """Initialize video player state - load videos, metadata, and rating scales."""
    user = st.session_state.user

    # Load rating scales
    st.session_state.rating_scales = load_rating_scales(config)

    # Track which scales are required
    st.session_state.required_scales = [
        scale.get('title') for scale in st.session_state.rating_scales
        if scale.get('required_to_proceed', True)
    ]

    # Get configuration
    db_path = config['paths']['db_path']
    video_path = config['paths']['video_path']
    min_ratings_per_video = config['settings']['min_ratings_per_video']

    # Get all video files
    try:
        all_videos = [f for f in os.listdir(video_path) if f.lower().endswith('.mp4')]
    except FileNotFoundError:
        st.error(f"Video directory not found: {video_path}")
        all_videos = []

    # Filter out videos already rated by this user
    videos_rated_by_user = get_rated_videos_for_user(user.user_id)
    unrated_videos = [v for v in all_videos if v.replace('.mp4', '') not in videos_rated_by_user]

    # Count total ratings per video and filter out fully-rated videos
    try:
        rated_files = os.listdir('user_ratings')
        rated_ids = [f.split('_')[1].replace('.json', '') for f in rated_files if f.endswith('.json')]
        rating_counts = pd.Series(rated_ids).value_counts()
        videos_fully_rated = rating_counts[rating_counts >= min_ratings_per_video].index.tolist()
        videos_to_rate = [v for v in unrated_videos if v.replace('.mp4', '') not in videos_fully_rated]
    except Exception as e:
        print(f"[WARNING] Error filtering fully-rated videos: {e}")
        videos_to_rate = unrated_videos

    # Shuffle videos
    random.shuffle(videos_to_rate)

    st.session_state.videos_to_rate = videos_to_rate
    st.session_state.current_video_index = 0
    st.session_state.video_path = video_path

    # Load metadata from database
    try:
        conn = duckdb.connect(db_path, read_only=True)

        if videos_to_rate:
            event_id_str = ', '.join(f"'{v.replace('.mp4', '')}'" for v in videos_to_rate)
            query = f"SELECT * FROM events WHERE id IN ({event_id_str})"
            df_metadata = conn.execute(query).fetchdf()
        else:
            df_metadata = pd.DataFrame()

        conn.close()
        st.session_state.metadata = df_metadata
    except Exception as e:
        print(f"[WARNING] Failed to load metadata: {e}")
        st.session_state.metadata = pd.DataFrame()

    st.session_state.video_initialized = True

def display_rating_interface(action_id, video_filename, config):
    """Display the main rating interface with video and scales."""
    # Apply compact layout to minimize scrolling
    apply_compact_layout()

    # Optionally set video height (as percentage of viewport height)
    set_video_height(height_vh=40)  # Video takes 40% of screen height

    # Optionally adjust spacing
    # set_spacing(top=1, bottom=0.5, between_elements=0.3)

    user = st.session_state.user
    video_path = st.session_state.video_path
    metadata = st.session_state.metadata
    rating_scales = st.session_state.rating_scales

    # Display options from config
    display_metadata = config['settings'].get('display_metadata', True)
    display_pitch = config['settings'].get('display_pitch', True)
    video_playback_mode = config['settings'].get('video_playback_mode', 'loop')

    #st.title("⚽ Video Rating")

    # Top metadata bar (if enabled)
    if display_metadata and not metadata.empty:
        row = metadata[metadata['id'] == action_id]
        if not row.empty:
            #st.markdown("### Action Information")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Team", row.team.values[0])
            with col2:
                st.metric("Player", row.player.values[0])
            with col3:
                st.metric("Jersey #", row.jersey_number.values[0])
            with col4:
                st.metric("Type", row.type.values[0])
            with col5:
                if 'bodypart' in row.columns:
                    st.metric("Body Part", row.bodypart.values[0])

    st.markdown("---")

    # Video and pitch visualization area
    if display_pitch and not metadata.empty:
        # Show video and pitch side by side
        col_video, col_pitch = st.columns([55, 45])

        with col_video:
          #  st.markdown("### Video")
            video_file = os.path.join(video_path, video_filename)
            display_video_with_mode(video_file, video_playback_mode)

        with col_pitch:
           # st.markdown("### Pitch Visualization")
            # Generate pitch visualization
            row = metadata[metadata['id'] == action_id]
            if not row.empty:
                try:
                    import mplsoccer
                    pitch = mplsoccer.Pitch(pitch_type="statsbomb", pitch_color="grass")
                    fig, ax = pitch.draw(figsize=(6, 4))

                    fig.patch.set_facecolor('black')
                    fig.patch.set_alpha(1)

                    # Draw arrow
                    start_x = row.start_x.values[0]
                    start_y = row.start_y.values[0]
                    end_x = row.end_x.values[0]
                    end_y = row.end_y.values[0]

                    pitch.arrows(start_x, start_y, end_x, end_y,
                                ax=ax, color="blue", width=2, headwidth=10, headlength=5)
                    ax.plot(start_x, start_y, 'o', color='blue', markersize=10)

                    fig.tight_layout(pad=0)
                    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

                    st.pyplot(fig)
                    plt.close(fig)
                except Exception as e:
                    st.error(f"Failed to generate pitch visualization: {e}")
            else:
                st.info("No metadata available for this video")

    else:
        # Show only video (centered)
        st.markdown("### Video")
        video_file = os.path.join(video_path, video_filename)
        display_video_with_mode(video_file, video_playback_mode)

    # Action not recognized button
    action_not_recognized = st.button(
        "⚠️ Action not recognized", type="primary",
        key=f"not_recognized_{action_id}",
        help="Check this if you cannot identify or rate this action",
        width="stretch"
        )

    st.markdown("---")

    # Rating scales
    #st.markdown("### Rating Scales")
    st.markdown("### Please rate the action on the following dimensions:")

    scale_values = {}

    for scale_config in rating_scales:
        scale_type = scale_config.get('type', 'discrete')
        title = scale_config.get('title', 'Scale')
        label_low = scale_config.get('label_low', '')
        label_high = scale_config.get('label_high', '')
        required = scale_config.get('required_to_proceed', True)

        # Display scale title and labels
        st.markdown(f"**{title}** {'*(required)*' if required and not action_not_recognized else ''}")

        col_low, col_scale, col_high = st.columns([1, 3, 1])

        with col_low:
            st.markdown(f"*{label_low}*")

        with col_scale:
            if scale_type == 'discrete':
                values = scale_config.get('values', [1, 2, 3, 4, 5, 6, 7])
                selected = st.pills(
                    label=title,
                    options=values,
                    #horizontal=True,
                    key=f"scale_{action_id}_{title}",
                    label_visibility="collapsed",
                    width="stretch"
                 #   index=None
                )
                scale_values[title] = selected

            elif scale_type == 'slider':
                slider_min = scale_config.get('slider_min', 0)
                slider_max = scale_config.get('slider_max', 100)
                selected = st.slider(
                    label=title,
                    min_value=float(slider_min),
                    max_value=float(slider_max),
                    value=float(slider_min + slider_max) / 2,
                    key=f"scale_{action_id}_{title}",
                    label_visibility="collapsed"
                )
                scale_values[title] = selected

            elif scale_type == 'text':
                selected = st.text_input(
                    label=title,
                    key=f"scale_{action_id}_{title}",
                    placeholder="Enter your response...",
                    label_visibility="collapsed"
                )
                scale_values[title] = selected if selected else None

        with col_high:
            st.markdown(f"*{label_high}*")

        st.markdown("")  # Spacing

    st.markdown("---")

    # Navigation and submission buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("◀️ Back to Questionnaire", use_container_width=True):
            if st.session_state.get('confirm_back', False):
                st.session_state.page = 'questionnaire'
                st.session_state.user_id_confirmed = False
                st.session_state.video_initialized = False
                st.rerun()
            else:
                st.session_state.confirm_back = True
                st.warning("⚠️ Click again to confirm. Unsaved ratings will be lost.")

    with col3:
        if st.button("Submit Rating ▶️", use_container_width=True, type="primary"):
            # Validate ratings
            if not action_not_recognized:
                # Check that all required scales have values
                required_scales = st.session_state.required_scales
                missing_scales = [
                    title for title in required_scales
                    if scale_values.get(title) is None or scale_values.get(title) == ''
                ]

                if missing_scales:
                    st.error(f"⚠️ Please provide ratings for all required scales: {', '.join(missing_scales)}")
                    st.stop()

            # Save rating
            if save_rating(user.user_id, action_id, scale_values, action_not_recognized):
                st.success("✅ Rating saved successfully!")

                # Move to next video
                st.session_state.current_video_index += 1
                st.session_state.confirm_back = False

                # Clear scale values for next video
                st.rerun()
            else:
                st.error("❌ Failed to save rating. Please try again.")

def show_completion_message():
    """Display message when all videos have been rated."""
    st.title("🎉 All Done!")

    st.success("""
    ### Thank you for your participation!

    You have completed rating all available videos.

    Your responses have been saved and will help us understand creativity assessment in soccer.
    """)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("◀️ Back to Questionnaire", use_container_width=True):
            st.session_state.page = 'questionnaire'
            st.session_state.user_id_confirmed = False
            st.session_state.video_initialized = False
            st.rerun()

    with col3:
        if st.button("Export Data 📊", use_container_width=True, type="primary"):
            try:
                from utils.export_to_csv import export_all_data
                export_all_data()
                st.success("✅ Data exported successfully! Check the 'output' folder.")
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
