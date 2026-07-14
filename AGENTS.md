# LocalHub Agent Instructions

## 1. Mission

Build the LocalHub frontend as a Vue.js 3 SPA that faithfully implements the approved Figma design and the MVP requirements in `/docs`.

The frontend must remain compatible with the FastAPI API contract in `docs/07_API_CONTRACT.md`.

## 2. Read-first documents

Before modifying code, read:

1. `docs/00_PROJECT_CONTEXT.md`
2. `docs/01_PRODUCT_REQUIREMENTS.md`
3. `docs/05_DESIGN_SYSTEM.md`
4. `docs/06_COMPONENT_SPEC.md`
5. `docs/07_API_CONTRACT.md`
6. `docs/08_FRONTEND_ARCHITECTURE.md`
7. `docs/10_ACCEPTANCE_CRITERIA.md`

For a Figma-driven task, also read `docs/11_FIGMA_FILE_SPEC.md`.

## 3. Fixed technology decisions

- Framework: Vue.js 3
- Build tool: Vite
- Language: JavaScript
- Component style: Vue Single File Components
- Routing: Vue Router
- HTTP: Axios through `src/services/http.js`
- Styling: global CSS tokens plus scoped component CSS
- Map: Leaflet with an approved tile provider and visible attribution
- State: local component state and composables; do not add Pinia unless explicitly approved
- Icons: use assets supplied by Figma or the existing project assets; do not add a new icon package without approval

## 4. Non-negotiable scope

Implement only the approved MVP:

- Home
- Post list, detail, create, edit, delete
- Password verification for edit/delete
- Category filtering and keyword search
- Map markers and category filtering
- Floating chatbot and mobile full-screen chatbot
- Responsive layout
- Loading, empty, error and success feedback states

Do not add:

- Authentication or account management
- Comments
- Likes, bookmarks or tags
- Image upload
- Weather or route APIs
- WebSocket
- Internationalization
- Admin pages
- Unapproved dependencies

## 5. Coding rules

- Reuse existing components before creating a new component.
- Do not hardcode API URLs, colors, spacing, radius or z-index values.
- Use CSS variables from `src/styles/tokens.css`.
- Keep page components orchestration-focused; move reusable UI to `src/components`.
- All API calls must go through `src/services`.
- Do not return or display post passwords.
- Do not place API keys or secrets in frontend code.
- Preserve accessibility: semantic elements, labels, keyboard access, visible focus and descriptive button text.
- Every page must support loading, empty and error states.
- Do not modify backend files unless explicitly requested.

## 6. Figma MCP translation rules

- Fetch structured design context for the exact node.
- Fetch a screenshot for visual comparison.
- Fetch variables used by the selection.
- Treat generated React/Tailwind as design representation only.
- Translate output to Vue SFC and this repository's CSS token system.
- Reuse existing LocalHub components.
- Do not create placeholder assets when Figma provides an asset.
- Verify desktop and mobile behavior against Figma before completion.

## 7. Completion report

After a task, report:

- Files created or changed
- Routes or components affected
- API endpoints used
- Assumptions made
- Tests performed
- Remaining risks or blockers
