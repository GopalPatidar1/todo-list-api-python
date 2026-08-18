from app.repositories.todolist import addTodo, getTodolist as fetchTodo, deleteTodo, updateTodoItem
from app.models.todo_list import TodoList
from fastapi.responses import JSONResponse
from app.core.customException import CustomException
from sqlalchemy.ext.asyncio import AsyncSession

async def addTodoItem(db: AsyncSession, todoData, userId: int):
    try:
      todo = TodoList(
          task=todoData.task,
          desc=todoData.desc,
          user_id=int(userId),
      )
      
      await addTodo(db, todo)

      await db.commit()
      await db.refresh(todo)
      
      return {
          "id": todo.id,
          "task": todo.task,
      }
    except Exception as e:
        await db.rollback()
        print(f"Error creating todo: {e}")
        raise CustomException(500, "Something went wrong") 

async def getTodolist(userId: str, db: AsyncSession, limit: int, nextCursor: int|None):
   return  await fetchTodo(db=db, userId=userId, limit=limit, nextCursor=nextCursor)

async def deleteTodoItem(db: AsyncSession, userId: str, todoId: str):
   result = await deleteTodo(db=db, userId=userId, todoId=todoId)
   if result.rowcount == 0:
      raise CustomException(404,"Todo not found") 
   
   return {
      'success': True
   }

async def updateTodo(db: AsyncSession, todoId:str, userId: str, data,):
   result = await updateTodoItem(db=db, todoId=todoId, userId=userId, data=data)

   if result is None:
      raise CustomException(404,"Todo not found") 
   return result