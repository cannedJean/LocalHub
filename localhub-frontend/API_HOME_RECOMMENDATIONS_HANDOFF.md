# LocalHub 홈 추천 장소 API 연동 확인 및 백엔드 전달사항

홈 화면 코드를 기준으로 추천 장소 API 호출 방식, 응답 처리 구조, 데이터가 표시되지 않는 원인과 백엔드 전달사항을 정리합니다.

## 1. 어떤 API를 호출하는가

`HomeView.vue`의 `loadLocations()`가 `fetchLocations({ size: 3 })`를 호출합니다.

```js
// localhub-frontend/src/views/HomeView.vue:24
async function loadLocations() {
  loadingLoc.value = true
  errorLoc.value = false
  try {
    const data = await fetchLocations({ size: 3 })
    locations.value = normalizePage(data, normalizeLocation).items
  } catch {
    errorLoc.value = true
  } finally {
    loadingLoc.value = false
  }
}
```

`fetchLocations`는 다음과 같이 정의되어 있습니다.

```js
// localhub-frontend/src/api/locations.js:7
export function fetchLocations(params = {}) {
  return apiClient.get('/locations', { params }).then((res) => res.data)
}
```

API 클라이언트의 `baseURL`은 `${VITE_API_BASE_URL}/api`입니다.

```js
// localhub-frontend/src/api/client.js:7
const apiClient = axios.create({
  baseURL: `${apiBaseUrl}/api`,
  headers: { 'Content-Type': 'application/json' },
  timeout: 12_000,
})
```

따라서 프론트엔드가 실제로 호출하는 주소는 다음과 같습니다.

```text
GET {VITE_API_BASE_URL}/api/locations?size=3
```

로컬 환경의 예시는 다음과 같습니다.

```text
http://localhost:8000/api/locations?size=3
```

그러나 백엔드 실제 경로는 `/api/v1/tourism/locations`이므로 프론트엔드 호출 경로와 일치하지 않습니다.

## 2. `response.data`와 `response.data.items` 중 무엇을 사용하는가

최종적으로 사용하는 값은 **`response.data.items`**입니다.

처리 순서는 다음과 같습니다.

1. `fetchLocations()`가 Axios 응답의 `res.data`, 즉 HTTP 응답 본문을 반환합니다.
2. `HomeView.vue`가 그 응답 본문을 `normalizePage()`에 전달합니다.
3. `normalizePage()`가 응답 봉투의 `items` 또는 호환 가능한 대체 필드를 읽습니다.

```js
// localhub-frontend/src/utils/normalizers.js:38
export function normalizePage(payload = {}, mapper = (value) => value) {
  const envelope = payload?.data ?? payload
  const sourceItems = Array.isArray(envelope)
    ? envelope
    : (envelope?.items ?? envelope?.results ?? [])

  const items = sourceItems.map(mapper)
```

즉 정상적인 응답 계약에서는 다음과 같은 봉투 형태를 기대합니다.

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "size": 3,
  "totalPages": 1
}
```

`response.data`가 배열로 반환되는 경우에도 폴백 처리가 가능하지만, 정상 계약은 `{ items, total, page, size, totalPages }` 형태입니다. 백엔드 `/tourism/locations`가 반환하는 해당 구조와 응답 필드 자체는 일치합니다.

## 3. 추천 장소가 표시되지 않는 이유

추천 장소 기능은 더미 데이터나 미구현 상태가 아닙니다. 프론트엔드 코드는 실제 API를 호출하도록 구현되어 있으며, 현재 추천 장소가 표시되지 않는 것은 요청이 실패하기 때문입니다.

### 3.1 경로 불일치 — 핵심 원인

- 프론트엔드 요청: `/api/locations`
- 백엔드 실제 경로: `/api/v1/tourism/locations`

두 경로가 달라 현재 요청은 `404 Not Found`가 발생할 수 있습니다.

### 3.2 `.env` 또는 API 기준 주소 설정

`VITE_API_BASE_URL`이 올바르게 설정되어 있는지 확인해야 합니다. 로컬 개발 환경의 기준값은 다음과 같습니다.

```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

환경변수 설정과 실제 실행 중인 백엔드 주소가 다르면, API 경로를 맞춰도 요청에 실패합니다.

### 3.3 CORS 설정

백엔드에 `CORSMiddleware`가 설정되어 있지 않으면 브라우저에서 프론트엔드 개발 서버와 백엔드 간 요청이 차단될 수 있습니다.

- 프론트엔드 개발 서버 예시: `http://localhost:5173`
- 백엔드 서버 예시: `http://localhost:8000`

백엔드는 최소한 로컬 개발 프론트엔드 origin을 허용해야 하며, 배포 시에는 실제 Netlify origin도 허용해야 합니다.

## 4. 요청 실패 시 프론트엔드 동작

API 호출이 실패하면 `loadLocations()`의 `catch`에서 다음 상태가 설정됩니다.

```js
errorLoc.value = true
```

그 결과 홈 화면은 빈 데이터 상태가 아니라 **에러 및 다시 시도 UI**를 표시합니다.

## 5. 백엔드 담당자에게 전달할 요약

- 홈 화면의 `추천 장소` 영역은 **`GET /api/locations?size=3`**을 호출합니다.
- API 기준 주소는 **`VITE_API_BASE_URL + /api`**입니다.
- 프론트엔드는 최종적으로 **`response.data.items`**를 사용합니다.
- 기대하는 응답 봉투는 **`{ items, total, page, size, totalPages }`**입니다.
- `items`의 각 요소는 다음 원본 TourAPI 필드를 사용합니다.
  - `contentid`
  - `contenttypeid`
  - `title`
  - `addr1`
  - `addr2`
  - `tel`
  - `mapx`
  - `mapy`
  - `firstimage`
- 현재 추천 장소가 표시되지 않는 직접적인 원인은 **프론트엔드 `/api/locations`와 백엔드 `/api/v1/tourism/locations`의 경로 차이**입니다.
- 추가로 다음 항목도 확인해야 합니다.
  - 프론트엔드 개발 서버 `http://localhost:5173`에 대한 CORS 허용
  - 배포된 Netlify origin에 대한 CORS 허용
  - `VITE_API_BASE_URL`과 실제 백엔드 주소 일치
  - 게시글, 챗봇, 날씨 API의 경로와 응답 필드 정합성

## 6. 경로 정합 방안

다음 세 가지 방안 중 하나를 선택해야 합니다.

### 방안 1. 백엔드 경로를 프론트엔드 계약에 맞춤

백엔드가 다음 경로를 제공하도록 통일합니다.

```text
GET /api/locations
```

LocalHub의 기존 프론트엔드 API 계약과 다른 게시글·날씨·챗봇 경로를 함께 유지하기 가장 쉬운 방안입니다.

### 방안 2. 프론트엔드의 장소 API 경로만 백엔드에 맞춤

프론트엔드 장소 API 호출을 다음 백엔드 경로에 맞게 수정합니다.

```text
GET /api/v1/tourism/locations
```

단, 장소 API에만 별도 prefix가 생기므로 게시글·챗봇·날씨 API와의 일관성을 확인해야 합니다.

### 방안 3. `VITE_API_BASE_URL`에 장소 API prefix를 포함

예를 들어 다음처럼 설정하고 프론트엔드에서 `/locations`를 유지하는 방안입니다.

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api/v1/tourism
```

하지만 현재 `apiClient`가 환경변수 뒤에 `/api`를 추가하고 있으며, 동일한 클라이언트를 게시글·챗봇·날씨에서도 사용합니다. 따라서 prefix가 서로 엇갈리거나 `/api`가 중복될 수 있어 **권장하지 않습니다**.

## 7. 권장 결론

공통 API 계약 문서인 `API_HANDOFF.md`를 기준으로 백엔드 라우팅을 통일하는 방안을 권장합니다. 특히 장소 API만 맞추고 끝내지 말고 다음 기능도 같은 시점에 함께 검증해야 합니다.

- 게시글 목록·상세·작성·수정·삭제
- 비밀번호 오류 `403`
- 리소스 없음 `404`
- 입력값 검증 `422`
- 날씨 조회
- 챗봇 요청과 응답 source 구조
- 프론트엔드 개발 및 Netlify 배포 origin에 대한 CORS

프론트엔드와 백엔드가 합의해야 하는 최종 장소 API 예시는 다음과 같습니다.

```http
GET /api/locations?type_id=&keyword=&city=&page=&size=
```

```json
{
  "items": [
    {
      "contentid": "string",
      "contenttypeid": "12",
      "title": "장소명",
      "addr1": "주소",
      "addr2": "상세 주소",
      "tel": "전화번호",
      "mapx": "127.0000",
      "mapy": "36.0000",
      "firstimage": "https://example.com/image.jpg",
      "firstimage2": "https://example.com/thumbnail.jpg"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 3,
  "totalPages": 1
}
```

