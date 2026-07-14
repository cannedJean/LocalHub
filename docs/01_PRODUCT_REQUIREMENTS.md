# 01. Product Requirements

## MVP priority

### Must Have

| ID | Requirement | Frontend interpretation |
|---|---|---|
| M-01 | One target region | All screens use one configured region |
| M-02 | Anonymous community | No login gate or account UI |
| M-03 | Post CRUD | List, detail, create, edit and delete screens |
| M-04 | Password authorization | Password field during create and modal/form during edit/delete |
| M-05 | Category board | Filter posts by approved categories |
| M-06 | JSON-backed regional information | Show regional data delivered by backend |
| M-07 | Chatbot | Floating UI, history, mobile full-screen mode |
| M-08 | Vue 3 SPA | Client-side routing |
| M-09 | Responsive UI | Desktop and mobile states |
| M-10 | Deployment readiness | API URL comes from environment variable |

### Should Have

| ID | Requirement | Frontend interpretation |
|---|---|---|
| S-01 | Map visualization | Leaflet markers and category filters |
| S-02 | Post keyword search | Search title and content using backend query |
| S-03 | Suggested chatbot questions | Quick prompt chips |
| S-04 | Loading and error UX | Consistent feedback for all remote operations |

### Could Have

Only after Must and Should are complete:

- View count
- Simple statistics cards
- Festival calendar
- Link copy

### Won't Have

- Login, signup, JWT or OAuth
- Comments
- Likes or bookmarks
- Image upload
- Tags
- Weather
- Route guidance
- WebSocket
- i18n
- Admin panel
- Multi-region switching

## Functional requirements

### Home

- Show LocalHub identity and configured region.
- Show category shortcuts.
- Show recent posts.
- Show a map preview or link to map.
- Keep chatbot entry available.

### Board

- List posts with title, category and created date.
- Search by keyword.
- Filter by category.
- Support pagination.
- Navigate to post detail.
- Provide a clear write button.

### Post detail

- Display category, title, body and timestamps.
- Expose edit and delete actions.
- Ask for password before protected actions.
- Never display or return the saved password.

### Post form

- Fields: category, title, content and password.
- Password is required when creating.
- Editing requires authorization according to the API contract.
- Validate required fields before submission.
- Confirm success and return to detail/list.

### Map

- Display location markers from backend.
- Filter markers by category.
- Marker popup shows name, category and address.
- Show tile attribution.
- Handle missing coordinates without crashing.

### Chatbot

- Floating button on desktop.
- Dialog panel on desktop.
- Full-screen presentation on small mobile screens.
- Preserve history during the current browser session.
- Show suggested questions.
- Disable send while waiting.
- Display retryable error feedback.
