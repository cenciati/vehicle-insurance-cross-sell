from fastapi import FastAPI

from src.api.routes.predict import predict

app = FastAPI(root_path="/")

app.include_router(predict)
