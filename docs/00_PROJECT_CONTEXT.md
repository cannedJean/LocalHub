# 00. Project Context

## Project identity

| Field | Value |
|---|---|
| Product name | LocalHub |
| Product type | Public-data-based anonymous local information community |
| Target users | Local residents and tourists |
| Frontend | Vue.js 3 SPA |
| Backend | FastAPI REST API |
| Database | SQLite through SQLAlchemy |
| Frontend deployment | Netlify |
| Backend deployment | Render |
| Deadline | 2026-07-15 21:00 KST |

## Required project variables

```yaml
TARGET_REGION: TBD
FIGMA_FILE_URL: TBD
API_BASE_URL_LOCAL: http://localhost:8000
API_BASE_URL_PRODUCTION: TBD
MAP_LIBRARY: Leaflet
MAP_TILE_PROVIDER: TBD_APPROVED_PROVIDER
```

### Rule

Do not infer `TARGET_REGION`, production URL or map provider. Stop and request the missing value when it is required for implementation.

## Product statement

LocalHub helps residents and tourists discover trusted local attractions, restaurants and festivals from prepared public-data JSON, while allowing anonymous users to share community posts without account registration.

## MVP value proposition

A user can:

1. Discover selected-region information.
2. browse and search anonymous posts.
3. create, update and delete their own post with a password.
4. inspect places on a map.
5. ask a chatbot questions grounded in provided regional data and community posts.

## Core constraints

- Exactly one region is implemented.
- There is no login or user account.
- Post edit/delete authorization uses the post password.
- Frontend secrets are prohibited.
- The UI must work on desktop and mobile.
- Figma is the visual source of truth; project tokens and components are the implementation source of truth.
