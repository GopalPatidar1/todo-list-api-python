from fastapi import APIRouter, Request, Depends
from app.service import todolist
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.schema.todo_list import TodoItem, UpdateTodoItem

router = APIRouter(prefix='/todolist', tags=[
    'Todo List'
])

@router.get('/')
def getTodolist(request: Request, db= Depends(get_db), limit:int = 10, nextCursor:int|None=None):
    userId =  request.state.userId
    return todolist.getTodolist(userId=userId, db=db, limit=limit, nextCursor=nextCursor)

@router.post('/')
def addTodoItem(request: Request, data: TodoItem, db = Depends(get_db)):
    userId = request.state.userId
    return todolist.addTodoItem(db, data, userId)

@router.put('/{todoId}')
def updateTodoItem(todoId: int, request: Request, item: UpdateTodoItem, db = Depends(get_db)):
    return todolist.updateTodo(userId=request.state.userId, data=item, db=db, todoId=todoId)

@router.delete('/{item_id}')
def deleteTodoItem(item_id: int,request: Request, db:Session =Depends(get_db)):
    return todolist.deleteTodoItem(todoId=item_id, db=db, userId=request.state.userId)

@router.get('/{item_id}')
def getTodoItem(item_id: int):
    return {
        'id': item_id,
        'title': f'Todo item {item_id}',
        'completed': False
    }
