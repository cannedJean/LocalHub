# LocalHub Frontend

대전·충청권 지역정보 + 익명 커뮤니티 서비스의 프론트엔드입니다. **Vue 3 (Composition API, `<script setup>`)
+ Vite + Vue Router 4 + Pinia** 기반 SPA이며, FastAPI 백엔드와 REST로 통신합니다.

## 기술 스택

- Vue 3 (`<script setup>`) / Vite
- Vue Router 4 (history mode) / Pinia
- Axios (단일 API 클라이언트, `VITE_API_BASE_URL` 사용)
- Leaflet + OpenStreetMap (지도)
- Tailwind CSS (디자인 토큰 기반)

## 사전 준비

- Node.js 18+ / npm

## 실행 방법

```bash
npm install
cp .env.example .env   # Windows: copy .env.example .env
# .env 에서 VITE_API_BASE_URL 을 백엔드 주소로 설정 (기본: http://localhost:8000)
npm run dev            # 개발 서버 (http://127.0.0.1:5173)
npm run build          # 프로덕션 빌드 (dist/)
npm run preview        # 빌드 결과 미리보기
```

## 환경 변수

| 변수 | 설명 | 예시 |
|---|---|---|
| `VITE_API_BASE_URL` | 백엔드(FastAPI) 베이스 URL. `/api` 는 클라이언트가 자동으로 붙임 | `http://localhost:8000` |

- 프론트엔드에는 **이 변수 하나만** 사용합니다. OpenAI·날씨 API 키 등 민감정보는 절대 프론트에 두지 않습니다.
- 실제 `.env` 는 커밋하지 않습니다(`.gitignore` 등록). 값 없이 변수명만 담은 `.env.example` 만 커밋합니다.

## 화면 / 라우트

| 경로 | 화면 |
|---|---|
| `/` | 홈 (히어로·검색, 카테고리, 추천 장소, 최근 게시글) |
| `/places` | 지역정보 목록 + 지도 (검색·유형·지역 필터) |
| `/map` | 지도 우선 뷰 (`/places` 와 동일 컴포넌트) |
| `/boards` | 커뮤니티 게시판 목록 (검색·카테고리·페이지네이션, URL 쿼리 동기화) |
| `/boards/new` | 글 작성 |
| `/boards/:id` | 게시글 상세 (수정·삭제 시 비밀번호 확인 모달) |
| `/boards/:id/edit` | 게시글 수정 (비밀번호 필요) |
| `/sources` | 데이터 출처 및 라이선스 |
| `*` | 404 |
| 전역 | 챗봇 위젯 (PC 플로팅 / 모바일 전체화면) |

## 백엔드 API 계약

클라이언트는 `${VITE_API_BASE_URL}/api` 경로만 호출합니다.

```
GET    /api/health
GET    /api/posts?page=&size=&keyword=&category=
GET    /api/posts/{id}
POST   /api/posts              { category, title, content, password }
PUT    /api/posts/{id}         { category, title, content, password }
DELETE /api/posts/{id}         { password }
GET    /api/location-types
GET    /api/locations?type_id=&keyword=&city=&page=&size=
GET    /api/locations/{contentid}
GET    /api/weather?city=daejeon
POST   /api/chat               { message, history }
```

- 게시글 카테고리 값(단일 소스): `tour` / `food` / `festival` / `free` (관광지/맛집/축제/자유게시판).
- 비밀번호는 평문으로 전송하며 응답/로그에 포함하지 않습니다(교육용 의도). 오답 시 `403`, 없는 글 `404`, 검증 오류 `422`.

## 배포 (Netlify)

- `netlify.toml` + `public/_redirects` 에 SPA fallback(`/* → /index.html 200`)이 포함되어 새로고침/딥링크가 동작합니다.
- Netlify 빌드 설정: Build command `npm run build`, Publish directory `dist`.
- 배포 환경 변수에 `VITE_API_BASE_URL` (Render 백엔드 URL)을 설정합니다.

## 데이터 출처

이 서비스는 한국관광공사 TourAPI 4.0 국문 관광정보 데이터를 활용하였습니다.
출처: 한국관광공사 | 라이선스: 공공누리 제3유형 (출처표시-변경금지)
