# Design System CSS Variables & Reusable Classes

## CSS Variables (Defined in `:root`)

### Colors
```css
--primary-navy: #1a3a52;          /* Main corporate color */
--primary-light: #2a5a7f;         /* Lighter navy for accents */
--accent-blue: #3b82f6;           /* Button primary color */
--accent-teal: #14b8a6;           /* Secondary accent */
--success: #059669;               /* Success/positive states */
--warning: #d97706;               /* Warning/caution states */
--danger: #dc2626;                /* Error/rejected states */
--white: #ffffff;                 /* White */
--light-grey: #f9fafb;            /* Very light background */
--medium-grey: #e5e7eb;           /* Borders and dividers */
--dark-grey: #6b7280;             /* Secondary text */
--text-dark: #1f2937;             /* Primary text */
```

### Spacing
```css
--spacing-xs: 0.5rem;             /* 8px */
--spacing-sm: 1rem;               /* 16px */
--spacing-md: 1.5rem;             /* 24px */
--spacing-lg: 2rem;               /* 32px */
--spacing-xl: 3rem;               /* 48px */
```

### Typography
```css
--font-family-main: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
--font-size-xs: 0.75rem;          /* 12px */
--font-size-sm: 0.875rem;         /* 14px */
--font-size-base: 1rem;           /* 16px */
--font-size-lg: 1.125rem;         /* 18px */
--font-size-xl: 1.5rem;           /* 24px */
--font-size-2xl: 2rem;            /* 32px */
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Border & Radius
```css
--border-radius-sm: 4px;
--border-radius-md: 8px;
--border-radius-lg: 12px;
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
```

---

## Reusable CSS Classes

### Navigation Buttons (Header)
```css
.btn-nav              /* Inactive nav button - transparent with border */
.btn-nav-active       /* Active nav button - filled blue */
```

### Action Buttons (Main Pages)
```css
.btn-action           /* Base action button */
.btn-action-primary   /* Blue background - main CTAs */
.btn-action-secondary /* Navy background - secondary CTAs */
.btn-action-tertiary  /* Teal background - alternate CTAs */
```

### Small Button
```css
.btn-small           /* Compact button for tables/dense layouts */
```

### Page Structure
```css
.page-title          /* Large main heading (h1 equivalent) */
.page-subtitle       /* Subtitle explaining page purpose */
```

### Forms
```css
.form-card           /* Container for form (max 700px, centered) */
.form-title          /* Heading inside form */
.required            /* Red asterisk for required fields */
.form-hint           /* Small grey text below inputs */
.form-actions        /* Button container for form submit/cancel */
.form-group          /* Wrapper for label + input */
```

### Dashboard Stats
```css
.stat-grid           /* Container for stat cards */
.stat-card           /* Individual statistic card */
.stat-label          /* Label text in stat card */
.stat-value          /* Large number in stat card */
```

### Tables
```css
.table-card          /* Wrapper around table */
.ats-score-badge     /* Circular ATS score badge with color variants */
.ats-score-badge.excellent   /* Green variant (80+) */
.ats-score-badge.good        /* Amber variant (60-79) */
.ats-score-badge.poor        /* Red variant (below 60) */
```

### Status Badges
```css
.badge               /* Base badge/pill styling */
.badge-applied       /* Light blue - Applied status */
.badge-interview     /* Light amber - Interview status */
.badge-rejected      /* Light red - Rejected status */
```

### Resume Analyzer
```css
.error-alert         /* Red error message container */
.result-header       /* Header section for analysis results */
.job-info-grid       /* Grid for company/position info */
.job-info-item       /* Individual job info card */
.job-info-label      /* Label in job info */
.job-info-value      /* Value in job info */

.ats-result-section  /* Wrapper for ATS score section */
.ats-score-container /* Container for score display */
.ats-score-display   /* Circular ATS score display */
.ats-score-display.excellent  /* Green variant */
.ats-score-display.good       /* Amber variant */
.ats-score-display.poor       /* Red variant */
.ats-score-value     /* Large percentage text */
.ats-score-label     /* Label below score */

.score-interpretation    /* Card explaining score meaning */
.score-interpretation.excellent
.score-interpretation.good
.score-interpretation.poor

.keywords-section        /* Container for keywords results */
.keywords-container      /* Two-column grid for matched/missing */
.keywords-card           /* Card for matched or missing keywords */
.keywords-card.matched   /* Green-styled keywords card */
.keywords-card.missing   /* Amber-styled keywords card */
.keywords-list           /* Flex container for keyword badges */
.keyword-badge           /* Individual keyword pill */
.keyword-badge.matched   /* Green keyword badge */
.keyword-badge.missing   /* Amber keyword badge */
.keywords-count          /* Counter text */
.keywords-empty          /* Empty state message */
.keywords-perfect        /* Success message */
.missing-keywords-tips   /* Tips for improvement */

.extracted-text-section  /* Textarea container */
.extracted-text          /* Textarea for resume text */

.tips-section            /* Tips container */
.tips-grid               /* Grid layout for tips */
.tip-card                /* Individual tip card */
```

### Sections & Info
```css
.section-title       /* Medium heading for sections */
.section-subtitle    /* Subtitle for sections */

.info-section        /* Wrapper for info/tips section */
.info-grid           /* Grid for info cards */
.info-card           /* Individual info card */
.info-step           /* Numbered circle for steps */

.empty-state         /* Container for empty state message */
```

### General
```css
.container           /* Max-width wrapper (1200px) */
.content-wrapper     /* Card wrapper with padding and shadow */
.card                /* General purpose card container */
.flex-center         /* Flex centered container */

.text-center         /* Center aligned text */
.text-muted          /* Dark grey text for secondary info */
.text-success        /* Green text */
.text-warning        /* Amber text */
.text-danger         /* Red text */

.grid                /* CSS Grid for auto-fit */
.gap-sm, .gap-md, .gap-lg  /* Gap helpers */

.mt-small, .mt-medium, .mt-large  /* Margin-top helpers */
.mb-small, .mb-medium, .mb-large  /* Margin-bottom helpers */
```

---

## Usage Examples

### Creating a New Button
```html
<!-- Primary action -->
<a href="/action" class="btn btn-action btn-action-primary">
    Click Me
</a>

<!-- Secondary action -->
<button class="btn btn-action btn-action-secondary">
    Cancel
</button>

<!-- Nav button -->
<a href="/page" class="btn btn-nav">Page</a>
```

### Creating a Stat Card
```html
<div class="stat-card">
    <div class="stat-label">Total Applications</div>
    <div class="stat-value">42</div>
</div>
```

### Creating a Status Badge
```html
<span class="badge badge-applied">Applied</span>
<span class="badge badge-interview">Interview</span>
<span class="badge badge-rejected">Rejected</span>
```

### Creating an ATS Score Badge
```html
<div class="ats-score-badge excellent">85%</div>
<div class="ats-score-badge good">72%</div>
<div class="ats-score-badge poor">45%</div>
```

### Creating a Form Group
```html
<div class="form-group">
    <label for="input">Field Name <span class="required">*</span></label>
    <input type="text" id="input" name="input">
    <p class="form-hint">Helpful hint text here</p>
</div>
```

---

## Responsive Breakpoints

### Desktop (Default)
- Full featured layout
- Multiple columns
- Maximum spacing

### Tablet (max-width: 768px)
- Adjusted font sizes
- Reduced spacing
- Flexible grid columns
- Touch-friendly buttons

### Mobile (max-width: 480px)
- Single column layouts
- Minimal padding
- Readable fonts
- Optimized for touch

---

## Customization Quick Tips

### Change Brand Color
Find and replace `--primary-navy: #1a3a52` with your color

### Change Button Color
Find `.btn-action-primary` and change `background-color`

### Change Spacing
Adjust `--spacing-md` and other spacing variables in `:root`

### Change Font
Update `--font-family-main` with your preferred font

### Change Border Radius
Update `--border-radius-md` and `--border-radius-lg`

---

## Notes for Developers

1. **Always use variables** - Don't hardcode colors or spacing
2. **Reuse classes** - Apply existing classes before creating new ones
3. **Maintain consistency** - Keep spacing and sizing predictable
4. **Test responsive** - Check layouts on mobile, tablet, and desktop
5. **Use semantic HTML** - Proper heading hierarchy, form labels, etc.
6. **Keep it simple** - This is intentionally beginner-friendly

---

Generated: January 3, 2026
