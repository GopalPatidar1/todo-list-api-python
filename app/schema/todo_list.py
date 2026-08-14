from pydantic import BaseModel, Field

class TodoItem(BaseModel):
    task: str = Field(min_length=5, max_length=50)
    desc: str = Field(min_length=5, max_length=255)

class UpdateTodoItem(BaseModel):
    task: str | None = None
    desc: str | None = None
    status: str | None = None