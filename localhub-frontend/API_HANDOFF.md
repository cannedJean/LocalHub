# LocalHub 관광 API 연동 문서 (프론트 → 백엔드 전달용)

프론트엔드(Vue 3)에서 관광 정보(TourAPI 4.0 기반) API를 호출하는 코드와, 응답을 사용하는 컴포넌트를 정리한 문서입니다. 백엔드는 아래 필드명과 응답 형식에 맞춰 API를 구현해 주시면 프론트 수정 없이 바로 연동됩니다.

---

## 1. 호출 베이스 설정

`.env`의 `VITE_API_BASE_URL` + `/api` 가 baseURL이 됩니다. (기본값 `http://localhost:8000`)

```js
// src/api/client.js
import axios from 'axios'

const apiBaseUrl = String(import.meta.env.VITE_API_BASE_URL ?? '')
  .trim()
  .replace(/\/+$/, '')

const apiClient = axios.create({
  baseURL: `${apiBaseUrl}/api`,
  headers: { 'Content-Type': 'application/json' },
  timeout: 12_000,
})

export function getApiStatus(error) {
  return error?.response?.status ?? 0
}

export function getApiDetail(error, fallback = '요청을 처리하지 못했습니다.') {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((item) => item?.msg).filter(Boolean).join(' ') || fallback
  }
  return error?.response?.data?.message || fallback
}

// FastAPI 422 검증 오류({ detail: [{ loc, msg }] })를 필드별 메시지로 변환
export function getValidationErrors(error) {
  const detail = error?.response?.data?.detail
  if (!Array.isArray(detail)) return {}
  return detail.reduce((errors, issue) => {
    const field = issue?.loc?.at(-1)
    if (typeof field === 'string' && typeof issue?.msg === 'string') {
      errors[field] = issue.msg
    }
    return errors
  }, {})
}

export default apiClient
```

---

## 2. 관광 API 호출 함수 (axios)

```js
// src/api/locations.js
import apiClient from './client'

export function fetchLocationTypes() {
  return apiClient.get('/location-types').then((res) => res.data)
}

export function fetchLocations(params = {}) {
  return apiClient.get('/locations', { params }).then((res) => res.data)
}

export function fetchLocation(contentId) {
  return apiClient.get(`/locations/${contentId}`).then((res) => res.data)
}
```

### 요청 엔드포인트 명세

| 함수 | 메서드 | 경로 | 쿼리 파라미터 |
|---|---|---|---|
| `fetchLocationTypes` | GET | `/api/location-types` | 없음 |
| `fetchLocations` | GET | `/api/locations` | `page`, `size`, `keyword`, `type_id`, `city` |
| `fetchLocation` | GET | `/api/locations/{contentId}` | 없음 |

**`/api/locations` 쿼리 파라미터 상세:**

| 파라미터 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `page` | number | X (기본 1) | 페이지 번호 |
| `size` | number | X | 페이지당 개수 |
| `keyword` | string | X | 장소명/주소 검색어 |
| `type_id` | string | X | `contenttypeid` 값 (아래 표 참고) |
| `city` | string | X | 지역 id (`daejeon`/`sejong`/`gyeryong`/`gongju`/`nonsan`/`okcheon`) |

---

## 3. `item.xxx` 정규화 로직 (백엔드 응답 필드 매핑)

프론트는 아래 함수로 API 원본 응답을 화면에서 쓰는 형태로 변환합니다. **여기 나오는 `source.xxx`가 백엔드가 응답에 넣어야 하는 실제 필드명**입니다.

```js
// src/utils/normalizers.js
const FALLBACK_TYPE = { label: '기타', emoji: '📍' }

// mapx(경도)/mapy(위도)는 문자열로 와도 됩니다. 프론트에서 float 변환 및 범위 검증 처리.
function parseCoordinate(value, min, max) {
  if (value === '' || value === null || value === undefined) return null
  const parsed = Number.parseFloat(value)
  return Number.isFinite(parsed) && parsed >= min && parsed <= max ? parsed : null
}

export function normalizeLocation(source = {}, index = 0) {
  const contentId = String(source.contentid ?? '')
  const typeId = String(source.contenttypeid ?? '')
  const type = LOCATION_TYPE_MAP.get(typeId) ?? FALLBACK_TYPE
  const latitude = parseCoordinate(source.mapy, -90, 90)
  const longitude = parseCoordinate(source.mapx, -180, 180)
  const image = String(source.firstimage || source.firstimage2 || '').replace(/^http:/, 'https:')

  return {
    contentId,
    typeId,
    typeLabel: type.label,
    emoji: type.emoji,
    title: source.title || '이름 없는 장소',
    address: [source.addr1, source.addr2].filter(Boolean).join(' ') || '주소 정보 없음',
    telephone: source.tel || '',
    image,
    latitude,
    longitude,
    hasValidCoordinates: latitude !== null && longitude !== null,
    tintIndex: index % 4,
  }
}

// 여러 페이지네이션 응답 형태를 허용하고 일관된 구조로 변환
export function normalizePage(payload = {}, mapper = (value) => value) {
  const envelope = payload?.data ?? payload
  const sourceItems = Array.isArray(envelope)
    ? envelope
    : (envelope?.items ?? envelope?.results ?? [])
  const items = sourceItems.map(mapper)

  return {
    items,
    total: Number(envelope?.total ?? envelope?.pagination?.total_items ?? items.length),
    page: Number(envelope?.page ?? envelope?.pagination?.page ?? 1),
    size: Number(envelope?.size ?? items.length),
    totalPages: Number(
      envelope?.totalPages ?? envelope?.total_pages ?? envelope?.pagination?.total_pages ?? 1,
    ),
  }
}
```

### 백엔드 응답에 필요한 필드 (TourAPI 원본 필드명 그대로 사용)

| 필드명 | 설명 | 타입 | 비고 |
|---|---|---|---|
| `contentid` | 콘텐츠 ID | string | |
| `contenttypeid` | 콘텐츠 유형 ID | string | 아래 유형표 참고 |
| `title` | 장소명 | string | 없으면 프론트가 "이름 없는 장소" 표시 |
| `addr1` | 주소(기본) | string | |
| `addr2` | 주소(상세) | string | 없어도 됨 |
| `tel` | 전화번호 | string | 없어도 됨 |
| `mapx` | 경도 (longitude) | string | **문자열 허용**, -180~180 벗어나면 프론트가 무시 |
| `mapy` | 위도 (latitude) | string | **문자열 허용**, -90~90 벗어나면 프론트가 무시 |
| `firstimage` | 대표 이미지 URL | string | 없으면 `firstimage2` 사용, 둘 다 없으면 이모지로 대체 표시 |
| `firstimage2` | 대체 이미지 URL | string | `firstimage` 없을 때 사용 |

### `contenttypeid` 값 목록 (프론트에 하드코딩된 유형)

| id | 라벨 | 비고 |
|---|---|---|
| `12` | 관광지 | |
| `14` | 문화시설 | |
| `15` | 축제·공연 | |
| `25` | 여행코스 | |
| `28` | 레포츠 | |
| `32` | 숙박 | 지역정보 필터 화면에서는 제외(홈 바로가기에도 없음) |
| `38` | 쇼핑 | |
| `39` | 음식점 | |

---

## 4. 컴포넌트에서 `item.xxx` 사용 (정규화 이후 필드 — 백엔드는 신경 쓸 필요 없음)

`PlacesView.vue`, `HomeView.vue`에서는 위 `normalizeLocation()` 결과를 사용합니다. 즉 원본 API 필드가 아니라 변환된 필드(`contentId`, `typeLabel`, `emoji`, `title`, `address`, `telephone`, `image`, `latitude`, `longitude`, `hasValidCoordinates`, `typeId`)입니다.

```js
// src/views/PlacesView.vue (데이터 요청 부분)
async function loadData() {
  loading.value = true
  error.value = false
  try {
    const params = { page: page.value, size: 20 }
    if (filterKeyword.value) params.keyword = filterKeyword.value
    if (filterType.value) params.type_id = filterType.value
    if (filterCity.value) params.city = filterCity.value

    const data = await fetchLocations(params)
    const normalized = normalizePage(data, normalizeLocation)
    items.value = normalized.items
    totalItems.value = normalized.total
    totalPages.value = normalized.totalPages
    selected.value = null
    renderMarkers()
  } catch {
    error.value = true
    items.value = []
    if (markersGroup) markersGroup.clearLayers()
  } finally {
    loading.value = false
  }
}
```

```vue
<!-- src/views/PlacesView.vue (템플릿에서 item.xxx 사용 부분) -->
<button v-for="item in items" :key="item.contentId" @click="selectItem(item)">
  <ImagePlaceholder :src="item.image" :emoji="item.emoji" :tint-index="item.tintIndex" />
  <div class="font-bold">{{ item.title }}</div>
  <div>{{ item.typeLabel }} · 📍 {{ item.address }}</div>
</button>
```

```js
// src/views/HomeView.vue (데이터 요청 부분)
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

```vue
<!-- src/views/HomeView.vue (템플릿에서 loc.xxx 사용 부분) -->
<button v-for="loc in locations" :key="loc.contentId" @click="...">
  <ImagePlaceholder :src="loc.image" :emoji="loc.emoji" :tint-index="loc.tintIndex" />
  <div>{{ loc.typeLabel }} · {{ loc.title }}</div>
  <div>📍 {{ loc.address }}</div>
</button>
```

지도 마커/팝업(`PlacesView.vue`)에서도 동일한 정규화된 필드를 사용합니다:

```js
// src/views/PlacesView.vue (지도 마커 렌더링)
items.value.forEach((item) => {
  if (!item.hasValidCoordinates) return
  const marker = L.marker([item.latitude, item.longitude]).addTo(markersGroup)
  marker.bindPopup(() => buildSafePopup(item)) // item.image, item.title, item.typeLabel, item.typeId, item.address, item.telephone 사용
})
```

---

## 5. 권장 응답 형식 예시

### `GET /api/locations?page=1&size=20`

```json
{
  "items": [
    {
      "contentid": "126508",
      "contenttypeid": "39",
      "title": "성심당 본점",
      "addr1": "대전광역시 중구 대종로480번길 15",
      "addr2": "",
      "tel": "042-256-4114",
      "mapx": "127.429306",
      "mapy": "36.328735",
      "firstimage": "http://tong.visitkorea.or.kr/cms/resource/.../image.jpg",
      "firstimage2": ""
    }
  ],
  "total": 516,
  "page": 1,
  "size": 20,
  "totalPages": 26
}
```

- 최상위에 `items`/`total`/`page`/`size`/`totalPages`를 두는 것을 권장합니다.
- (호환용) `pagination: { total_items, page, total_pages }` 래핑 구조도 프론트에서 자동으로 인식하지만, 최상위 평탄 구조가 더 단순합니다.

### `GET /api/locations/{contentId}` (단건)

동일한 필드 구조를 단일 객체로 반환 (`items` 래핑 없이):

```json
{
  "contentid": "126508",
  "contenttypeid": "39",
  "title": "성심당 본점",
  "addr1": "대전광역시 중구 대종로480번길 15",
  "addr2": "",
  "tel": "042-256-4114",
  "mapx": "127.429306",
  "mapy": "36.328735",
  "firstimage": "http://tong.visitkorea.or.kr/.../image.jpg"
}
```

---

## 6. 백엔드에 꼭 전달할 핵심 사항 (요약)

1. **필드명은 TourAPI 원본 그대로** 써주세요: `contentid`, `contenttypeid`, `addr1`, `addr2`, `tel`, `mapx`, `mapy`, `firstimage`, `firstimage2`. 필드명이 다르면 프론트가 데이터를 못 읽습니다.
2. **`mapx`/`mapy`는 문자열이어도 됩니다** — 프론트가 `parseFloat` + 범위 검증(-180~180, -90~90) 후 사용합니다. 유효하지 않으면 해당 장소는 지도에서 자동 제외됩니다.
3. **페이지네이션은 최상위에 `items`/`total`/`page`/`size`/`totalPages`** 형태를 권장합니다.
4. `firstimage`/`firstimage2`가 둘 다 빈 문자열이어도 괜찮습니다 — 프론트가 이모지로 대체 표시합니다.
5. `/api/locations` 쿼리 파라미터명: `page`, `size`, `keyword`, `type_id`, `city` (정확한 이름으로 받아주세요).
