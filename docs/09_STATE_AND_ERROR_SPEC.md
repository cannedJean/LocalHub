# 09. State and Error Specification

## Global async states

Every API-backed area supports:

```text
idle → loading → success
              ↘ error
```

## Error mapping

| HTTP/status | User message | UI behavior |
|---|---|---|
| Network/timeout | 서버에 연결할 수 없습니다 | Retry action |
| 400 | 요청 내용을 확인해 주세요 | General or field feedback |
| 403 | 비밀번호가 일치하지 않습니다 | Keep password modal open |
| 404 | 요청한 정보를 찾을 수 없습니다 | Not-found state |
| 422 | 입력값을 확인해 주세요 | Map field errors |
| 500+ | 잠시 후 다시 시도해 주세요 | Retry, preserve user input |

## Form validation

### Post title

- Required
- Trim whitespace
- Suggested maximum: 100 characters unless backend defines another limit

### Content

- Required
- Trim for required check but preserve line breaks

### Password

- Required
- Do not display saved password
- Do not persist in localStorage/sessionStorage
- Clear after successful request

## Toast usage

Use toast for:

- Post created
- Post updated
- Post deleted
- Recoverable background error

Do not rely on toast alone for field errors.

## Empty states

| Context | Message |
|---|---|
| No posts | 아직 등록된 게시글이 없습니다 |
| No search result | 검색 조건에 맞는 게시글이 없습니다 |
| No locations | 표시할 지역 정보가 없습니다 |
| Chat empty | 지역 정보가 궁금한가요? 질문을 입력해 주세요 |
