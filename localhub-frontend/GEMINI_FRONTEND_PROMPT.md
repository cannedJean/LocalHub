# LocalHub Frontend — Master Build Prompt for Gemini

> Paste everything below the line into Gemini as a single prompt. It is self-contained: it
> encodes the RFP constraints, the functional spec (기능명세서), the data/license rules, and the
> exact Figma design system so the model can build the full Vue 3 SPA without further context.

---

## ROLE

You are a senior frontend engineer. Build the **complete production-ready frontend** for **LocalHub**,
an anonymous local-information community web service for the **대전·충청권 (Daejeon/Chungcheong)** region.
Deliver a Vue 3 SPA that exactly matches the design system and screen specs below, wired to a FastAPI
backend via REST. Output real, runnable files (not pseudo-code), with a clear project tree.

---

## 1. HARD CONSTRAINTS (from the RFP — non-negotiable)

1. **Framework:** Vue.js 3 (Composition API, `<script setup>`), **SPA** architecture. Build tool: **Vite**.
2. **Anonymous only:** NO signup, NO login, NO auth/JWT/OAuth, NO user accounts. Never build account UI.
3. **Post edit/delete auth = password only.** On create, the user sets a plaintext edit password.
   Edit/delete is authorized solely by matching that password (verified server-side). The frontend just
   collects the password and sends it; it must **never** display or log stored passwords.
4. **Single region:** 대전·충청권 only. Do NOT build a multi-region switcher. Included cities:
   대전, 세종, 계룡, 공주, 논산, 옥천.
5. **Data source:** All location data comes from the backend (which serves pre-collected TourAPI 4.0 JSON).
   The frontend calls **our backend API only** — never call public/TourAPI or weather APIs directly, and
   never embed any API key in frontend code.
6. **Secrets:** The only frontend env var is `VITE_API_BASE_URL`. No OpenAI/weather keys in the frontend.
   Provide a `.env.example` with just `VITE_API_BASE_URL=http://localhost:8000`. Add `.env` to `.gitignore`.
7. **Deployment target:** Netlify. Must include SPA redirect config so deep links / refresh work
   (e.g. `public/_redirects` with `/*  /index.html  200`, or `netlify.toml`).
8. **Attribution (license):** Every page footer must show the data source & license:
   "출처: 한국관광공사 | 데이터: TourAPI 4.0 국문 관광정보 | 라이선스: 공공누리 제3유형 (출처표시-변경금지)".
9. **Comments feature is OUT of scope** (excluded from this MVP). Do not build comment UI.

> Note: The Figma write-form helper text says "비밀번호는 암호화되어 저장됩니다". This is mockup
> filler and contradicts the spec, which mandates **plaintext** storage for educational purposes. Do NOT
> claim encryption in the UI. Use neutral helper copy: "수정·삭제 시 필요합니다. 4자 이상 입력해 주세요."

---

## 2. TECH STACK & PROJECT SETUP

- **Vue 3 + Vite** (JavaScript is fine; TypeScript optional but keep it simple and consistent).
- **Vue Router 4** for the SPA routes below (history mode).
- **Pinia** for state (chat session state, filters). Chat history persists in `sessionStorage`.
- **Axios** (or fetch wrapper) with a single API client reading `import.meta.env.VITE_API_BASE_URL`.
- **Leaflet** (`leaflet` + OpenStreetMap tiles) for the map (selected optional feature).
- Styling: plain CSS with CSS custom properties (design tokens below) **or** Tailwind — your choice, but
  the tokens/values must match exactly. Font family: **Inter** (load via Google Fonts / `@fontsource`),
  with a Korean fallback stack: `Inter, 'Pretendard', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif`.
- Fully **responsive**: desktop 1440 reference, must work down to 360px mobile.
- Include: loading skeletons/spinners, empty states, and error states with retry everywhere data loads.

Deliverables: `package.json`, `vite.config.js`, `index.html`, `src/` tree, router, api client, stores,
components, views, styles, `.env.example`, `.gitignore`, Netlify redirect config, and a `README.md`
(install / run / build / env / deploy).

---

## 3. DESIGN TOKENS (extracted from Figma — use exactly)

**Colors**
```
--primary:        #2563eb   /* buttons, active nav, links, chat header, user bubble, active chips */
--primary-strong: #1d4ed8   /* emphasis / hover text */
--primary-tint:   #eff6ff   /* weather widget pill bg */
--link-chip-bg:   #eff3fe   /* chat source link chips */
--selected-border:#c6d9fe   /* selected list item / edit button outline */

--text-heading:   #111827
--text-body:      #374151
--text-strong:    #1f2937
--text-muted:     #6b7280
--text-faint:     #9ca3af
--text-nav:       #4a5568   /* inactive nav */

--bg-page:        #f8fafd
--bg-card:        #ffffff
--bg-subtle:      #f3f4f6   /* table header, modal cancel btn */
--bg-chat:        #f6f8fb   /* chat body & input */

--border:         #e5e7eb   /* default card/divider border */
--border-input:   #d9dde5   /* inputs, chips */
--border-list:    #edeff2   /* list-item separators */

/* Category badge / accent colors */
--cat-festival:   #2563eb   /* 축제 */
--cat-food:       #e67316   /* 맛집 */
--cat-tour:       #16a34a   /* 관광지 */
--cat-free:       #6b7280   /* 자유 */

/* Danger (delete) */
--danger:         #dc2626
--danger-bg:      #fff2f2
--danger-border:  #f9b5b5

/* Placeholder image tints (cycle for cards without firstimage) */
--tint-blue:   #e2edff;  --tint-green:  #daf1e7;  --tint-orange: #ffecda;  --tint-purple: #f2e7ff;

/* Hero */
--hero-bg: #2563eb; --hero-eyebrow: #d9e5ff; --hero-subtitle: #e5edff;

/* Footer */
--footer-bg: #111827; --footer-text: #c4c9d1; --footer-faint: #6b7280;
```

**Typography (Inter)** — size / weight:
- Hero title: 44 / 800 (ExtraBold)
- Page title (list/board/write): 26 / 800
- Section title (home sections): 22 / 800
- Detail/card title: 24 / 800
- Modal title: 20 / 700
- Card place name: 17 / 700; list item name: 16 / 700
- Body text: 16 / 400 (line-height ~1.6 for post body)
- Base UI text / nav / buttons: 15 (700 for buttons/active, 500 for inactive)
- Chips / small labels: 14
- Meta / table cells / badges: 13
- Tiny (helper, attribution): 11–12

**Radius:** pills & weather widget = fully rounded (17–24px); cards = 14; modal = 16; chat panel = 16;
inputs = 10; buttons = 8–10; small thumbs = 10.

**Layout:**
- Content container max-width ~1200px, centered, with responsive horizontal padding (24px mobile).
  Wider working pages (지역정보, 게시판) may use up to ~1360px.
- **Header:** sticky, height 72px, white bg, 1px bottom border `--border`. Left: logo `◉ LocalHub`
  (22/800, `--primary`). Center/right: nav links `홈 · 지역정보·지도 · 커뮤니티` (active = `--primary`/700,
  inactive = `--text-nav`/500). Far right: **weather widget pill** (`--primary-tint` bg, rounded 24):
  `☀️ 대전 28°C · 야외활동 추천` (text `--primary-strong`, 14/600). Collapse nav into a menu on mobile.
- **Footer:** dark (`--footer-bg`) with logo + the mandatory attribution lines (see constraint 8).

---

## 4. ROUTES / SCREENS

| Route | Screen | Notes |
|---|---|---|
| `/` | SCR-01 Home | hero + search, category shortcuts, recommended places, recent posts |
| `/places` | SCR-02 지역정보 목록 | JSON-based list, search + category/region filters |
| `/map` | SCR-03 지도 | Leaflet map, markers, filters, popup (often same page/split view as /places) |
| `/boards` | SCR-04 게시판 목록 | table, category chips, search, pagination, 글쓰기 |
| `/boards/new` | SCR-05 글 작성 | title/category/content/password form |
| `/boards/:id` | SCR-06 게시글 상세 | content + 수정/삭제 (password modal) |
| `/boards/:id/edit` | SCR-07 게시글 수정 | pre-filled form, password required |
| `/sources` | SCR-08 데이터 출처 | source & license page |
| `*` | SCR-09 404 | not-found fallback |
| global | SCR-10 챗봇 | floating widget on all pages; fullscreen on mobile |

You may implement `/places` and `/map` as one page with a split view (list 480px + map 860px on desktop)
exactly like the Figma INFO-01 screen, plus a separate `/map` route if convenient.

---

## 5. SCREEN-BY-SCREEN SPEC (matches Figma exactly)

### SCR-01 Home (`/`)
- **Hero** (full-width, `--hero-bg`, ~380px): eyebrow `대전 · 세종 · 충청권` (16/600, `--hero-eyebrow`);
  title `지역의 모든 정보를 한 곳에서, LocalHub` (44/800 white); subtitle
  `관광지 · 맛집 · 축제 정보부터 이웃 주민과의 이야기까지. 회원가입 없이 지금 바로 이용하세요.` (17, `--hero-subtitle`);
  a white rounded search bar (radius 12, ~620px) with placeholder `🔍  지역, 장소, 키워드를 검색해 보세요`
  and a blue `검색` button (radius 8). Submitting navigates to `/places?keyword=...`.
- **카테고리 바로가기** section: 6 cards (bg `#f8fafd`, border, radius 14, ~183×116) each with emoji + label:
  `🏰 관광지 · 🍜 음식점 · 🎉 축제·공연 · 🎨 문화시설 · 🚴 레포츠 · 🛍️ 쇼핑`. Click → `/places?type=<id>`.
- **대전·충청 추천 장소** section: 3 place cards (white, border, radius 14, ~384×250): tinted image area
  (150px) with emoji fallback, then name `유형 · 이름` (17/700) and address `📍 주소` (14, muted).
- **커뮤니티 최근 게시글** section: header with title + `전체보기 ›` link (`--primary`). A rounded list
  (radius 14) of rows: `[카테고리 badge] 제목 ............ YYYY.MM.DD · 조회 N`. Category badge colored by
  type. Rows clickable → `/boards/:id`.
- Footer with full attribution (logo + `본 서비스는 한국관광공사 TourAPI 4.0 ...` + city list + license line).

### SCR-02 / SCR-03 지역정보 & 지도 (`/places`, `/map`)
- Page bg `--bg-page`. Page title `지역정보 찾아보기` (26/800).
- **Filter card** (white, radius 14): search input (radius 10, placeholder
  `🔍  장소명 또는 주소로 검색  (예: 유성, 둘레길, 국밥)`), then **content-type chips**
  `전체 · 관광지 · 음식점 · 문화시설 · 축제·공연 · 여행코스 · 레포츠 · 쇼핑`, then a **지역** row of region chips
  `전체 · 대전 · 세종 · 계룡 · 공주 · 논산 · 옥천`. Active chip = `--primary` fill + white; inactive = white +
  `--border-input` + `--text-nav`.
- **Split view**: left **ListPanel** (480px, radius 14) with header (`검색 결과` + `총 N건 · 대전 기준`) and
  list items (92px tall): rounded tinted thumb (64px, emoji fallback) + name (16/700) + `유형 · 📍 주소` (13,
  muted). Selected item = tint bg `#f3f4f6`/blue accents. Right **MapPanel (MAP-01)** (860px, radius 14):
  real Leaflet map centered on Daejeon/Chungcheong, markers for valid coordinates only, a **selected marker**
  style, a **popup (MAP-05)** card (300px, radius 12): tinted image + name (17/800) + `유형 (contentTypeId N)`
  (13, `--primary`) + `📍 주소 · ☎ 전화`. Map attribution text:
  `Leaflet | © OpenStreetMap contributors · 한국관광공사 TourAPI 4.0`.
- **Data handling rules (MUST):** `mapx`(경도)/`mapy`(위도) come as strings → parse to float; **exclude
  invalid/empty coords from the map** (MAP-06) without crashing. If `firstimage` is empty → use a tinted
  placeholder with a type emoji (INFO-04). Missing address must not break layout. Keep `contentid` as string.

### SCR-04 게시판 목록 (`/boards`)
- Title row: `커뮤니티 게시판` (26/800) + blue `✏️ 글쓰기` button (radius 10) → `/boards/new`.
- Toolbar: category chips `전체 · 관광지 · 맛집 · 축제 · 자유게시판` + right-aligned search input
  (`🔍  제목·내용 검색`).
- **Post table** (radius 14, header bg `--bg-subtle`): columns `번호 | 카테고리 | 제목 | 작성일 | 조회`.
  Rows 60px, category cell colored by type, title in `--text-strong` (clickable → detail).
- **Pagination**: `‹` + numbered pages (active = blue rounded 8) + `›`. Sync `page`, `keyword`, `category`
  to the URL query (POST-02). Wire to `GET /api/posts?page=&size=&keyword=&category=`.
- States: loading skeleton rows, empty ("검색 결과가 없습니다" / "게시글이 없습니다"), error + retry (POST-09).

### SCR-06 게시글 상세 (`/boards/:id`)
- `‹ 목록으로` back link. **DetailCard** (white, border, radius 14, ~780px): category badge, title (24/800),
  divider, meta line `작성일 YYYY.MM.DD HH:mm · 조회 N · 수정됨 ...` (13, faint), body (16, `--text-body`,
  preserve line breaks). **ActionRow** (right): `수정` (outline, `--primary` text, border `--selected-border`)
  and `삭제` (bg `--danger-bg`, border `--danger-border`, text `--danger`).
- Nonexistent id → 404 (POST-04). Clicking 수정/삭제 opens the **Password Confirm modal**.

### Password Confirm Modal (used by 수정 & 삭제)
- Overlay: `#111827` at 55% opacity. **Card** 420px, radius 16: title `비밀번호 확인` (20/700),
  desc `게시글 작성 시 입력한 비밀번호를 입력해 주세요.`, password input (radius 10), buttons
  `취소` (bg `--bg-subtle`, muted text) + `확인` (blue). On 삭제 confirm → `DELETE /api/posts/:id` with password;
  on 수정 confirm → verify then go to `/boards/:id/edit`. Wrong password → `403` → inline error
  "비밀번호가 일치하지 않습니다." (do not close modal).

### SCR-05 / SCR-07 글 작성·수정 (`/boards/new`, `/boards/:id/edit`)
- Page title `새 글 쓰기` (or `글 수정`). **FormCard** (white, border, radius 14, ~780px) with fields
  (input bg `#f8fafd`, border `--border-input`, radius 10, 46px tall):
  - **제목**: text input, placeholder `제목을 입력하세요 (최대 100자)`, max 100 chars.
  - **카테고리**: dropdown, placeholder `카테고리를 선택하세요` — options 관광지 / 맛집 / 축제 / 자유게시판.
  - **내용**: textarea (~160px), placeholder `지역 주민들과 나누고 싶은 이야기를 자유롭게 적어주세요.`
  - **비밀번호 \***: password input, placeholder `••••••`, helper (orange `--cat-food`)
    `⚠ 수정·삭제 시 필요합니다. 4자 이상 입력해 주세요.` (min 4 chars). On edit screen, password is required
    to submit the update.
  - Buttons (right): `취소` (outline) + `등록`/`수정 완료` (blue).
- **Validation (POST-08):** block empty title/content/password; show per-field error messages. Invalid →
  surface backend `422` messages. On success (`POST` / `PUT`) → navigate to the detail page.

### SCR-08 데이터 출처 (`/sources`)
- A page listing: 제공기관 한국관광공사, 데이터명 TourAPI 4.0 국문 관광정보, 대상 권역 대전·충청권, 포함 지역
  대전/세종/계룡/공주/논산/옥천, 총 1,365건, 라이선스 공공누리 제3유형 (출처표시-변경금지), and the per-type
  counts table below. Include the required attribution text block.

### SCR-09 404
- Friendly not-found with a link back to `/`.

### SCR-10 Chatbot widget (global)
- **Floating button (CHAT-01):** 64px blue circle, `💬`, fixed bottom-right (24px inset).
- **Desktop panel:** 400×620, radius 16, border. Header bar (`--primary`): 🤖 avatar (white 20% circle) +
  `로컬허브 지역 비서` (16/700 white) + close `✕`. Body bg `--bg-chat`:
  - Bot bubbles: white, border, radius 12, left-aligned, text `--text-strong` 14.
  - User bubbles: `--primary` fill, white text, right-aligned, radius 12.
  - **Sources block** in bot answers: divider + `📍 관련 정보 · 추천 게시글` label, then link chips
    (bg `--link-chip-bg`, `--primary` text, radius 8) like `🗺 장태산 자연휴양림 (관광지 데이터) ↗` and
    `💬 은행동 산책 코스 후기 (커뮤니티) ↗` — clicking navigates to the place/post.
  - **Suggestion chips** (min 4, CHAT-06): white pills with `--primary` border/text, e.g.
    `대전 관광지를 추천해줘`, `이번 주말 축제를 알려줘`, `유성구 맛집 위치를 알려줘`, `축제 관련 게시글을 찾아줘`,
    `오늘은 실내와 실외 중 어디가 좋아?`. Clicking fills/sends the question.
  - Input bar: rounded input (radius 22, `메시지를 입력하세요`) + round blue send button `↑`.
- **Mobile:** fullscreen (down to 360px), header with back `←` instead of ✕.
- **Behavior:** `POST /api/chat` with `{ message, history }`. Maintain conversation history in the current
  session (`sessionStorage`, persists across route changes — CHAT-07). Block empty/duplicate sends (CHAT-03).
  Show a typing/loading indicator; on timeout/error show a message + retry button (CHAT-08). Render the
  `sources[]` array from the response as link chips. Never fabricate data — only render what the API returns.

---

## 6. API CONTRACT (call backend only, via `VITE_API_BASE_URL`)

```
GET    /api/health                         -> { "status": "ok" }

GET    /api/posts?page=&size=&keyword=&category=
                                           -> { items:[...], total, page, size, totalPages } (adapt to actual)
GET    /api/posts/{id}                      -> post detail
POST   /api/posts        body: { category, title, content, password }
PUT    /api/posts/{id}   body: { category, title, content, password }
DELETE /api/posts/{id}   body/param: { password }

GET    /api/location-types                  -> content type list (id + korean name + count)
GET    /api/locations?type_id=&keyword=&city=&page=&size=
GET    /api/locations/{contentid}

GET    /api/weather?city=daejeon            -> { city, observed_at, temperature, condition, icon_code,
                                                 recommendation, recommendation_reason, source }

POST   /api/chat         body: { message, history }
                                           -> { answer, sources:[{ type, id, label }] }
```

**Response conventions (handle these in the UI):**
- Passwords are never returned by the API.
- Wrong password → `403 Forbidden` → "비밀번호가 일치하지 않습니다."
- Missing resource → `404 Not Found` → show 404 / not-found UI.
- Validation error → `422` → show field/general error messages.
- Weather failure must NOT break other features (WEATHER-04): degrade gracefully, show "날씨 정보를 불러올 수 없습니다."

---

## 7. DOMAIN DATA MODEL

**Post (community):** `id`, `category` (`tour`/`food`/`festival`/`free` mapped to 관광지/맛집/축제/자유),
`title`, `content`, `created_at`, `updated_at?`, `views?`. Password is input-only, never rendered.

**Location (from TourAPI JSON, served by backend):** key fields — `contentid` (string), `contenttypeid`,
`title`, `addr1`, `addr2`, `tel`, `mapx`(경도 string), `mapy`(위도 string), `firstimage`, `firstimage2`.

**Content type IDs (map id → Korean label + emoji):**
```
12 관광지 🏰 (335)   14 문화시설 🎨 (82)   15 축제공연행사 🎉 (26)   25 여행코스 🧭 (28)
28 레포츠 🚴 (68)    32 숙박 🏨 (52)       38 쇼핑 🛍️ (258)         39 음식점 🍜 (516)
```
Total 1,365건. Region cities: 대전 · 세종 · 계룡 · 공주 · 논산 · 옥천.

**JSON processing rules (MUST):** parse `mapx/mapy` to float and drop invalid coords from the map; treat
empty `firstimage` as "no image" → tinted emoji placeholder; tolerate missing address/tel; keep `contentid`
as string; never invent data that isn't present.

---

## 8. QUALITY BAR / ACCEPTANCE

- Pixel-faithful to the tokens/specs above (colors, radii, spacing, typography, Korean copy).
- Responsive 360px → 1440px; chatbot is a floating panel on desktop and fullscreen on mobile.
- Every data view has loading, empty, and error(+retry) states.
- Board CRUD works end-to-end against the API; list ↔ URL query stay in sync; refresh persists correct view.
- Map shows only valid coordinates; images gracefully fall back; app never crashes on missing fields.
- Footer attribution present on all pages; `/sources` page complete.
- No secrets in code; only `VITE_API_BASE_URL`; `.env.example`, `.gitignore`, Netlify SPA redirect included.
- Clean component structure (e.g. `components/` for AppHeader, AppFooter, WeatherWidget, CategoryCard,
  PlaceCard, PostRow, FilterChips, Pagination, PasswordModal, ChatWidget, etc.; `views/` per route;
  `stores/` for chat & filters; `api/` client; `router/`).

Now generate the complete project. Start with the file tree, then output each file's full contents.
Ask no clarifying questions — make reasonable, documented choices for anything unspecified.
