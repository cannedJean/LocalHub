# LocalHub

대전·충청권의 한국관광공사 TourAPI 4.0 데이터와 익명 커뮤니티를 제공하는 Vue 3 + FastAPI MVP입니다.

## 프로젝트 구성

- `localhub-frontend`: Vue 3, Vite, Vue Router 4, Pinia, Leaflet SPA
- `localhub-backend`: FastAPI, SQLAlchemy, SQLite REST API
- `localhub-files`: 요구사항, 회의 기록, 원천 데이터, 프로젝트 산출물
- `localhub-submission`: 제출용 산출물

프론트엔드는 자체 백엔드의 `/api`만 호출합니다. OpenAI 및 기상청 서비스키는 백엔드 환경변수에만 저장하며 Git에 커밋하지 않습니다.

## 로컬 실행

백엔드:

```powershell
cd localhub-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

프론트엔드(별도 터미널):

```powershell
cd localhub-frontend
npm install
Copy-Item .env.example .env
npm run dev -- --host 127.0.0.1
```

- 프론트: `http://127.0.0.1:5173`
- API 문서: `http://127.0.0.1:8000/docs`
- 상태 확인: `http://127.0.0.1:8000/api/health`

자세한 API 설정은 [localhub-backend/README.md](localhub-backend/README.md), 배포 순서와 영구 디스크 주의사항은 [DEPLOYMENT.md](DEPLOYMENT.md)를 참고합니다.
