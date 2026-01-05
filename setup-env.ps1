# Simple script pour créer les fichiers .env

Write-Host "📝 Création des fichiers d'environnement..." -ForegroundColor Yellow

# Backend .env
$backendEnv = @"
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/financeai
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
SECRET_KEY=dev-secret-key-12345678
ACCESS_TOKEN_EXPIRE_MINUTES=10080
BRIDGE_API_KEY=mock-key
BRIDGE_CLIENT_ID=mock-id
BRIDGE_CLIENT_SECRET=mock-secret
CLAUDE_API_KEY=mock-key
SENDGRID_API_KEY=mock-key
EXCHANGE_RATE_API_KEY=mock-key
CORS_ORIGINS=http://localhost:3000
"@

$backendEnv | Out-File -FilePath "backend\.env" -Encoding utf8 -NoNewline
Write-Host "✅ backend\.env créé" -ForegroundColor Green

# Frontend .env.local
"NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath "frontend\.env.local" -Encoding utf8 -NoNewline
Write-Host "✅ frontend\.env.local créé" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Fichiers créés avec succès!" -ForegroundColor Green


