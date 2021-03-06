from time import time

from fastapi import FastAPI, Request

from apis.user import router as user_apis
from apis.helium import router as helium_apis
from apis.coingecko import router as coingecko_apis
from apis.authentication import router as authentication_apis
from database.postgres.postgres import Postgres
from settings import settings

if settings.database == Postgres:
    from database.postgres.base import Base, engine
    Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/status")
async def status():
    return {"status": "OK"}


app.include_router(authentication_apis, prefix="")
app.include_router(user_apis, prefix="/user")
app.include_router(helium_apis, prefix="/helium")
app.include_router(coingecko_apis, prefix="/coingecko")
