# 🚀 DÉMARRAGE DÉVELOPPEMENT - MODE CODE

## ✅ CE QUI EST PRÊT

- ✅ Structure projet complète (backend + frontend)
- ✅ Docker Compose (PostgreSQL + Redis + Backend + Frontend + Celery)
- ✅ Requirements Python + dependencies
- ✅ Configuration TypeScript/Next.js
- ✅ Standards qualité (.cursorrules)
- ✅ Plan développement détaillé (PLAN_DEV_CODE_FIRST.md)

---

## 🔥 QUICK START (5 MINUTES)

### Prérequis
```bash
# Installer:
- Docker Desktop
- Python 3.12+
- Node.js 20+
- Git
- VSCode (recommandé)
```

### Étape 1: Lancer l'infrastructure

```bash
# Terminal 1: Démarrer PostgreSQL + Redis
docker-compose up postgres redis

# Attendre que les services soient healthy (30 secondes)
# Vérifier: docker ps → STATUS = healthy
```

### Étape 2: Setup Backend

```bash
# Terminal 2: Backend
cd backend

# Créer venv
python -m venv venv

# Activer
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installer dependencies
pip install -r requirements-dev.txt

# Copier .env
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# IMPORTANT: Éditer .env avec tes vraies clés API:
# - BRIDGE_API_KEY
# - ANTHROPIC_API_KEY
# - SENDGRID_API_KEY
# - SECRET_KEY (générer: openssl rand -base64 32)
```

### Étape 3: Setup Frontend

```bash
# Terminal 3: Frontend
cd frontend

# Installer dependencies
npm install

# Copier .env
copy .env.local.example .env.local  # Windows
cp .env.local.example .env.local    # Mac/Linux

# Éditer .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Étape 4: Lancer le tout

```bash
# Option A: Docker Compose (TOUT EN UN)
docker-compose up

# Option B: Manuellement (plus flexible pour dev)

# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Celery Worker
cd backend
celery -A app.workers.celery_app worker --loglevel=info

# Terminal 3: Frontend
cd frontend
npm run dev
```

### Étape 5: Vérifier

```bash
# Backend: http://localhost:8000/docs (Swagger UI)
# Frontend: http://localhost:3000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

---

## 📋 JOUR 1: PREMIERS FICHIERS À CRÉER

### 1. Backend: Configuration & Database (2h)

```python
# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FinanceAI"
    DATABASE_URL: str
    SECRET_KEY: str
    # ... autres settings

    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME}

@app.get("/")
async def root():
    return {"message": "Welcome to FinanceAI API"}
```

**Test**:
```bash
cd backend
uvicorn app.main:app --reload

# Dans un autre terminal:
curl http://localhost:8000/health
# → {"status":"ok","app":"FinanceAI"}

# Ouvrir browser: http://localhost:8000/docs
# → Swagger UI visible ✅
```

---

### 2. Backend: Modèle User + Auth (3h)

```python
# backend/app/models/user.py
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    company_size = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
```

```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    company_name: str = Field(..., min_length=1, max_length=255)
    company_size: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: str
    company_name: str
    company_size: str | None
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

```python
# backend/app/core/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
```

```python
# backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead, Token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        company_name=user_data.company_name,
        company_size=user_data.company_size,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    # Find user
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Create token
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
```

```python
# backend/app/main.py (mettre à jour)
from app.api.v1 import auth

# Ajouter après app = FastAPI(...):
app.include_router(auth.router)
```

**Test**:
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "Test123!",
    "company_name": "Test Corp"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "Test123!"
  }'
# → {"access_token":"eyJ...","token_type":"bearer"}
```

---

## 🎯 CHECKPOINTS JOUR 1

- [ ] Docker: PostgreSQL + Redis running
- [ ] Backend: FastAPI app starts without errors
- [ ] Endpoint `/health` fonctionne
- [ ] Endpoint `/docs` affiche Swagger UI
- [ ] User model créé
- [ ] Auth endpoints: `/register` et `/login` fonctionnent
- [ ] Test: Créer user + login + recevoir JWT token

**Si tous les checks ✅** → Fin Jour 1 SUCCESS! 🎉

**NEXT**: Jour 2 → CRUD models (Bank, Transaction, Invoice)

---

## 📚 RESSOURCES

- **Plan complet**: `PLAN_DEV_CODE_FIRST.md`
- **Standards qualité**: `.cursorrules`
- **Database schema**: `database_schema.sql`

---

## 🆘 TROUBLESHOOTING

### Docker: "Cannot connect to Docker daemon"
```bash
# Démarrer Docker Desktop
# Windows: Ouvrir Docker Desktop app
# Mac: Ouvrir Docker.app
# Linux: sudo systemctl start docker
```

### PostgreSQL: "Connection refused"
```bash
# Vérifier que le container tourne
docker ps | grep postgres

# Si pas de container, lancer
docker-compose up postgres
```

### Python: "Module not found"
```bash
# Vérifier que venv est activé
which python  # Mac/Linux
where python  # Windows
# Doit pointer vers venv/bin/python

# Réinstaller dependencies
pip install -r requirements-dev.txt
```

### FastAPI: "Import error"
```bash
# Vérifier structure:
# backend/app/__init__.py doit exister (peut être vide)
# Créer si manquant:
touch backend/app/__init__.py  # Mac/Linux
echo. > backend\app\__init__.py  # Windows
```

---

**READY TO CODE? GO GO GO! 💪🔥**

