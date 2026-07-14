# 10. Acceptance Criteria

## Definition of Done

A frontend task is complete only when:

- It matches the approved Figma frame at desktop and mobile widths.
- It uses existing tokens and components.
- It uses the documented API service layer.
- Loading, empty and error states are present.
- Keyboard navigation is usable.
- No secrets or passwords are logged or persisted.
- The browser console has no avoidable errors.
- The implementation works after a production build.
- Changed behavior is documented in the completion report.

## Page acceptance tests

### Home

- [ ] Region name is loaded from project configuration.
- [ ] Recent posts load or show appropriate state.
- [ ] Map and board CTAs navigate correctly.
- [ ] Chat button is visible and operable.

### Board list

- [ ] Page loads posts from `/api/posts`.
- [ ] Keyword and category are reflected in the URL.
- [ ] Clear filters restores default results.
- [ ] Pagination works.
- [ ] Mobile list remains readable at 360px.
- [ ] Empty and error states work.

### Post creation

- [ ] Required fields block invalid submit.
- [ ] Successful submit navigates to detail.
- [ ] Double submission is prevented.
- [ ] Password is never shown after submit.

### Post detail/edit/delete

- [ ] 404 is handled.
- [ ] Wrong password shows inline modal feedback.
- [ ] Correct edit updates the view.
- [ ] Correct delete returns to list.
- [ ] Delete requires an explicit destructive confirmation.

### Map

- [ ] Markers use valid coordinates only.
- [ ] Category filtering updates visible markers.
- [ ] Popups include name and address.
- [ ] Attribution is visible.
- [ ] Map cleans up on route leave.

### Chatbot

- [ ] Desktop opens as a floating panel.
- [ ] Mobile opens full-screen.
- [ ] Send is disabled for blank input and while waiting.
- [ ] User and assistant messages are visually distinct.
- [ ] Error state offers retry.
- [ ] Current-session history survives route changes.
- [ ] Message HTML is not injected unsafely.

## Build checks

```bash
npm run build
npm run dev
```

Recommended if test tools are available:

```bash
npm run lint
npm run test
```
