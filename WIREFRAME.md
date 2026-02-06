# TrashCollector AI - Wireframe & UI Overview

## Application Architecture

### Single Page Application
- **Framework**: Pure HTML/CSS/JavaScript (No framework)
- **Hosting**: Python HTTP Server (localhost:8000)
- **Input**: Image uploads via file input or drag-drop
- **Output**: JSON classification results with visual feedback

---

## Page Layout Breakdown

### HEADER SECTION
```
╔════════════════════════════════════════════════════════════════════╗
║                      GRADIENT HEADER (GREEN)                       ║
║                         TrashCollector AI                          ║
║                  Smart Waste Segregation System                    ║
║                    (White text, centered)                          ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Height: 120px
- Background: Linear gradient (Green #059669 → #047857)
- Text Color: White (#dcfce7)
- Font Size: H1 42px bold, P 16px light

---

### STATUS BAR
```
╔════════════════════════════════════════════════════════════════════╗
║  Model: gemma3:4b-cloud        │        Status: Active (green)    ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Height: 60px
- Background: Semi-transparent green overlay
- Layout: Flexbox, space-between
- Label Color: #86efac
- Value Color: #dcfce7

---

### MAIN CONTENT AREA

#### 1. UPLOAD SECTION
```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║                           📷                                       ║
║                   Drop image here or click                         ║
║                   to upload                                        ║
║                                                                    ║
║              Supports: JPG, PNG, WEBP (max 5MB)                   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Width: 100% - 80px padding
- Height: 200px
- Border: 2px dashed green (#16a34a)
- Border Radius: 20px
- Background: Semi-transparent green gradient
- Hover: Lift up 5px, shadow increase

**Interactive:**
- Click to open file dialog
- Drag & drop enabled

---

#### 2. PREVIEW SECTION (After upload)
```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║                    ┌─────────────────────┐                        ║
║                    │                     │                        ║
║                    │   [Image Preview]   │                        ║
║                    │    (320x320px)      │                        ║
║                    │                     │                        ║
║                    └─────────────────────┘                        ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Max Width: 320px
- Max Height: 320px
- Border Radius: 20px
- Shadow: 0 20px 50px rgba(22, 163, 74, 0.4)

---

#### 3. CLASSIFY BUTTON
```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║                  [  Classify Waste  ]                             ║
║                   (Gradient Green)                                 ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Width: ~200px
- Height: 50px
- Background: Linear gradient (Green #16a34a → #22c55e)
- Border Radius: 50px
- Font: 16px bold
- States: Normal, Hover (lift + shadow), Disabled (opacity 0.5)

---

#### 4. LOADING STATE
```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║                       [Spinning Spinner]                          ║
║                                                                    ║
║              Analyzing image with AI...                           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Spinner: 60x60px
- Border: 4px dashed green
- Animation: 0.8s rotation

---

#### 5. ERROR STATE
```
╔════════════════════════════════════════════════════════════════════╗
║  ⚠️  Error message text here                                       ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Full width - padding
- Height: Auto (min 50px)
- Background: Red overlay gradient
- Border Left: 4px solid red
- Text Color: Light red (#fca5a5)
- Border Radius: 15px

---

#### 6. RESULTS SECTION (Dynamic background change)
```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║  OBJECT IDENTIFIED                                                ║
║  Plastic Bottle                                                    ║
║                                                                    ║
║  WASTE CATEGORY                                                    ║
║  ┌──────────────────────────────────┐                            ║
║  │  Plastic (Gradient Background)   │                            ║
║  └──────────────────────────────────┘                            ║
║                                                                    ║
║  DISPOSAL INSTRUCTIONS                                            ║
║  ═══════════════════════════════════════════════════════════════  ║
║  │  Rinse thoroughly, remove labels, and place in the recycling ║
║  │  bin. Crush if possible to save space.                        ║
║  ════════════════════════════════════════════════════════════════ ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Width: 100% - 80px padding
- Padding: 40px
- Background: Semi-transparent green gradient
- Border: 1px solid green overlay
- Border Radius: 20px
- Animation: Slide up 0.6s

**Element Breakdown:**
- Headers: 12px, uppercase, green (#86efac), 1px letter-spacing
- Object: 28px, bold, light text
- Category button: 18px, gradient background, inline-block, 50px radius
- Instruction box: Dark background, left border 5px green

---

### CATEGORIES GRID
```
╔════════════════════════════════════════════════════════════════════╗
║  🟢    🔵    🟡    ⚪    🔷    🟣    🔴    🌱    💨    ⚫          ║
║  Wet   Dry   Plastic Metal Glass E-Waste Hazard Bio Sprays Unknown ║
╚════════════════════════════════════════════════════════════════════╝
```

**Dimensions:**
- Grid: auto-fit, minmax(85px, 1fr)
- Gap: 15px
- Card: 85x85px min
- Border Radius: 15px
- Shadow: 0 10px 30px
- Hover: Lift 5px, shadow increase

**Categories (10 total):**
1. 🟢 Wet (Green gradient)
2. 🔵 Dry (Blue gradient)
3. 🟡 Plastic (Amber gradient)
4. ⚪ Metal (Gray gradient)
5. 🔷 Glass (Teal gradient)
6. 🟣 E-Waste (Purple gradient)
7. 🔴 Hazardous (Red gradient)
8. 🌱 Biowaste (Lime gradient)
9. 💨 Sprays (Cyan gradient)
10. ⚫ Unknown (Dark gray gradient)

---

## Container Layout

### OUTER CONTAINER
- **Max Width**: 850px
- **Margin**: 0 auto (centered)
- **Border Radius**: 25px
- **Background**: Linear gradient dark green overlay
- **Border**: 1px solid green overlay
- **Backdrop Filter**: blur(10px)
- **Shadow**: Multiple layers + inset highlight

### BODY BACKGROUND
- **Default**: Green gradient (Dark to medium green)
- **On Result**: Changes to category gradient (0.6s transition)
- **Fixed Radial Gradients**: Green accent circles at 20% and 80%

---

## Color Scheme - GREEN THEME

### Primary Colors
- **Primary Green**: #16a34a
- **Secondary Green**: #22c55e
- **Accent Green**: #4ade80

### Category Gradients
| Category | Gradient | Usage |
|----------|----------|-------|
| Wet | #059669 → #047857 | Organic waste |
| Dry | #3b82f6 → #1d4ed8 | Paper, cardboard |
| Plastic | #f59e0b → #d97706 | Bottles, wrappers |
| Metal | #6b7280 → #374151 | Cans, foil |
| Glass | #14b8a6 → #0d9488 | Bottles, jars |
| E-Waste | #8b5cf6 → #6d28d9 | Electronics |
| Hazardous | #ef4444 → #dc2626 | Chemicals |
| Biowaste | #84cc16 → #65a30d | Organic matter |
| Sprays | #06b6d4 → #0891b2 | Aerosols |
| Unknown | #6b7280 → #1f2937 | Unidentified |

### Text Colors
- **Primary Text**: #dcfce7 (Light mint)
- **Secondary Text**: #86efac (Medium green)
- **Link/Label**: #94a3b8 (Slate)
- **White**: #f0fdf4

---

## Interactive States

### BUTTON STATES
| State | Styling |
|-------|---------|
| Default | Green gradient, box-shadow |
| Hover | translateY(-3px), enhanced shadow |
| Active | Scale 1.05 (category results) |
| Disabled | opacity 0.5 |

### UPLOAD AREA STATES
| State | Styling |
|-------|---------|
| Default | Dashed border, semi-transparent |
| Hover | Darker bg, lifted, shadow |
| Drag Over | Bright bg, strong shadow |
| Active | Image preview appears |

### LOADING STATE
| Feature | Animation |
|---------|-----------|
| Spinner | 0.8s linear rotation |
| Progress | Continuous loop |
| UI | Opacity fade in |

---

## Responsive Design

### Breakpoints
- **Mobile**: < 500px
  - Single column grid for categories
  - Reduced padding
  - Smaller fonts

- **Tablet**: 500px - 850px
  - 2-3 column grid for categories
  - Medium spacing

- **Desktop**: > 850px
  - Container max-width: 850px
  - Full grid display (auto-fit)
  - Full spacing and effects

### Adjustments
- All shadows scale appropriately
- Border radius stays consistent
- Font sizes scale down on mobile
- Padding reduces on small screens

---

## API Integration Points

### Endpoints Used
1. **GET /** - Returns HTML page
2. **POST /classify** - Accepts FormData with image file
3. **Response** - JSON with:
   - `success`: boolean
   - `object`: string (item name)
   - `category`: string (waste type)
   - `color`: string (gradient)
   - `instruction`: string (disposal info)

### Error Handling
- Network errors display in error box
- Invalid file formats trigger validation
- Timeout shows "Analyzing..." then error
- JSON parse failures caught gracefully

---

## Animation & Transitions

### Timings
| Element | Duration | Easing |
|---------|----------|--------|
| Background | 0.6s | ease |
| Results slide | 0.6s | cubic-bezier(0.34, 1.56, 0.64, 1) |
| Button hover | 0.3s | ease |
| Upload hover | 0.4s | cubic-bezier(0.34, 1.56, 0.64, 1) |
| Spinner | 0.8s | linear infinite |

---

## Accessibility Features

- High contrast text on dark backgrounds
- Color + emoji indicators for categories
- Error messages clear and visible
- Loading indicator obvious
- Button states clear (hover, disabled)
- Proper spacing for touch targets
- Keyboard navigable (tab, enter)

---

## Summary

**Page Type**: Single-page application with dynamic content updates

**Key Sections**:
1. Header (branding)
2. Status bar (info)
3. Upload interface
4. Preview area
5. Classify button
6. Loading state
7. Error display
8. Results display
9. Category reference grid

**Visual Design**: Dark green theme with vibrant category gradients

**UX Flow**: Upload → Preview → Classify → Dynamic Result Display

**Technology**: HTML + CSS + Vanilla JavaScript
