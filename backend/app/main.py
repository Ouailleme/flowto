"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Import routers
from app.api.v1 import auth, banks, transactions, invoices, reconciliations, categorization, reminders

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="FinanceAI - Automatisation comptable PME avec IA",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FinanceAI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API routers
API_V1_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_V1_PREFIX, tags=["Authentication"])
app.include_router(banks.router, prefix=API_V1_PREFIX, tags=["Bank Accounts"])
app.include_router(transactions.router, prefix=API_V1_PREFIX, tags=["Transactions"])
app.include_router(invoices.router, prefix=API_V1_PREFIX, tags=["Invoices"])
app.include_router(reconciliations.router, prefix=API_V1_PREFIX, tags=["Reconciliations"])
app.include_router(categorization.router, prefix=API_V1_PREFIX, tags=["Categorization"])
app.include_router(reminders.router, prefix=API_V1_PREFIX, tags=["Reminders"])


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("🚀 FinanceAI API starting...")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔧 Environment: {settings.APP_ENV}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("👋 FinanceAI API shutting down...")
