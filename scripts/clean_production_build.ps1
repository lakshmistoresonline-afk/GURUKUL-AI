# D:\GURUKUL-AI\scripts\clean_production_build.ps1

Write-Host "--- GURUKUL-AI: STARTING CLEAN PRODUCTION BUILD ---" -ForegroundColor Cyan

# 1. Backend Verification
Write-Host "[1/5] Verifying Backend Syntax..." -ForegroundColor Yellow
python -m compileall backend/src
if ($LASTEXITCODE -ne 0) { Write-Error "Syntax Error Detected"; exit 1 }

Write-Host "[2/5] Running Backend Logic Tests..." -ForegroundColor Yellow
cd backend
$env:PYTHONPATH="."
pytest tests/test_mastery_engine.py tests/test_content_integration.py
if ($LASTEXITCODE -ne 0) { Write-Error "Logic Tests Failed"; exit 1 }
cd ..

# 2. Content Validation
Write-Host "[3/5] Validating 163 Chapters..." -ForegroundColor Yellow
python scripts/validate_gurukul_content.py
# Check report for errors
$report = Get-Content GURUKUL_CONTENT_VALIDATION_REPORT.json | ConvertFrom-Json
if ($report.errors.Count -gt 0) { Write-Error "Content Validation Errors Found"; exit 1 }

# 3. Frontend Build
Write-Host "[4/5] Cleaning and Building Frontend..." -ForegroundColor Yellow
cd frontend-nextjs
npm run clean
npm run build
if ($LASTEXITCODE -ne 0) { Write-Error "Frontend Build Failed"; exit 1 }
cd ..

# 4. Security Scan
Write-Host "[5/5] Performing Final Secret Scan..." -ForegroundColor Yellow
python scripts/secret_scanner.py

Write-Host "`n=== CLEAN BUILD COMPLETED SUCCESSFULLY ===" -ForegroundColor Green
