from fastapi import APIRouter

from src.routers.v1.auth_router import auth_router
from src.routers.v1.account_router import account_router
from src.routers.v1.document_router import document_router
from src.routers.v1.profile_router import profile_router
from src.routers.v1.type_account_router import type_account_router
from src.routers.v1.transaction_router import transaction_router

v1_router = APIRouter()

v1_router.include_router(router=document_router, prefix='')
v1_router.include_router(router=type_account_router, prefix='')
v1_router.include_router(router=auth_router, prefix='')
v1_router.include_router(router=profile_router, prefix='')
v1_router.include_router(router=account_router, prefix='')
v1_router.include_router(router=transaction_router, prefix='')