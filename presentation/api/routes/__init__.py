from fastapi import APIRouter
from .document_routes import router as document_router
from .search_routes import router as search_router

api_router = APIRouter()
api_router.include_router(document_router)
api_router.include_router(search_router)
