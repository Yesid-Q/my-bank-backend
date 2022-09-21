from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.configs.settings import settings, TORTOISE_ORM
from src.routers.v1 import v1_router

app: FastAPI = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    

@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()

app.include_router(v1_router, prefix='/v1')