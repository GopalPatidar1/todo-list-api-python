from functools import wraps
import asyncio

def retry(max_retries, delay):
     def commonFun(func):
        @wraps(func)
        async def wrapper(*args, **kargs):
           for attempt in range(max_retries):
             last_exception = None
             try:
              return await func(*args, **kargs)
             except Exception as exc:
                 last_exception = exc
                 print(f"Attempt {attempt + 1} failed: {exc}")
                 if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
           raise last_exception
        return wrapper
     return commonFun
  
  
@retry(3, 3)
async def sendTodoUpdatenotification(userId, message):
    print("sending a notificaion for todo list message", userId, message)
    


