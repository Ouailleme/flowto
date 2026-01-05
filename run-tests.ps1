# Script PowerShell pour lancer les tests E2E automatiquement

Write-Host "🚀 FinanceAI - Lancement des Tests E2E" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Créer .env pour backend si n'existe pas
if (-not (Test-Path "backend\.env")) {
    Write-Host "📝 Création backend\.env..." -ForegroundColor Yellow
    @"
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/financeai
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
SECRET_KEY=dev-secret-key-change-in-production-12345678
ACCESS_TOKEN_EXPIRE_MINUTES=10080
BRIDGE_API_KEY=mock-bridge-key
BRIDGE_CLIENT_ID=mock-client-id
BRIDGE_CLIENT_SECRET=mock-client-secret
CLAUDE_API_KEY=mock-claude-key
SENDGRID_API_KEY=mock-sendgrid-key
EXCHANGE_RATE_API_KEY=mock-exchange-rate-key
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
"@ | Out-File -FilePath "backend\.env" -Encoding utf8
    Write-Host "✅ backend\.env créé" -ForegroundColor Green
}

# Créer .env.local pour frontend si n'existe pas
if (-not (Test-Path "frontend\.env.local")) {
    Write-Host "📝 Création frontend\.env.local..." -ForegroundColor Yellow
    @"
NEXT_PUBLIC_API_URL=http://localhost:8000
"@ | Out-File -FilePath "frontend\.env.local" -Encoding utf8
    Write-Host "✅ frontend\.env.local créé" -ForegroundColor Green
}

Write-Host ""
Write-Host "🐳 Démarrage Docker (PostgreSQL + Redis)..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "⏳ Attente que PostgreSQL soit prêt (5 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "🔥 Backend sera lancé sur http://localhost:8000" -ForegroundColor Green
Write-Host "🎨 Frontend sera lancé sur http://localhost:3000" -ForegroundColor Green
Write-Host "🧪 Tests E2E vont démarrer automatiquement" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📖 Ouvrir TEST_RUNNER.md pour plus d'infos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Instructions pour l'utilisateur
Write-Host "⚠️  PROCHAINES ÉTAPES MANUELLES:" -ForegroundColor Red
Write-Host ""
Write-Host "Terminal 1 - Backend:" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  python -m venv venv" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  pip install -r requirements.txt" -ForegroundColor White
Write-Host "  uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 2 - Tests E2E:" -ForegroundColor Yellow
Write-Host "  cd frontend" -ForegroundColor White
Write-Host "  npm run test:e2e:ui" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Ensuite les tests vont se lancer automatiquement!" -ForegroundColor Green


