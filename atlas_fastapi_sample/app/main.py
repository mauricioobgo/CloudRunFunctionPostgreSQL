from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from app.config import APP_NAME
from app.db import create_db_and_tables, get_session
from app.models import User, UserCreate, UserRead


app = FastAPI(title=APP_NAME)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/users", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, session: Session = Depends(get_session)) -> User:
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User.model_validate(payload)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
