# 06. Component Specification

## Component hierarchy

```text
App
├─ AppHeader
├─ RouterView
├─ AppFooter
├─ ChatWidget
└─ ToastRegion
```

## UI primitives

### BaseButton

Props:

```js
{
  variant: "primary" | "secondary" | "ghost" | "danger",
  size: "sm" | "md" | "lg",
  disabled: Boolean,
  loading: Boolean,
  type: "button" | "submit"
}
```

Requirements:

- Preserve label width when loading where possible.
- Set `aria-busy` during loading.
- Disabled styles must remain readable.

### BaseInput / BaseTextarea / BaseSelect

Common props:

```js
{
  id: String,
  label: String,
  modelValue: String,
  required: Boolean,
  error: String,
  hint: String,
  disabled: Boolean
}
```

### BaseModal

- Teleport to body
- Focus trap
- Escape close
- Restore focus to trigger
- Header, body and footer slots

### Status components

- `LoadingSkeleton`
- `EmptyState`
- `ErrorState`
- `ToastMessage`

## Domain components

### AppHeader

- Desktop navigation and mobile menu
- Active route indication
- No authentication controls

### RegionHero

Props:

```js
{
  regionName: String,
  description: String
}
```

### CategoryFilter

```js
{
  categories: Array,
  modelValue: String,
  allLabel: String
}
```

Emits `update:modelValue`.

### PostList

Props:

```js
{
  posts: Array,
  loading: Boolean
}
```

Desktop and mobile presentation may differ, but data and action semantics stay identical.

### PostForm

Props:

```js
{
  mode: "create" | "edit",
  initialValue: Object,
  submitting: Boolean,
  serverError: String
}
```

Emits `submit` and `cancel`.

### PasswordModal

Props:

```js
{
  open: Boolean,
  action: "edit" | "delete",
  loading: Boolean,
  error: String
}
```

Never log or persist password values.

### LocationMap

Props:

```js
{
  locations: Array,
  selectedCategory: String,
  loading: Boolean,
  error: String
}
```

- Initialize Leaflet once.
- Update marker layer rather than recreating map.
- Clean map instance on unmount.
- Include tile attribution.

### ChatWidget

Internal states:

```text
closed
open-idle
open-sending
open-error
```

Session history item:

```js
{
  id: String,
  role: "user" | "assistant" | "error",
  content: String,
  createdAt: String
}
```

Do not use `v-html` for chatbot content unless content is sanitized.
