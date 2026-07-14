# 07. API Contract

## Base configuration

Frontend environment variable:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK=false
```

All calls must use the shared Axios client in `src/services/http.js`.

## Common response assumptions

- JSON content type
- Dates are ISO 8601 strings
- Post passwords are never included in responses

### Common error format

```json
{
  "detail": "Human-readable error message",
  "code": "OPTIONAL_MACHINE_CODE",
  "field_errors": {
    "title": "제목을 입력해 주세요."
  }
}
```

The frontend must gracefully support FastAPI's default `detail` response even if `code` and `field_errors` are absent.

## Post model

```json
{
  "id": 101,
  "category": "festival",
  "title": "이번 주말 축제 정보",
  "content": "축제 위치와 운영 시간을 공유합니다.",
  "created_at": "2026-07-14T15:20:00+09:00",
  "updated_at": "2026-07-14T15:20:00+09:00"
}
```

Allowed category values must come from configuration or backend data. Suggested initial values:

```json
[
  {"value": "attraction", "label": "관광지"},
  {"value": "restaurant", "label": "맛집"},
  {"value": "festival", "label": "축제·행사"},
  {"value": "general", "label": "자유게시판"}
]
```

## GET `/api/posts`

Query:

| Name | Type | Default |
|---|---|---|
| `page` | integer | 1 |
| `size` | integer | 10 |
| `keyword` | string | empty |
| `category` | string | empty |

Response:

```json
{
  "items": [],
  "page": 1,
  "size": 10,
  "total": 0,
  "total_pages": 0
}
```

## GET `/api/posts/{id}`

Response: Post model.

Errors:

- 404: post not found

## POST `/api/posts`

Request:

```json
{
  "category": "festival",
  "title": "이번 주말 축제 정보",
  "content": "내용",
  "password": "1234"
}
```

Response:

- 201 with created Post model

## PUT `/api/posts/{id}`

Request:

```json
{
  "category": "festival",
  "title": "수정 제목",
  "content": "수정 내용",
  "password": "1234"
}
```

Response: updated Post model.

Errors:

- 403 wrong password
- 404 not found
- 422 validation

## DELETE `/api/posts/{id}`

Preferred request:

```json
{
  "password": "1234"
}
```

Response:

```json
{
  "message": "Post deleted"
}
```

If the backend cannot accept a DELETE body, agree on one alternative before implementation:

- `POST /api/posts/{id}/delete`
- password query parameter is not recommended

## GET `/api/locations`

Query:

- `category` optional

Response:

```json
{
  "items": [
    {
      "id": "loc-001",
      "name": "지역 명소",
      "category": "attraction",
      "address": "주소",
      "latitude": 37.5665,
      "longitude": 126.978,
      "description": "짧은 설명"
    }
  ],
  "total": 1
}
```

## POST `/api/chat`

Request:

```json
{
  "message": "주말에 갈 만한 축제를 추천해줘",
  "history": [
    {
      "role": "user",
      "content": "이 지역 관광지를 알려줘"
    },
    {
      "role": "assistant",
      "content": "추천 결과입니다."
    }
  ]
}
```

Response:

```json
{
  "answer": "제공 데이터에 따르면...",
  "sources": [
    {
      "type": "festival",
      "id": "festival-001",
      "label": "축제명"
    }
  ]
}
```

The UI must work when `sources` is absent.

## GET `/api/health`

Response:

```json
{
  "status": "ok"
}
```
