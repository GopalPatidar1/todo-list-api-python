from fastapi import APIRouter, Request, Depends, status
from app.service import todolist
from app.config.database import get_db
from app.schema.todo_list import TodoItem, UpdateTodoItem
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/todolist', tags=[
    'Todo List'
])

@router.get('/')
async def getTodolist(request: Request, db: AsyncSession = Depends(get_db), limit:int = 10, nextCursor:int|None=None):
    userId =  request.state.userId
    return await todolist.getTodolist(userId=userId, db=db, limit=limit, nextCursor=nextCursor)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def addTodoItem(request: Request, data: TodoItem, db: AsyncSession = Depends(get_db)):
    userId = request.state.userId
    return await todolist.addTodoItem(db, data, userId)

@router.put('/{todoId}')
async def updateTodoItem(todoId: int, request: Request, item: UpdateTodoItem, db: AsyncSession = Depends(get_db)):
    return await todolist.updateTodo(userId=request.state.userId, data=item, db=db, todoId=todoId)

@router.delete('/{item_id}')
async def deleteTodoItem(item_id: int,request: Request, db: AsyncSession =Depends(get_db)):
    return await todolist.deleteTodoItem(todoId=item_id, db=db, userId=request.state.userId)

@router.get('/{item_id}')
def getTodoItem(item_id: int):
    return {
        'id': item_id,
        'title': f'Todo item {item_id}',
        'completed': False
    }
