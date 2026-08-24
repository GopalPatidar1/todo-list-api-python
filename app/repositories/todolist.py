from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.todo_list import TodoList
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def addTodo(db:AsyncSession, todo):
    db.add(todo)
    await db.flush()

async def getTodolist(db: AsyncSession, userId: str, nextCursor: int | None, limit:int):
    filterRec = [TodoList.user_id == userId]

    if nextCursor is not None:
        filterRec.append(TodoList.id <= nextCursor)
        # join() / outerjoin() control the SQL rows you query; selectinload() controls how SQLAlchemy loads related objects.
    result = await db.scalars(
        select(TodoList)
        # // Used to eagerly load a related object/relationship using a separate SQL query, so accessing the relationship does not cause additional queries for each record.
        .options(selectinload(TodoList.user)) 
        # Creates an INNER JOIN between tables. It returns only records that have a matching related record and is commonly used to filter or query using related table columns.
        # .join(TodoList.user) 
        # Creates a LEFT OUTER JOIN between tables. It returns all records from the main table, even when there is no matching related record.
        # .outerjoin(TodoList.user)
        .where(*filterRec)
        .order_by(TodoList.id.desc())
        .limit(limit+1)
    )
    result = result.all()

    nextCursor = result[-1].id if result else None
    availNext = len(result) > limit

    return {"nextCursor": nextCursor, "availNext":availNext ,"result": result[:limit]}

async def deleteTodo(todoId: int, userId: int, db: AsyncSession):
    result = await db.execute(delete(TodoList).where(
        TodoList.user_id == userId,
        TodoList.id == todoId
    ))

    await db.commit()

    return result

async def updateTodoItem(db: AsyncSession, todoId:int, userId: int, data):
     result = await db.execute(
        update(TodoList)
        .where(
            TodoList.id == todoId,
            TodoList.user_id == userId
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(TodoList)
       )

     await db.commit()

     return result.scalar_one_or_none()