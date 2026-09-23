import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@db:5432/tasks"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class TaskCreate(BaseModel):
    title: str

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

app = FastAPI(title="DevOps Task Manager API")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/tasks", response_model=list[TaskResponse])
def get_tasks():
    with SessionLocal() as db:
        return db.query(Task).order_by(Task.id).all()

@app.post("/api/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    title = task.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    with SessionLocal() as db:
        item = Task(title=title)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

@app.patch("/api/tasks/{task_id}", response_model=TaskResponse)
def toggle_task(task_id: int):
    with SessionLocal() as db:
        item = db.get(Task, task_id)
        if not item:
            raise HTTPException(status_code=404, detail="Task not found")
        item.completed = not item.completed
        db.commit()
        db.refresh(item)
        return item
