import os


APP_NAME = os.getenv("APP_NAME", "Atlas SQLModel Sample")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/app_db")
