# 03. User Flows

## Flow A: Browse and search posts

```text
Home
→ Community
→ Board list loads
→ User enters keyword or selects category
→ URL query is updated
→ Filtered result appears
→ User opens a post
```

Failure states:

- Network failure → error panel + retry
- No matches → empty search result + clear filters

## Flow B: Create a post

```text
Board list
→ Write
→ Enter category, title, content, password
→ Client validation
→ POST /api/posts
→ Success toast
→ Navigate to new post detail
```

Failure states:

- Validation error → field-level message
- Server error → retain form data and show retry feedback

## Flow C: Edit a post

```text
Post detail
→ Edit
→ Password verification
→ Authorized
→ Edit form populated
→ PUT /api/posts/:id
→ Success toast
→ Return to detail
```

Wrong password:

```text
Password modal
→ 403 response
→ Show "비밀번호가 일치하지 않습니다"
→ Keep modal open and focus password input
```

## Flow D: Delete a post

```text
Post detail
→ Delete
→ Confirmation + password
→ DELETE /api/posts/:id
→ Success
→ Navigate to board list
```

## Flow E: Explore map

```text
Home or navigation
→ Map
→ Fetch locations
→ Render markers
→ Select category
→ Update visible markers
→ Click marker
→ Show place details
```

## Flow F: Ask chatbot

```text
Any main page
→ Open chatbot
→ Select suggested question or type text
→ POST /api/chat
→ Append assistant response
→ Continue conversation
```

Failure:

```text
API timeout/error
→ Append error bubble
→ Show retry action
```
