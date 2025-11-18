# Layout Customization Guide

This guide shows you how to customize the appearance and spacing of pages to minimize scrolling and optimize layout.

## Quick Start

All pages now use `apply_compact_layout()` which automatically reduces padding and spacing. You can further customize each page using the functions in `utils/styling.py`.

## Available Styling Functions

### 1. `apply_compact_layout()`

**What it does**: Reduces all padding, margins, and spacing to fit more content on screen without scrolling.

**Usage**: Already applied to all pages. This is your baseline.

```python
from utils.styling import apply_compact_layout

def show():
    apply_compact_layout()  # Call at start of page
    # ... rest of your page
```

---

### 2. `set_spacing(top, bottom, between_elements)`

**What it does**: Fine-tune spacing on the page.

**Parameters**:
- `top`: Top padding in rem units (1 rem ≈ 16px)
- `bottom`: Bottom padding in rem units
- `between_elements`: Space between all elements in rem units

**Example**:
```python
from utils.styling import set_spacing

# Very compact - minimal spacing
set_spacing(top=0.5, bottom=0.5, between_elements=0.2)

# Normal spacing
set_spacing(top=2, bottom=1, between_elements=0.5)

# Lots of space
set_spacing(top=3, bottom=2, between_elements=1)
```

**Where to use**: Any page where you want custom spacing.

---

### 3. `set_video_height(height_vh, height_px)`

**What it does**: Control video player height.

**Parameters** (use one):
- `height_vh`: Height as percentage of viewport (e.g., 40 = 40% of screen height)
- `height_px`: Height in pixels (e.g., 400)

**Example**:
```python
from utils.styling import set_video_height

# Video takes 50% of screen height
set_video_height(height_vh=50)

# Video is exactly 400 pixels tall
set_video_height(height_px=400)
```

**Where to use**: In `videoplayer.py` at the start of `display_rating_interface()`.

---

### 4. `create_vertical_spacer(height_rem)`

**What it does**: Add empty space between specific elements.

**Parameters**:
- `height_rem`: Space height in rem units

**Example**:
```python
from utils.styling import create_vertical_spacer

st.markdown("### Section 1")
create_vertical_spacer(1)  # Small gap
st.markdown("### Section 2")
create_vertical_spacer(2)  # Large gap
st.markdown("### Section 3")
```

**Where to use**: Between any elements where you want extra space.

---

### 5. `apply_custom_css(css_string)`

**What it does**: Apply any custom CSS styling.

**Example**:
```python
from utils.styling import apply_custom_css

# Make buttons bigger and green
apply_custom_css('''
    .stButton button {
        font-size: 1.5rem;
        padding: 1rem 2rem;
        background-color: #4CAF50;
    }
''')

# Hide specific text
apply_custom_css('''
    h3 {
        display: none;
    }
''')
```

**Where to use**: When you need very specific styling changes.

---

## Common Customization Scenarios

### Scenario 1: Make Welcome Page Fit Without Scrolling

**File**: `pages/welcome.py`

```python
def show():
    # Apply compact layout
    apply_compact_layout()

    # Further reduce spacing
    set_spacing(top=1, bottom=0.5, between_elements=0.3)

    st.title("⚽ Creativity Rating App")

    # Use st.markdown instead of multiple paragraphs
    st.markdown("""
    ## Welcome!
    Instructions here...
    """)

    # Buttons at bottom
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("▶️ Next", ...)
```

**Result**: All content visible without scrolling.

---

### Scenario 2: Optimize Video Player Page

**File**: `pages/videoplayer.py`

**Option A: Smaller video for more rating scales**

```python
def display_rating_interface(action_id, video_filename, config):
    apply_compact_layout()

    # Video takes only 35% of screen
    set_video_height(height_vh=35)

    # Tight spacing
    set_spacing(top=0.5, bottom=0.5, between_elements=0.3)

    # ... rest of code
```

**Option B: Larger video, fewer scales**

```python
def display_rating_interface(action_id, video_filename, config):
    apply_compact_layout()

    # Video takes 60% of screen
    set_video_height(height_vh=60)

    # Normal spacing
    set_spacing(top=1, bottom=0.5, between_elements=0.5)

    # ... rest of code
```

---

### Scenario 3: Remove Unnecessary Text

**Example**: Hide section headers to save space

```python
# Instead of showing "### Video" heading
# st.markdown("### Video")  # Comment this out
st.video(video_file)

# Or use custom CSS to hide all h3 headers
apply_custom_css('''
    h3 {
        display: none !important;
    }
''')
```

---

### Scenario 4: Adjust Metadata Display Height

**File**: `pages/videoplayer.py`

```python
# Make metrics smaller
apply_custom_css('''
    [data-testid="stMetricValue"] {
        font-size: 1rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
    }
''')
```

---

### Scenario 5: Compact Questionnaire Form

**File**: `pages/questionnaire.py`

```python
def show():
    apply_compact_layout()

    # Very tight spacing for forms
    set_spacing(top=0.5, bottom=0.5, between_elements=0.2)

    # Make form labels smaller
    apply_custom_css('''
        .stTextInput label,
        .stNumberInput label,
        .stRadio label {
            font-size: 0.9rem !important;
        }
    ''')

    # ... rest of code
```

---

## Step-by-Step Customization Process

### Step 1: Identify the Problem

Run your app and note where scrolling is required:
- Which page has too much scrolling?
- Which elements take up too much space?
- What content could be smaller or removed?

### Step 2: Apply Compact Layout

If not already done, add to the page:
```python
from utils.styling import apply_compact_layout
apply_compact_layout()
```

### Step 3: Adjust Spacing

Experiment with values:
```python
set_spacing(top=1, bottom=0.5, between_elements=0.3)
```

Try different values:
- Smaller numbers = tighter spacing
- Larger numbers = more breathing room

### Step 4: Control Specific Elements

For videos:
```python
set_video_height(height_vh=40)  # Adjust the number
```

For custom needs:
```python
apply_custom_css('''
    /* Your CSS here */
''')
```

### Step 5: Test and Iterate

1. Save your changes
2. Refresh the browser (Streamlit auto-reloads)
3. Check if scrolling is reduced
4. Adjust values as needed

---

## Finding CSS Selectors

To customize specific elements, you need to know their CSS selectors.

**Method 1: Browser Inspector**

1. Right-click on element in browser
2. Choose "Inspect" or "Inspect Element"
3. Look for `data-testid` or class names
4. Use these in your CSS

**Method 2: Common Streamlit Selectors**

```css
/* Titles */
h1, h2, h3

/* Buttons */
.stButton button

/* Text inputs */
.stTextInput

/* Radio buttons */
.stRadio

/* Checkboxes */
.stCheckbox

/* Videos */
[data-testid="stVideo"]

/* Metrics */
[data-testid="stMetricValue"]
[data-testid="stMetricLabel"]

/* Columns */
[data-testid="column"]

/* Main container */
.block-container

/* Horizontal rules */
hr
```

---

## Example: Complete Video Player Optimization

Here's a complete example optimizing the video player page:

```python
def display_rating_interface(action_id, video_filename, config):
    # Step 1: Apply compact layout
    apply_compact_layout()

    # Step 2: Set video height to 40% of screen
    set_video_height(height_vh=40)

    # Step 3: Tight spacing
    set_spacing(top=0.5, bottom=0.5, between_elements=0.3)

    # Step 4: Custom adjustments
    apply_custom_css('''
        /* Hide section headers */
        h3 {
            display: none !important;
        }

        /* Smaller metrics */
        [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }

        /* Compact rating scales */
        .stRadio {
            margin-bottom: 0.3rem !important;
        }

        /* Remove horizontal rule spacing */
        hr {
            margin: 0.3rem 0 !important;
        }
    ''')

    # ... rest of your code
```

---

## Tips and Best Practices

1. **Start with compact_layout**: This gives you the biggest improvement
2. **Adjust video first**: Video usually takes the most space
3. **Use vh units**: `height_vh=40` adapts to different screen sizes
4. **Test on different screens**: What fits on desktop may not fit on laptop
5. **Iterate gradually**: Make small changes and test
6. **Comment your changes**: So you remember why you set values

---

## Common Values Reference

### Spacing (rem units)

- `0.2` - Extremely tight
- `0.3` - Very tight
- `0.5` - Compact (default after apply_compact_layout)
- `1.0` - Normal
- `2.0` - Spacious

### Video Height (% of viewport)

- `30vh` - Small video, lots of room for scales
- `40vh` - Balanced
- `50vh` - Half screen
- `60vh` - Large video
- `80vh` - Very large

### Button Padding

- `0.3rem 0.8rem` - Small buttons
- `0.4rem 1rem` - Compact (current default)
- `0.6rem 1.5rem` - Normal
- `1rem 2rem` - Large buttons

---

## Need More Help?

1. Check `utils/styling.py` for all available functions
2. Use browser inspector to find element selectors
3. Test on your target screen size
4. Remember: `1rem ≈ 16px`, `100vh = full screen height`

Happy customizing! 🎨
