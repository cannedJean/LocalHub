# 11. Figma File Specification

## Page structure

```text
00_Cover
01_Foundations
02_Components
03_Desktop
04_Mobile
05_Prototype
06_Dev_Handoff
```

## Naming convention

Use semantic names. Do not use `Frame 123`, `Group 5` or `Rectangle 8`.

Examples:

```text
Screen/Home/Desktop
Screen/BoardList/Desktop
Screen/BoardList/Mobile
Component/Button
Component/PostCard
Component/ChatWidget
Section/RecentPosts
State/Empty
State/Error
```

## Variables

Create Figma Variables that match `tokens/design-tokens.json`.

Collections:

- `Color`
- `Spacing`
- `Radius`
- `Typography`
- `Elevation`

Variable names should map predictably to CSS variables.

Example:

```text
Figma: color/brand/600
CSS: --color-brand-600
```

## Required components and variants

### Button

Properties:

- Variant: Primary, Secondary, Ghost, Danger
- Size: Small, Medium, Large
- State: Default, Hover, Pressed, Disabled, Loading

### Input

- State: Default, Focus, Filled, Error, Disabled
- Optional label, hint and error slots

### Category chip

- Selected: True/False
- Icon: optional

### Post card/list item

- Desktop and mobile layouts
- Category, title, date

### Modal

- Password
- Delete confirmation
- Generic status

### Chat widget

- Closed
- Open/Idle
- Open/Loading
- Open/Error
- Desktop/Mobile

### Map marker/popup

- Attraction, Restaurant, Festival
- Default and selected

## Layout rules

- Use Auto Layout for all reusable components and primary sections.
- Use constraints for responsive behavior.
- Test frames at 360, 768, 1024 and 1440 widths.
- Repeated items must be component instances.
- Add annotations for interaction behavior not visible in static UI.
- Keep layer order and naming clean enough for MCP extraction.

## Required desktop frames

- Home
- Board list: default, search empty, loading/error
- Post detail
- Post create
- Post edit
- Map
- Chat open

## Required mobile frames

- Home
- Board list
- Post detail
- Post form
- Map
- Chat full-screen
- Mobile menu

## Handoff annotation format

Attach concise notes:

```text
Behavior:
- Search submits on Enter.
- Category updates the route query.
- Loading keeps layout height stable.

API:
- GET /api/posts
- Query: keyword, category, page

Responsive:
- Table becomes cards below 768px.
```

## MCP usage rule

For implementation, provide Cursor the exact node/frame URL, not only the file URL. Large pages should be implemented one screen or component at a time.
