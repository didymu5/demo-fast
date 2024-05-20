from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from redis import Redis

# Define a simple Todo model
class Todo:
    def __init__(self, id: int, text: str, completed: bool):
        self.id = id
        self.text = text
        self.completed = completed

# Create a FastAPI app
app = FastAPI()

# Dependency function to connect to Redis
async def get_redis():
    redis_client = Redis(host="localhost", port=6379)
    yield redis_client
    redis_client.close()

# Get all todos
@app.get("/todos")
async def get_all_todos(redis: Redis = Depends(get_redis)):
    try:
        todos = []
        for key in redis.scan_iter():
            todo_data = redis.hgetall(key)
            if todo_data:
                todo = Todo(
                    int(todo_data[b"id"]), todo_data[b"text"].decode(), bool(todo_data[b"completed"])
                )
                todos.append(todo)
        return jsonable_encoder(todos)
    except:
      raise HTTPException(status_code=404, detail="Todo no found") 
# Get a specific todo by ID
@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int, redis: Redis = Depends(get_redis)):
    todo_key = f"todo:{todo_id}"
    todo_data = redis.hgetall(todo_key)
    if not todo_data:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo = Todo(
        int(todo_data[b"id"]), todo_data[b"text"].decode(), bool(todo_data[b"completed"])
    )
    return jsonable_encoder(todo)

# Create a new todo
@app.post("/todos")
async def create_todo(text: str, redis: Redis = Depends(get_redis)):
    next_id = int(redis.incr("todo_id"))
    todo_key = f"todo:{next_id}"
    redis.hset(todo_key, {"id": next_id, "text": text, "completed": False})
    return jsonable_encoder(Todo(next_id, text, False))

# Mark a todo as completed
@app.patch("/todos/{todo_id}/completed")
async def mark_completed(todo_id: int, redis: Redis = Depends(get_redis)):
    todo_key = f"todo:{todo_id}"
    if not redis.exists(todo_key):
        raise HTTPException(status_code=404, detail="Todo not found")
    redis.hset(todo_key, {"completed": True})
    return {"message": "Todo marked as completed"}

# Delete a todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, redis: Redis = Depends(get_redis)):
    todo_key = f"todo:{todo_id}"
    if not redis.exists(todo_key):
        raise HTTPException(status_code=404, detail="Todo not found")
    redis.delete(todo_key)
    return {"message": "Todo deleted"}

# Run the API (uvicorn is recommended)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)