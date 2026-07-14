# 08. Frontend Architecture

## Target structure

```text
localhub-frontend/
├─ public/
├─ src/
│  ├─ assets/
│  ├─ components/
│  │  ├─ common/
│  │  ├─ board/
│  │  ├─ map/
│  │  └─ chat/
│  ├─ composables/
│  ├─ config/
│  ├─ router/
│  ├─ services/
│  ├─ styles/
│  ├─ utils/
│  ├─ views/
│  ├─ App.vue
│  └─ main.js
├─ .env.example
└─ package.json
```

## Suggested files

```text
src/
├─ components/common/
│  ├─ AppHeader.vue
│  ├─ AppFooter.vue
│  ├─ BaseButton.vue
│  ├─ BaseInput.vue
│  ├─ BaseModal.vue
│  ├─ EmptyState.vue
│  └─ ErrorState.vue
├─ components/board/
│  ├─ CategoryFilter.vue
│  ├─ PostList.vue
│  ├─ PostListItem.vue
│  ├─ PostForm.vue
│  └─ PasswordModal.vue
├─ components/map/
│  ├─ LocationMap.vue
│  └─ LocationPopup.vue
├─ components/chat/
│  ├─ ChatWidget.vue
│  ├─ ChatMessage.vue
│  └─ SuggestedQuestions.vue
├─ composables/
│  ├─ usePosts.js
│  └─ useChat.js
├─ config/
│  ├─ categories.js
│  └─ project.js
├─ services/
│  ├─ http.js
│  ├─ posts.js
│  ├─ locations.js
│  └─ chat.js
├─ styles/
│  ├─ tokens.css
│  ├─ reset.css
│  └─ global.css
└─ views/
   ├─ HomeView.vue
   ├─ PostListView.vue
   ├─ PostDetailView.vue
   ├─ PostFormView.vue
   ├─ MapView.vue
   └─ NotFoundView.vue
```

## Data flow

```text
View
→ composable or service
→ shared Axios client
→ FastAPI
→ normalized result
→ component props
```

## State rules

- Route query is the source of truth for board filters and page.
- Form state stays local to the form.
- Chat history may use sessionStorage.
- Do not store post passwords.
- Do not duplicate server data across unrelated global stores.

## Mock strategy

Use mock mode only for parallel frontend development.

```env
VITE_USE_MOCK=true
```

Service modules must expose the same interface in mock and real modes. Components must not know which mode is active.

## CSS rules

- Import tokens globally.
- Use component-scoped CSS.
- Avoid inline style except dynamic map sizing or unavoidable calculated values.
- No raw color literals outside `tokens.css`.
- No arbitrary z-index values; use tokens.
