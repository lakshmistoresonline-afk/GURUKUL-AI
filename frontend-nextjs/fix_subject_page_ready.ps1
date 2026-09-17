$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " GURUKUL AI - SUBJECT PAGE RUNTIME FIX" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------
# 1. Resolve project
# ------------------------------------------------------------

$ProjectRoot = "D:\GURUKUL-AI\frontend-nextjs"
$File = Join-Path $ProjectRoot "src\app\subject\[subjectId]\page.tsx"

if (-not (Test-Path -LiteralPath $File)) {
    Write-Host "ERROR: Subject page not found:" -ForegroundColor Red
    Write-Host $File
    exit 1
}

Set-Location $ProjectRoot

Write-Host "[1/5] Subject page found." -ForegroundColor Green
Write-Host $File
Write-Host ""

# ------------------------------------------------------------
# 2. Create timestamped backup
# ------------------------------------------------------------

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Backup = "$File.backup_$Timestamp"

Copy-Item -LiteralPath $File -Destination $Backup -Force

Write-Host "[2/5] Backup created:" -ForegroundColor Green
Write-Host $Backup
Write-Host ""

# ------------------------------------------------------------
# 3. Read source
# ------------------------------------------------------------

$Content = Get-Content -LiteralPath $File | Out-String

# ------------------------------------------------------------
# 4. Patch the existing subject loading effect
# ------------------------------------------------------------

$OldEffect = @'
  useEffect(() => {
    if (subjectId) {
      studentApi.getSubject(subjectId).then(res => {
        setSubject(res);
        setLoading(false);
      }).catch(err => {
        console.error("Failed to load subject", err);
        setLoading(false);
      });
    }
  }, [subjectId]);
'@

$NewEffect = @'
  useEffect(() => {
    if (!subjectId) return;

    // Reset readiness while a subject is loading.
    document.body.removeAttribute('data-gurukul-ready');

    studentApi.getSubject(subjectId)
      .then(res => {
        setSubject(res);
        setLoading(false);

        // Canonical production-readiness contract.
        // The page is ready only after a valid subject is loaded.
        document.body.setAttribute('data-gurukul-ready', 'true');
      })
      .catch(err => {
        console.error("Failed to load subject", err);
        setLoading(false);

        // Failed subject loads must never report the page as ready.
        document.body.removeAttribute('data-gurukul-ready');
      });

    return () => {
      document.body.removeAttribute('data-gurukul-ready');
    };
  }, [subjectId]);
'@

if (-not $Content.Contains($OldEffect)) {
    Write-Host "ERROR: Expected subject loading effect was not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "The file may already have been modified, or its structure differs." -ForegroundColor Yellow
    Write-Host "Backup remains available at:" -ForegroundColor Yellow
    Write-Host $Backup
    exit 2
}

$Content = $Content.Replace($OldEffect, $NewEffect)

# ------------------------------------------------------------
# 5. Write and verify
# ------------------------------------------------------------

Set-Content -LiteralPath $File -Value $Content -Encoding UTF8

$Verify = Get-Content -LiteralPath $File | Out-String

$RequiredMarkers = @(
    "document.body.removeAttribute('data-gurukul-ready');",
    "document.body.setAttribute('data-gurukul-ready', 'true');",
    "The page is ready only after a valid subject is loaded."
)

foreach ($Marker in $RequiredMarkers) {
    if (-not $Verify.Contains($Marker)) {
        Write-Host "ERROR: Verification failed for marker:" -ForegroundColor Red
        Write-Host $Marker
        exit 3
    }
}

Write-Host "[3/5] Subject page patched successfully." -ForegroundColor Green
Write-Host ""

# ------------------------------------------------------------
# Show patched effect
# ------------------------------------------------------------

Write-Host "[4/5] Verifying patched useEffect..." -ForegroundColor Cyan
Write-Host ""

$Lines = Get-Content -LiteralPath $File

$Start = -1
$End = -1

for ($i = 0; $i -lt $Lines.Count; $i++) {
    if ($Lines[$i] -match "useEffect\(\(\) =>") {
        $Start = $i
        break
    }
}

if ($Start -ge 0) {
    for ($i = $Start; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match "\}, \[subjectId\]\);") {
            $End = $i
            break
        }
    }
}

if ($Start -ge 0 -and $End -ge $Start) {
    $Lines[$Start..$End] | ForEach-Object {
        Write-Host $_
    }
}

Write-Host ""

# ------------------------------------------------------------
# TypeScript validation
# ------------------------------------------------------------

Write-Host "[5/5] Running TypeScript validation..." -ForegroundColor Cyan
Write-Host ""

npx tsc --noEmit

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "TYPECHECK FAILED." -ForegroundColor Red
    Write-Host "Restoring backup..." -ForegroundColor Yellow

    Copy-Item -LiteralPath $Backup -Destination $File -Force

    Write-Host "Original file restored." -ForegroundColor Yellow
    exit 4
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host " SUBJECT PAGE FIX COMPLETE" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host ""
Write-Host "TypeScript: PASS" -ForegroundColor Green
Write-Host "Backup    : $Backup" -ForegroundColor Gray
Write-Host ""
Write-Host "The subject page now exposes:" -ForegroundColor Cyan
Write-Host "  data-gurukul-ready=true" -ForegroundColor White
Write-Host "only after a valid subject has loaded." -ForegroundColor White
Write-Host ""
Write-Host "Next: run the four Phase-10 Playwright tests." -ForegroundColor Cyan
Write-Host ""