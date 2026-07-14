import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./localhub.db")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# 게시판 비밀번호 검증용 샐트(실제 배포 시 더 강력한 솔트/해싱 방식 사용 권장)
PASSWORD_SALT = os.getenv("PASSWORD_SALT", "localhub-secret-salt")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")