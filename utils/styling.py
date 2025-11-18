"""
Styling utilities for customizing page appearance and layout.
"""
import streamlit as st

def apply_compact_layout():
    """
    Apply compact layout CSS to minimize scrolling and fit content to screen.
    This reduces padding, margins, and makes better use of vertical space.
    """
    st.markdown(
        """
        <style>
        /* Reduce top padding */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }

        /* Reduce spacing between elements */
        .stMarkdown {
            margin-bottom: 0.5rem !important;
        }

        /* Compact titles */
        h1 {
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            font-size: 2rem !important;
        }

        h2 {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
            font-size: 1.5rem !important;
        }

        h3 {
            margin-top: 0.3rem !important;
            margin-bottom: 0.3rem !important;
            font-size: 1.2rem !important;
        }

        /* Reduce button padding */
        .stButton button {
            padding: 0.4rem 1rem !important;
        }

        /* Compact form elements */
        .stRadio, .stCheckbox, .stTextInput, .stNumberInput {
            margin-bottom: 0.5rem !important;
        }

        /* Reduce horizontal rule spacing */
        hr {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Compact metrics */
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }

        /* Reduce video container padding */
        [data-testid="stImage"], [data-testid="stVideo"] {
            margin-bottom: 0.5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def set_element_height(height_px=None, height_vh=None):
    """
    Set custom height for an element using viewport units or pixels.

    Parameters:
    - height_px: Height in pixels (e.g., 400)
    - height_vh: Height as viewport percentage (e.g., 50 for 50% of viewport)

    Returns CSS class name that can be applied to elements.

    Example:
        set_element_height(height_vh=40)  # 40% of viewport height
        st.video(video_file)
    """
    if height_vh:
        st.markdown(
            f"""
            <style>
            .custom-height-container {{
                height: {height_vh}vh !important;
                max-height: {height_vh}vh !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    elif height_px:
        st.markdown(
            f"""
            <style>
            .custom-height-container {{
                height: {height_px}px !important;
                max-height: {height_px}px !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def set_video_height(height_vh=None, height_px=None):
    """
    Set custom height for video elements.

    Parameters:
    - height_vh: Height as viewport percentage (e.g., 40 for 40% of screen height)
    - height_px: Height in pixels (e.g., 400)

    Example:
        set_video_height(height_vh=50)  # Video takes 50% of screen height
    """
    if height_vh:
        st.markdown(
            f"""
            <style>
            [data-testid="stVideo"] video {{
                height: {height_vh}vh !important;
                max-height: {height_vh}vh !important;
            }}
            iframe {{
                height: {height_vh}vh !important;
                max-height: {height_vh}vh !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    elif height_px:
        st.markdown(
            f"""
            <style>
            [data-testid="stVideo"] video {{
                height: {height_px}px !important;
                max-height: {height_px}px !important;
            }}
            iframe {{
                height: {height_px}px !important;
                max-height: {height_px}px !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def set_spacing(top=None, bottom=None, between_elements=None):
    """
    Control spacing on the page.

    Parameters:
    - top: Top padding in rem (e.g., 1)
    - bottom: Bottom padding in rem (e.g., 1)
    - between_elements: Space between elements in rem (e.g., 0.5)

    Example:
        set_spacing(top=1, bottom=0.5, between_elements=0.3)
    """
    css = "<style>"

    if top is not None:
        css += f".block-container {{ padding-top: {top}rem !important; }}"

    if bottom is not None:
        css += f".block-container {{ padding-bottom: {bottom}rem !important; }}"

    if between_elements is not None:
        css += f"""
        .stMarkdown, .stButton, .stRadio, .stTextInput,
        .stNumberInput, .stVideo, .stImage {{
            margin-bottom: {between_elements}rem !important;
        }}
        """

    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)

def hide_element_by_label(label_text):
    """
    Hide a specific element by its label text.
    Useful for hiding unnecessary labels or text.

    Parameters:
    - label_text: The text of the label to hide

    Example:
        hide_element_by_label("Label Visibility")
    """
    st.markdown(
        f"""
        <style>
        label:contains("{label_text}") {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def set_column_heights(height_vh=None, height_px=None):
    """
    Set uniform height for all columns on the page.

    Parameters:
    - height_vh: Height as viewport percentage
    - height_px: Height in pixels

    Example:
        set_column_heights(height_vh=80)  # All columns are 80% of viewport
    """
    if height_vh:
        st.markdown(
            f"""
            <style>
            [data-testid="column"] {{
                height: {height_vh}vh !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    elif height_px:
        st.markdown(
            f"""
            <style>
            [data-testid="column"] {{
                height: {height_px}px !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def create_vertical_spacer(height_rem=1):
    """
    Create vertical space between elements.

    Parameters:
    - height_rem: Height in rem units (e.g., 1, 0.5, 2)

    Example:
        create_vertical_spacer(0.5)  # Small gap
        create_vertical_spacer(2)    # Large gap
    """
    st.markdown(
        f"""
        <div style="height: {height_rem}rem;"></div>
        """,
        unsafe_allow_html=True
    )

def apply_custom_css(css_string):
    """
    Apply any custom CSS to the page.

    Parameters:
    - css_string: CSS code as string

    Example:
        apply_custom_css('''
            .stButton button {
                background-color: #4CAF50;
                color: white;
            }
        ''')
    """
    st.markdown(
        f"""
        <style>
        {css_string}
        </style>
        """,
        unsafe_allow_html=True
    )
