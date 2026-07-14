# 02. Information Architecture

## Sitemap

```text
/
├─ /boards
│  ├─ /boards/new
│  ├─ /boards/:id
│  └─ /boards/:id/edit
├─ /map
└─ global chatbot overlay
```

## Router specification

| Path | Route name | Page component | Purpose |
|---|---|---|---|
| `/` | `home` | `HomeView.vue` | Region overview and recent posts |
| `/boards` | `post-list` | `PostListView.vue` | Searchable and filterable board |
| `/boards/new` | `post-create` | `PostFormView.vue` | Create a post |
| `/boards/:id` | `post-detail` | `PostDetailView.vue` | Read a post |
| `/boards/:id/edit` | `post-edit` | `PostFormView.vue` | Edit an authorized post |
| `/map` | `map` | `MapView.vue` | Regional location map |
| `/:pathMatch(.*)*` | `not-found` | `NotFoundView.vue` | 404 |

## Global navigation

Desktop header:

- LocalHub logo → Home
- 지역 정보/지도 → Map
- 커뮤니티 → Board
- 글쓰기 → New post

Mobile header:

- Logo
- Menu button
- Drawer with the same destinations

Chatbot is globally mounted in `App.vue`, except when explicitly hidden on error pages.
