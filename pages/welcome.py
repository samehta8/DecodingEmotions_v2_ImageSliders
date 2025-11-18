"""
Welcome page - Initial instructions screen.
"""
import streamlit as st
from utils.styling import apply_compact_layout, set_spacing

def show():
    """Display the welcome screen."""
    # Apply compact layout to minimize scrolling
    apply_compact_layout()
    # Optionally adjust spacing (top, bottom, between_elements in rem)
    # set_spacing(top=1, bottom=0.5, between_elements=0.3)

    st.title("⚽ Creativity Rating App")

    st.markdown("""
    ## Welcome!

    This application is designed to collect subjective ratings of soccer actions from video clips.

    ### Instructions:

    1. **Login**: First, you'll indicate whether you've participated before
    2. **Questionnaire**: New users will complete a brief demographic questionnaire
    3. **Rating**: You'll watch video clips and rate various aspects of each action
    4. **Progress**: Your ratings are automatically saved after each video

    ### Important Notes:

    - Please complete ratings in a quiet environment without distractions
    - Your responses will help us understand creativity assessment in soccer
    - All data is anonymized using a generated user ID
    - You can take breaks between videos - your progress is saved

    ---

    **Ready to begin?** Click the button below to proceed.
    """)

    st.markdown("")  # Spacing

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("▶️ Next", use_container_width=True, type="primary"):
            st.session_state.page = 'login'
            st.rerun()
