---
name: Technical Precision
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#38393a'
  surface-container-lowest: '#0c0f0f'
  surface-container-low: '#1a1c1c'
  surface-container: '#1e2020'
  surface-container-high: '#282a2b'
  surface-container-highest: '#333535'
  on-surface: '#e2e2e2'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#e2e2e2'
  inverse-on-surface: '#2f3131'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#c8c6c5'
  on-secondary: '#313030'
  secondary-container: '#474746'
  on-secondary-container: '#b7b4b4'
  tertiary: '#ffb786'
  on-tertiary: '#502400'
  tertiary-container: '#df7412'
  on-tertiary-container: '#461f00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb786'
  on-tertiary-fixed: '#311400'
  on-tertiary-fixed-variant: '#723600'
  background: '#121414'
  on-background: '#e2e2e2'
  surface-variant: '#333535'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  code-block:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 32px
---

## Brand & Style
The design system is built for high-performance learning and technical preparation. The aesthetic is rooted in **Minimalism** and **Modern Corporate** styles, prioritizing function over form. It draws inspiration from developer-centric platforms like LeetCode and roadmap.sh, emphasizing data density, logical grouping, and immediate access to information.

The target audience consists of software engineers and technical professionals who value efficiency and clarity. The UI should feel like a sophisticated tool—unobtrusive, reliable, and precise. Visual noise is eliminated to ensure the user’s cognitive load is reserved entirely for the content, such as complex algorithms and technical roadmaps.

## Colors
The palette is strictly functional, utilizing a deep-dark foundation to reduce eye strain during long study sessions.

- **Primary (#3b82f6):** Reserved for primary actions, progress indicators, and active states. It provides a sharp contrast against the dark background.
- **Surface (#171717):** Used for cards, code editors, and sidebars to create subtle depth against the background.
- **Text (#ededed):** High-contrast off-white for maximum readability. Secondary text should use a reduced opacity (e.g., 60%) rather than a different hue.
- **Border (#262626):** Defines the structure. In a shadowless environment, borders are the primary tool for element separation.

## Typography
The system uses **Inter** for all UI elements to ensure a clean, neutral, and systematic feel. **JetBrains Mono** is introduced specifically for code blocks and technical identifiers to provide the necessary fixed-width precision.

Typography is scaled for high information density. Paragraphs use a standard 16px size for readability, while metadata and labels scale down to 12-14px to maximize screen real estate. Use tabular numbers for any data involving timing, memory usage, or scoring.

## Layout & Spacing
The design system employs a **Fluid Grid** with tight gutters to maintain high data density. 

- **Grid:** A 12-column system for desktop, collapsing to 1 column for mobile.
- **Rhythm:** An 8px base grid governs all dimensions. Use 16px (md) for standard padding within containers and 8px (sm) for tighter groupings like list items or meta-info rows.
- **Reflow:** On desktop, the layout should utilize split-pane views (e.g., problem description on the left, code editor on the right). On mobile, these panes should stack vertically or be accessible via persistent tabs.

## Elevation & Depth
Depth is achieved through **Tonal Layers** and **Low-contrast Outlines** rather than shadows. 

- **Tier 0 (Background):** #0a0a0a - The base canvas.
- **Tier 1 (Surface):** #171717 - Navigation bars, sidebars, and card containers.
- **Tier 2 (Interactive):** #262626 - Hover states for list items or subtle button backgrounds.

Borders are the primary separators. Every container should have a 1px solid border (#262626). Do not use drop shadows; the UI should appear flat and structurally integrated into the grid.

## Shapes
The shape language is disciplined and geometric. A "Soft" roundedness (4px-8px) is applied to maintain a modern feel while staying true to the "Technical" aesthetic. 

- **Small elements (Checkboxes, Tags):** 4px.
- **Standard elements (Buttons, Inputs, Cards):** 6px.
- **Large containers (Modals):** 8px.
Avoid fully rounded "pill" shapes, as they contradict the structured, grid-based logic of the platform.

## Components
- **Buttons:** Primary buttons use a solid blue background with white text. Secondary buttons are ghost-style with a border and no fill, becoming #262626 on hover.
- **Code Blocks:** Use a slightly darker background than the surface (#0e0e0e). Syntax highlighting should follow a "One Dark" or similar high-contrast theme.
- **Inputs:** Text fields use the #0a0a0a background with a #262626 border. On focus, the border changes to the primary blue.
- **Status Chips:** Use subtle background tints with high-contrast text (e.g., a "Solved" chip uses a dark green background with a bright green text).
- **Progress Roadmaps:** Represented by 2px lines and 12px circular nodes. Active nodes are filled with the primary blue; completed nodes use a checkmark icon; pending nodes remain bordered.
- **Data Tables:** High-density, 12px padding on cells, with 1px bottom borders for row separation. No zebra-striping.