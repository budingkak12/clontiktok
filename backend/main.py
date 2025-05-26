from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

app = FastAPI()

# 获取当前文件的目录
current_dir = Path(__file__).parent
# 获取项目根目录
project_root = current_dir.parent
# dist目录路径
dist_dir = project_root / "dist"

# 挂载静态文件 - 将整个dist目录作为静态文件目录
app.mount("/", StaticFiles(directory=str(dist_dir), html=True), name="static")

@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI backend!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 