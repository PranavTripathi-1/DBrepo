from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from infrastructure.database import create_tables
from presentation.api.routes import document_routes, search_routes
from presentation.api.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
def create_app() -> FastAPI:
    app = FastAPI(
        title="Clean Architecture API with Vector Embeddings",
        description="A comprehensive API demonstrating Clean Architecture with CRUD operations, Redis caching, and vector search using Qdrant",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Include routers
    app.include_router(document_routes.router, prefix="/api/v1")
    app.include_router(search_routes.router, prefix="/api/v1")
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Clean Architecture API with Vector Embeddings",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health"
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "clean-architecture-api"}
    
    return app

app = create_app()

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
