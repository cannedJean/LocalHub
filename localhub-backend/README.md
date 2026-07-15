# LocalHub Backend

LocalHub Vue SPA가 호출하는 FastAPI REST 백엔드입니다. 관광 데이터는 저장소에 수록된 한국관광공사 TourAPI 4.0 JSON 1,365건만 사용합니다.

## 환경 준비

Python 3.12 권장:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

`.env`에 필요한 값을 입력합니다. 실제 값은 절대 커밋하지 않습니다.

| 변수 | 필수 여부 | 설명 |
|---|---:|---|
| `DATABASE_URL` | 필수 | 로컬 기본값 `sqlite:///./localhub.db` |
| `ALLOWED_ORIGINS` | 필수 | 허용할 프론트 origin을 쉼표로 구분. 경로와 끝 `/` 제외 |
| `OPENAI_API_KEY` | 챗봇 LLM 사용 시 | OpenAI 프로젝트 API 키 |
| `OPENAI_MODEL` | 선택 | 기본 `gpt-5-mini`(프로젝트에서 허용된 모델로 변경 가능) |
| `OPENAI_TIMEOUT_SECONDS` | 선택 | OpenAI 요청 제한시간, 기본 20초 |
| `OPENAI_MAX_OUTPUT_TOKENS` | 선택 | 추론 토큰을 포함한 출력 상한, 기본 800 |
| `OPENAI_REASONING_EFFORT` | 선택 | `minimal`/`low`/`medium`/`high`, 기본 `minimal` |
| `WEATHER_API_KEY` | 날씨 사용 시 | 기상청 API허브에서 발급한 `authKey` |
| `WEATHER_TIMEOUT_SECONDS` | 선택 | 기상청 요청 제한시간, 기본 10초 |

실행:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 외부 API 동작

### 챗봇

`POST /api/chat`은 먼저 로컬 관광 JSON과 커뮤니티 DB에서 질문과 관련된 자료를 검색합니다. 검증된 문맥이 있고 `OPENAI_API_KEY`가 설정된 경우에만 OpenAI Responses API를 호출합니다.

- 모델은 `OPENAI_MODEL`로 교체할 수 있습니다.
- GPT-5 계열은 추론 토큰도 출력 상한을 사용하므로 기본값을 `minimal`, 800 tokens로 제한합니다.
- 최근 대화 10개만 모델에 전달합니다.
- 관광 데이터·게시글·기상청 예보 밖의 사실은 생성하지 않도록 시스템 지시를 적용합니다.
- 키가 없으면 동일한 검색 결과로 결정적 안내문을 반환합니다.
- OpenAI 실패는 숨기지 않고 `502`로 반환하여 프론트 재시도가 동작합니다.
- 게시글 비밀번호는 조회·응답·챗봇 문맥·로그에 포함하지 않습니다.

### 날씨

`GET /api/weather?city=daejeon`은 기상청 API허브의 `VilageFcstInfoService_2.0/getUltraSrtFcst`를 백엔드에서 호출합니다. 결과는 10분 동안 메모리 캐시하여 호출량과 지연을 줄입니다.

[기상청 API허브 동네예보 조회](https://apihub.kma.go.kr/apiList.do?apiMov=4.+%EB%8F%99%EB%84%A4%EC%98%88%EB%B3%B4%28%EC%B4%88%EB%8B%A8%EA%B8%B0%EC%8B%A4%ED%99%A9%C2%B7%EC%B4%88%EB%8B%A8%EA%B8%B0%EC%98%88%EB%B3%B4%C2%B7%EB%8B%A8%EA%B8%B0%EC%98%88%EB%B3%B4%29+%EC%A1%B0%ED%9A%8C&seqApi=10&seqApiSub=286)에서 초단기예보 API 활용신청 후 마이페이지의 인증키를 `WEATHER_API_KEY`에 입력합니다. 키가 없으면 `503`, 지원하지 않는 도시이면 `422`, 제공기관 오류이면 `502`를 반환합니다.

## API

```text
GET    /api/health
GET    /api/posts?page=&size=&keyword=&category=
GET    /api/posts/{id}
POST   /api/posts
PUT    /api/posts/{id}
DELETE /api/posts/{id}
GET    /api/location-types
GET    /api/locations?type_id=&keyword=&city=&page=&size=
GET    /api/locations/{contentid}
GET    /api/weather?city=daejeon
POST   /api/chat
```

게시글 수정·삭제는 생성 시 입력한 평문 비밀번호를 서버에서 비교합니다. 이 방식은 교육용 요구사항이며 비밀번호는 모든 응답 스키마에서 제외됩니다.

## 검증

```powershell
python -m pytest -q
```

테스트는 임시 SQLite DB와 가짜 외부 API 응답을 사용하므로 실제 글과 API 사용량에 영향을 주지 않습니다.

배포 설정과 SQLite 영속성 선택은 저장소 루트의 [DEPLOYMENT.md](../DEPLOYMENT.md)를 따릅니다.
