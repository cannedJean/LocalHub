# LocalHub release changes

## 외부 API 연동

- 구형 `openai.ChatCompletion` 호출을 OpenAI Python SDK 2.x의 비동기 Responses API로 교체
- 관광 JSON·커뮤니티 게시글·기상청 예보를 검색한 뒤 검증된 문맥만 모델에 전달
- 기상청 API허브 초단기예보 API, 지역 격자, 응답 파싱, 활동 추천, 10분 캐시 구현
- API 키를 백엔드 `SecretStr` 환경변수로 한정하고 프론트/로그/응답에서 제외
- 외부 서비스 설정 누락과 제공기관 장애를 503/502로 구분

## 계약·품질

- `/api/location-types`에 데이터 기반 유형별 count 추가(합계 1,365)
- 게시글 category 허용값과 삭제 비밀번호 길이를 백엔드 스키마에서 검증
- 챗봇 history/source 역할·길이·타입 검증 및 자연어 검색 정확도 개선
- 프론트 날씨 아이콘·재시도·30초 챗봇 타임아웃 적용
- 지도 좌표를 한국 범위로 검증하여 `0,0`과 한국 밖 원천 오좌표 제외
- 사용되지 않던 가공 더미 관광 JSON 제거

## 검증·운영

- API, 게시글 CRUD/403, 챗봇 검색/OpenAI 호출, 기상청 파싱 회귀 테스트 추가
- 로컬/Render/Netlify 환경변수와 SQLite 영속성 선택을 배포 런북에 명시
- 실제 비밀값을 제외한 백엔드 `.env.example` 추가
