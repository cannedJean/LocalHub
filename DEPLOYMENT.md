# LocalHub 배포 런북

백엔드는 Render, 프론트엔드는 Netlify에 배포합니다. 저장소가 모노레포이므로 각 서비스의 Root/Base Directory를 반드시 지정해야 합니다.

## 0. 배포 전 게이트

```powershell
cd localhub-backend
python -m pytest -q

cd ..\localhub-frontend
npm ci
npm run build
```

다음 값은 코드나 GitHub에 넣지 않고 각 배포 서비스의 Environment variables에만 등록합니다.

- OpenAI 프로젝트 API 키
- 기상청 API허브 인증키(`authKey`)
- 운영 프론트 URL

## 1. Render 백엔드

GitHub 저장소를 연결하고 Web Service를 생성합니다.

| 설정 | 값 |
|---|---|
| Root Directory | `localhub-backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/api/health` |

환경변수:

| 키 | 값 |
|---|---|
| `PYTHON_VERSION` | `3.12.13` |
| `ALLOWED_ORIGINS` | Netlify 운영 origin. 초기 배포 전에는 임시 URL을 넣고 이후 확정 URL로 교체 |
| `OPENAI_API_KEY` | OpenAI 프로젝트 키 |
| `OPENAI_MODEL` | `gpt-5-mini` 또는 해당 OpenAI 프로젝트에서 허용된 Responses API 모델 |
| `OPENAI_TIMEOUT_SECONDS` | `20` |
| `OPENAI_MAX_OUTPUT_TOKENS` | `800` |
| `OPENAI_REASONING_EFFORT` | `minimal` |
| `WEATHER_API_KEY` | 기상청 API허브 인증키(`authKey`) |
| `WEATHER_TIMEOUT_SECONDS` | `10` |

### SQLite 영속성 — 배포 전에 반드시 선택

Render의 기본 파일시스템은 재배포·재시작 때 유지되지 않습니다.

- **운영 권장:** 유료 Persistent Disk를 `/var/data`에 마운트하고 `DATABASE_URL=sqlite:////var/data/localhub.db`로 설정합니다. 익명 게시글이 재배포 후에도 보존됩니다.
- **무료 시연 한정:** `DATABASE_URL=sqlite:///./localhub.db`를 사용합니다. 서비스는 동작하지만 재배포·재시작 때 게시글이 유실될 수 있으므로 운영 완료로 간주하지 않습니다.

Persistent Disk 생성은 비용이 발생하므로 결제 승인 후에만 진행합니다.

배포 후 점검:

```text
GET  https://<render-host>/api/health                    -> 200 {"status":"ok"}
GET  https://<render-host>/api/locations?size=3          -> 200, total=1365
GET  https://<render-host>/api/weather?city=daejeon      -> 200, source=기상청...
POST https://<render-host>/api/chat                      -> 200, answer + sources
```

Render 로그에 API 키, 게시글 비밀번호, 전체 요청 본문이 출력되지 않는지 확인합니다.

## 2. Netlify 프론트엔드

| 설정 | 값 |
|---|---|
| Base directory | `localhub-frontend` |
| Build command | `npm run build` |
| Publish directory | `dist` |
| Environment | `VITE_API_BASE_URL=https://<render-host>` |

`VITE_API_BASE_URL`에는 `/api`를 붙이지 않습니다. Axios 클라이언트가 자동으로 `/api`를 추가합니다. `public/_redirects`와 `netlify.toml`의 SPA fallback으로 딥링크 새로고침을 처리합니다.

Netlify URL이 확정되면 Render의 `ALLOWED_ORIGINS`를 해당 origin으로 갱신하고 다시 배포합니다.

## 3. 운영 수용 테스트

360px와 데스크톱 화면에서 다음 순서로 확인합니다.

1. 홈 추천 장소와 최근 게시글의 로딩·빈 상태·오류 재시도
2. 장소 검색/유형/도시 필터와 지도 마커·팝업
3. 게시글 생성 → 상세 → 잘못된 비밀번호 403 → 정상 수정 → 정상 삭제
4. 날씨 위젯의 실제 기온·상태·활동 추천과 오류 재시도
5. 챗봇 추천 질문 5개, 출처 칩 이동, 중복 전송 차단, 세션 유지, 외부 오류 재시도
6. `/boards/없는번호` 및 임의 경로의 404, 각 딥링크 새로고침
7. 응답과 브라우저 콘솔/Network에 비밀번호나 외부 API 키가 없는지 확인
