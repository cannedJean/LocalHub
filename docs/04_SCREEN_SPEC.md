# 04. Screen Specification

## Global layout

- Desktop content max width: 1200px
- Header height: 64px
- Main horizontal padding: 24px desktop, 16px mobile
- Minimum supported viewport: 360px
- Main background: `--color-bg-page`
- Focus ring must be visible for keyboard navigation

## Home

### Sections

1. Header
2. Region hero
3. Category shortcuts
4. Recent posts
5. Local map preview or map CTA
6. Footer
7. Floating chatbot

### Region hero content

- Eyebrow: `공공데이터 기반 지역 정보`
- Title: `[TARGET_REGION]을 더 가깝게, LocalHub`
- Description: 지역 정보 탐색과 익명 커뮤니티의 결합
- Primary CTA: `지역 정보 지도 보기`
- Secondary CTA: `커뮤니티 둘러보기`

### Recent post state

- Loading: 4 skeleton rows/cards
- Empty: `아직 등록된 게시글이 없습니다`
- Error: retry panel

## Board list

### Controls

- Search field with submit and clear actions
- Category chips/select
- Write button
- Result count
- Desktop table or card list
- Mobile stacked cards
- Pagination

### URL query synchronization

```text
/boards?keyword=축제&category=festival&page=1
```

Back/forward browser navigation must restore filter state.

## Post detail

- Breadcrumb
- Category badge
- Title
- Created/updated dates
- Body preserving line breaks
- Edit button
- Delete button
- Password modal
- Back to list

## Post form

- Create title: `새 글 작성`
- Edit title: `게시글 수정`
- Inputs:
  - category
  - title
  - content
  - password
- Buttons:
  - cancel
  - submit
- Prevent duplicate submit.
- Warn before leaving when the form is dirty.

## Map

- Page title and short guidance
- Category filter controls
- Map area:
  - 560px desktop height
  - minimum 420px mobile height
- Marker popup:
  - place name
  - category
  - address
  - optional short description
- Location count
- Empty/error overlay inside map container

## Chatbot

### Closed state

- Fixed floating button
- Accessible label: `LocalHub 챗봇 열기`

### Desktop open state

- Width: 360–400px
- Height: min(640px, viewport minus margins)
- Header, history, suggested prompts, composer
- Close and reset controls

### Mobile open state

- Full viewport fixed layer
- Respect safe areas
- Composer remains visible with virtual keyboard
