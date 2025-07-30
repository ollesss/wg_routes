from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Монтируем статические файлы
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

# Важно для Fly.io!
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))