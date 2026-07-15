gi# LocalHub Backend

## 설치

```bash
cd localhub-backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 실행

```bash
uvicorn main:app --reload
```

## 주요 엔드포인트

- `GET /api/regions`
- `GET /api/posts`
- `GET /api/posts/{post_id}`
- `POST /api/posts`
- `PUT /api/posts/{post_id}`
- `DELETE /api/posts/{post_id}`
- `GET /api/posts/{post_id}/comments`
- `POST /api/posts/{post_id}/comments`
- `GET /api/festivals`
- `GET /api/attractions`
- `POST /api/chat`
