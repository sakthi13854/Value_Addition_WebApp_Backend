from sqlalchemy import URL
import os 


DATABASE_URL=URL.create(
    "mysql+pymysql",
    username = os.getenv('DB_USERNAME'),
    password = os.getenv('DB_PASSWORD'),
    host = os.getenv('DB_HOST'),
    database = os.getenv('DB_DATABASE')
)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_CSRF_PROTECT = False
JWT_COOKIE_SECURE = False
JWT_COOKIE_SAMESITE = "Lax"