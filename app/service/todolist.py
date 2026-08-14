from app.repositories.todolist import addTodo, getTodolist as fetchTodo, deleteTodo, updateTodoItem
from app.models.todo_list import TodoList
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

def addTodoItem(db: Session, todoData, userId: int):
    try:
      todo = TodoList(
          task=todoData.task,
          desc=todoData.desc,
          user_id=userId,
      )
      
      addTodo(db, todo)

      db.commit()
      db.refresh(todo)
      
      return {
          "id": todo.id,
          "task": todo.task,
      }
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code = 500,content={
            'detail': 'Something went wrong'
        })

def getTodolist(userId: str, db:Session, limit: int, nextCursor: int|None):
   return  fetchTodo(db=db, userId=userId, limit=limit, nextCursor=nextCursor)

def deleteTodoItem(db: Session, userId: str, todoId: str):
   return deleteTodo(db=db, userId=userId, todoId=todoId)

def updateTodo(db:Session, todoId:str, userId: str, data,):
   return updateTodoItem(db=db, todoId=todoId, userId=userId, data=data)