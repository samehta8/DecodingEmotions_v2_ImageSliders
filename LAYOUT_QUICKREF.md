# Layout Customization - Quick Reference Card

## 🎯 Most Common Adjustments

### 1. Make Page Fit Without Scrolling
```python
from utils.styling import apply_compact_layout, set_spacing

def show():
    apply_compact_layout()
    set_spacing(top=0.5, bottom=0.5, between_elements=0.3)
```

### 2. Control Video Size
```python
from utils.styling import set_video_height

# Video takes 40% of screen
set_video_height(height_vh=40)
```

### 3. Add Space Between Elements
```python
from utils.styling import create_vertical_spacer

st.markdown("Section 1")
create_vertical_spacer(1)  # Add space here
st.markdown("Section 2")
```

### 4. Hide Unwanted Elements
```python
from utils.styling import apply_custom_css

# Hide all h3 headers
apply_custom_css('''
    h3 {
        display: none !important;
    }
''')
```

---

## 📐 Common Values

| Element | Small | Medium | Large |
|---------|-------|--------|-------|
| **Spacing** | 0.3 rem | 0.5 rem | 1.0 rem |
| **Video Height** | 30vh | 40vh | 60vh |
| **Top Padding** | 0.5 rem | 1 rem | 2 rem |

---

## 📍 Where to Add Code

### Welcome Page (`pages/welcome.py`)
```python
def show():
    apply_compact_layout()  # ← Add here
    set_spacing(top=1, bottom=0.5, between_elements=0.3)  # ← Add here
    st.title("⚽ Creativity Rating App")
    # ... rest of code
```

### Video Player (`pages/videoplayer.py`)
```python
def display_rating_interface(action_id, video_filename, config):
    apply_compact_layout()  # ← Add here
    set_video_height(height_vh=40)  # ← Add here
    # ... rest of code
```

### Questionnaire (`pages/questionnaire.py`)
```python
def show():
    apply_compact_layout()  # ← Add here
    # ... rest of code
```

---

## 🔧 Quick Fixes

### Problem: Video too large
```python
set_video_height(height_vh=30)  # Make smaller
```

### Problem: Too much space between elements
```python
set_spacing(between_elements=0.2)  # Tighter spacing
```

### Problem: Ratings don't fit on screen
```python
apply_custom_css('''
    .stRadio {
        margin-bottom: 0.2rem !important;
    }
''')
```

### Problem: Metadata section too tall
```python
apply_custom_css('''
    [data-testid="stMetricValue"] {
        font-size: 0.9rem !important;
    }
''')
```

---

## 💡 Pro Tips

1. **Always apply compact_layout first** - it gives the biggest improvement
2. **Use vh units for video** - adapts to different screen sizes (e.g., `40vh` = 40% of screen)
3. **Test after each change** - Streamlit auto-reloads when you save
4. **Start with suggested values** - then adjust up/down by small increments

---

## 🎨 Copy-Paste Templates

### Template 1: Minimal Scrolling (Video Player)
```python
def display_rating_interface(action_id, video_filename, config):
    apply_compact_layout()
    set_video_height(height_vh=35)
    set_spacing(top=0.5, bottom=0.5, between_elements=0.3)

    apply_custom_css('''
        h3 { display: none !important; }
        hr { margin: 0.3rem 0 !important; }
    ''')
    # ... rest of code
```

### Template 2: Compact Form (Questionnaire)
```python
def show():
    apply_compact_layout()
    set_spacing(top=0.5, bottom=0.5, between_elements=0.2)

    apply_custom_css('''
        label { font-size: 0.9rem !important; }
    ''')
    # ... rest of code
```

### Template 3: Clean Welcome Page
```python
def show():
    apply_compact_layout()
    set_spacing(top=1, bottom=0.5, between_elements=0.4)
    # ... rest of code
```

---

**For detailed explanations, see `LAYOUT_CUSTOMIZATION.md`**
