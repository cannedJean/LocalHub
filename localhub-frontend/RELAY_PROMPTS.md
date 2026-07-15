# LocalHub — Gemini ⇄ GPT Relay Prompts

Two reusable prompts for the review loop, plus locked decisions both models must honor.
Loop order each round: **Gemini generates/revises → paste to GPT → GPT corrects → paste GPT's fixes back to Gemini → repeat.**

---

## LOCKED DECISIONS (paste once into BOTH chats; keep constant for the whole loop)

1. **Architecture is fixed:** Vite + Vue 3 SFC (`<script setup>`) + Vue Router 4 (`createWebHistory`) + Pinia.
   The single-file CDN `localhub_app.html` is a throwaway visual reference only — **not** the deliverable.
2. **Output as multiple files**, never one HTML file. Each file goes in its own fenced code block whose
   first line is a path comment, e.g. `<!-- src/App.vue -->` or `// src/router/index.js`.
3. **Password verification (resolves GPT's open question — do NOT invent an endpoint):**
   - **Delete:** the confirm modal sends the password to `DELETE /api/posts/:id`. Wrong password → `403` →
     keep the modal open and show "비밀번호가 일치하지 않습니다."
   - **Edit:** the confirm modal navigates to `/boards/:id/edit` and carries the entered password in memory
     (Pinia, not the URL). The edit form's `PUT /api/posts/:id` is what actually verifies it; `403` → show
     the error on the form's password field. (No `verify-password` endpoint unless the backend later adds one.)
4. **Reuse GPT's already-corrected files verbatim** (do not regenerate): `index.html`, `src/main.js`,
   `src/api/client.js`, `src/router/index.js`, `.env.example`, `public/_redirects`.
5. All other rules come from the master spec in `GPT_CODEX_REVIEW_PROMPT.md` / `GEMINI_FRONTEND_PROMPT.md`
   (constraints, design tokens, screens, API contract, data model). Those are the source of truth.

---

## PROMPT A → send to GEMINI (rebuild / revise)

> Your previous output was a single `localhub_app.html` using Vue via CDN + the Options API. That is WRONG
> for this project and violates the required architecture. **Rebuild LocalHub as a real Vite + Vue 3 SFC
> project** using `<script setup>`, Vue Router 4 (`createWebHistory`), and Pinia.
>
> **Output rules:** Do NOT produce one HTML file. Produce **separate files**, each in its own fenced code
> block whose first line is a path comment (e.g. `<!-- src/App.vue -->`, `// src/stores/chat.js`). Give me
> **3–6 files per message**; I'll reply "continue" for the next batch. Keep the exact same visual design,
> Korean copy, colors, radii, and layout you already designed — only change the architecture and fix the
> issues below.
>
> **Reuse these files verbatim (do not regenerate them):** `index.html`, `src/main.js`, `src/api/client.js`,
> `src/router/index.js`, `.env.example`, `public/_redirects` — I will paste them below.
> [paste GPT's corrected entry/config files here]
>
> **Now generate the remaining files** (`src/App.vue`, `src/styles/tokens.css`, `src/styles/base.css`,
> `src/api/posts.js`, `src/api/locations.js`, `src/api/weather.js`, `src/api/chat.js`, `src/stores/chat.js`,
> `src/stores/filters.js`, all `src/components/*`, all `src/views/*`) and fix ALL of these, which a reviewer
> flagged in your last version:
>
> 1. Remove ALL mock/fabricated data and mock authorization. Never fall back to fake posts/locations on
>    network/403/404/422; preserve the real HTTP status and surface it in the UI.
> 2. Remove ALL frontend password storage. Passwords are input-only, sent to the API, never stored/returned/logged.
>    Do NOT claim the password is encrypted anywhere in the UI.
> 3. Read the API base **only** from `VITE_API_BASE_URL` (via the provided `client.js`). No hardcoded URLs.
> 4. Use the real endpoints only: `GET/POST /api/posts`, `GET/PUT/DELETE /api/posts/:id`,
>    `GET /api/location-types`, `GET /api/locations`, `GET /api/locations/:contentid`, `GET /api/weather?city=`,
>    `POST /api/chat`. There is no `/api/map/markers` — use `GET /api/locations`.
> 5. Correct field names to the TourAPI/contract shape: post `category` values are `tour`/`food`/`festival`/`free`
>    (↔ 관광지/맛집/축제/자유); locations use `contentid` (string), `contenttypeid`, `title`, `addr1`, `addr2`,
>    `tel`, `mapx` (경도, string), `mapy` (위도, string), `firstimage`. No `latitude`/`content_id`/`restaurant` etc.
> 6. Every data view needs **loading, empty, and error+retry** states.
> 7. Home: category shortcuts navigate with `?type=<contentTypeId>` (12/14/15/25/28/32/38/39); recommended
>    cards use tinted emoji fallback when `firstimage` is empty. No Unsplash/external placeholder images.
> 8. Places/Map: honor `keyword`/`type`/`city` query params; include all 8 content types and all 6 cities
>    (대전·세종·계룡·공주·논산·옥천). Parse `mapx/mapy` to float; reject empty/non-finite/out-of-range coords
>    (exclude from map, never crash). Add selected-marker style + full popup. Build the popup DOM **safely**
>    (no interpolated HTML → no XSS). **Destroy the Leaflet map on `onUnmounted`.**
> 9. Boards list: category chips (전체·관광지·맛집·축제·자유게시판) + search + pagination + `조회` column,
>    all synced to the URL query (`page`/`keyword`/`category`).
> 10. Post form: category options 관광지/맛집/축제/자유게시판; 제목 `maxlength=100`; 비밀번호 min 4 chars;
>     per-field validation errors; map backend `422` messages to fields.
> 11. Post detail: loading/404/error states; show 작성일/조회/수정됨 meta; correct back-to-list behavior;
>     accessible (keyboard-operable) password modal.
> 12. Password modal behavior per the LOCKED DECISIONS above (delete via DELETE, edit carries pw in memory + PUT verifies).
> 13. Sources page: include 총 1,365건 and the per-content-type counts table (12:335, 14:82, 15:26, 25:28,
>     28:68, 32:52, 38:258, 39:516).
> 14. Chat widget: guard against malformed `sessionStorage` (try/catch); do NOT duplicate the current message
>     in history; render `sources[]` as `{ type, id, label }` (navigate to the place/post — no `route` field);
>     include ≥4 suggestion chips; add timeout/error/retry; mobile = fullscreen with a back `←` header.
> 15. Weather: use the contract fields (`temperature`, `condition`, `icon_code`, `recommendation`,
>     `recommendation_reason`, `source`); on failure show "날씨 정보를 불러올 수 없습니다." without breaking other UI.
> 16. Accessibility/layout: working mobile menu; use real `<button>`/`<a>` for clickable elements; label inputs;
>     footer must be the exact sentence
>     `출처: 한국관광공사 | 데이터: TourAPI 4.0 국문 관광정보 | 라이선스: 공공누리 제3유형 (출처표시-변경금지)`;
>     mobile padding and chatbot inset = 24px.

---

## PROMPT B → send to GPT (each time you bring Gemini's revised code back)

> **Batch N — Gemini's revised code** (rebuilt as a Vite SFC project addressing your previous review).
> Re-review it against the full LocalHub spec and ALL your prior decisions and fixes. In the Change report,
> explicitly mark each relevant prior issue as **FIXED / STILL OPEN / REGRESSED**, and add any new issues.
> Keep the same output format: **Verdict → Change report → Corrected code → Open questions / regressions.**
>
> [paste the Gemini files here]

---

## PRACTICAL TIPS

- Gemini **canvas** favors single immersive files. If it keeps collapsing everything into one HTML, tell it
  in normal chat (not canvas): *"Output each file as a separate fenced code block with a path-comment first
  line; no canvas, no single-file bundle."*
- Relay in **coherent units** (whole files/components), not fragments — reviewers correct full files far better.
- Do a build sanity check locally between rounds: `npm install` then `npm run dev` (and `npm run build`),
  and paste any real Vite/console errors into Prompt B so GPT fixes concrete failures, not just spec drift.
