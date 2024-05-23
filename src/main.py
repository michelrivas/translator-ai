from fastapi import FastAPI

from src.translator.router import router


app = FastAPI(docs_url="/")

app.include_router(router)
