import uvicorn
from fastapi import FastAPI
from src.apis.text_chat import router
import sys


sys.path.append("..")
app = FastAPI()
# 添加子路由
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005)
