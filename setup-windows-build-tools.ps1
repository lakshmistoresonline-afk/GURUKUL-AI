# ============================================================
# Gurukul AI - Windows Desktop Build Environment Setup
# ============================================================
# Run PowerShell as Administrator.
#
# Installs/checks:
#   - Git
#   - Node.js 20
#   - Rust / Cargo
#   - Visual Studio Build Tools / C++ workload
#   - Windows SDK
#   - WebView2
#   - Tauri prerequisites
#
# Does NOT modify Gurukul AI source code.
# Does NOT modify Firebase credentials.
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       GURUKUL AI WINDOWS BUILD ENVIRONMENT SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------
# Administrator check
# ------------------------------------------------------------

$principal = New-Object Security.Principal.WindowsPrincipal(
    [Security.Principal.WindowsIdentity]::GetCurrent()
)

if (-not $principal.IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator
)) {
    Write-Host "ERROR: Please run PowerShell as Administrator." -ForegroundColor Red
    Write-Host ""
    Write-Host "Right-click PowerShell -> Run as administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Running as Administrator" -ForegroundColor Green

# ------------------------------------------------------------
# Winget
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking Windows Package Manager..." -ForegroundColor Cyan

$winget = Get-Command winget -ErrorAction SilentlyContinue

if (-not $winget) {
    Write-Host "ERROR: winget is not available." -ForegroundColor Red
    Write-Host "Please update/install App Installer from Microsoft Store." -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] winget available" -ForegroundColor Green

# ------------------------------------------------------------
# Helper function
# ------------------------------------------------------------

function Install-WingetPackage {
    param(
        [string]$Id,
        [string]$Name
    )

    Write-Host ""
    Write-Host "Checking $Name..." -ForegroundColor Cyan

    $installed = winget list --id $Id --exact --accept-source-agreements 2>$null

    if ($installed -match $Id) {
        Write-Host "[OK] $Name already installed" -ForegroundColor Green
        return
    }

    Write-Host "Installing $Name..." -ForegroundColor Yellow

    winget install `
        --id $Id `
        --exact `
        --source winget `
        --accept-package-agreements `
        --accept-source-agreements `
        --silent

    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Installation returned exit code $LASTEXITCODE for $Name" -ForegroundColor Yellow
    }
    else {
        Write-Host "[OK] $Name installation completed" -ForegroundColor Green
    }
}

# ------------------------------------------------------------
# Git
# ------------------------------------------------------------

Install-WingetPackage `
    -Id "Git.Git" `
    -Name "Git"

# ------------------------------------------------------------
# Node.js 20 LTS
# ------------------------------------------------------------

Install-WingetPackage `
    -Id "OpenJS.NodeJS.20" `
    -Name "Node.js 20"

# ------------------------------------------------------------
# Visual Studio Build Tools
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking Visual Studio Build Tools..." -ForegroundColor Cyan

$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

$vsInstalled = $false

if (Test-Path $vswhere) {
    $vs = & $vswhere -products * `
        -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 `
        -latest 2>$null

    if ($vs) {
        $vsInstalled = $true
    }
}

if ($vsInstalled) {
    Write-Host "[OK] Visual Studio C++ Build Tools already installed" -ForegroundColor Green
}
else {
    Write-Host "Installing Visual Studio 2022 Build Tools..." -ForegroundColor Yellow

    winget install `
        --id "Microsoft.VisualStudio.2022.BuildTools" `
        --exact `
        --source winget `
        --accept-package-agreements `
        --accept-source-agreements `
        --override "--quiet --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Visual Studio Build Tools installer returned $LASTEXITCODE" -ForegroundColor Yellow
    }
    else {
        Write-Host "[OK] Visual Studio Build Tools installed" -ForegroundColor Green
    }
}

# ------------------------------------------------------------
# Rust
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking Rust / Cargo..." -ForegroundColor Cyan

$cargoPath = "$env:USERPROFILE\.cargo\bin\cargo.exe"
$rustupPath = "$env:USERPROFILE\.cargo\bin\rustup.exe"

if (Test-Path $cargoPath) {
    Write-Host "[OK] Rust/Cargo already installed" -ForegroundColor Green
}
else {
    Write-Host "Installing Rust using rustup..." -ForegroundColor Yellow

    $rustupInstaller = "$env:TEMP\rustup-init.exe"

    Invoke-WebRequest `
        -Uri "https://win.rustup.rs/x86_64" `
        -OutFile $rustupInstaller

    & $rustupInstaller -y

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Rust installation failed." -ForegroundColor Red
        exit 1
    }

    Write-Host "[OK] Rust installation completed" -ForegroundColor Green
}

# ------------------------------------------------------------
# Add Cargo to current PATH
# ------------------------------------------------------------

Write-Host ""
Write-Host "Configuring Rust PATH..." -ForegroundColor Cyan

$cargoBin = "$env:USERPROFILE\.cargo\bin"

if (-not ($env:Path -split ";" | Where-Object {
    $_.TrimEnd("\") -eq $cargoBin.TrimEnd("\")
})) {
    $env:Path = "$cargoBin;$env:Path"
}

# Persist user PATH if required
$userPath = [Environment]::GetEnvironmentVariable(
    "Path",
    [EnvironmentVariableTarget]::User
)

if (-not ($userPath -split ";" | Where-Object {
    $_.TrimEnd("\") -eq $cargoBin.TrimEnd("\")
})) {

    [Environment]::SetEnvironmentVariable(
        "Path",
        "$cargoBin;$userPath",
        [EnvironmentVariableTarget]::User
    )

    Write-Host "[OK] Cargo added to user PATH" -ForegroundColor Green
}
else {
    Write-Host "[OK] Cargo already in user PATH" -ForegroundColor Green
}

# ------------------------------------------------------------
# Rust stable toolchain
# ------------------------------------------------------------

Write-Host ""
Write-Host "Configuring Rust stable toolchain..." -ForegroundColor Cyan

if (Test-Path $rustupPath) {

    & $rustupPath toolchain install stable

    & $rustupPath default stable

    & $rustupPath component add rust-src

    Write-Host "[OK] Rust stable configured" -ForegroundColor Green
}

# ------------------------------------------------------------
# WebView2
# ------------------------------------------------------------

Write-Host ""
Write-Host "Checking Microsoft Edge WebView2..." -ForegroundColor Cyan

$webviewInstalled = $false

$webviewPaths = @(
    "${env:ProgramFiles(x86)}\Microsoft\EdgeWebView\Application",
    "${env:ProgramFiles}\Microsoft\EdgeWebView\Application"
)

foreach ($path in $webviewPaths) {
    if (Test-Path $path) {
        $webviewInstalled = $true
        break
    }
}

if ($webviewInstalled) {
    Write-Host "[OK] WebView2 detected" -ForegroundColor Green
}
else {
    Write-Host "Installing WebView2 Runtime..." -ForegroundColor Yellow

    winget install `
        --id "Microsoft.EdgeWebView2Runtime" `
        --exact `
        --source winget `
        --accept-package-agreements `
        --accept-source-agreements `
        --silent

    Write-Host "[OK] WebView2 installation attempted" -ForegroundColor Green
}

# ------------------------------------------------------------
# Refresh PATH
# ------------------------------------------------------------

Write-Host ""
Write-Host "Refreshing environment..." -ForegroundColor Cyan

$machinePath = [Environment]::GetEnvironmentVariable(
    "Path",
    [EnvironmentVariableTarget]::Machine
)

$userPath = [Environment]::GetEnvironmentVariable(
    "Path",
    [EnvironmentVariableTarget]::User
)

$env:Path = "$userPath;$machinePath"

# Ensure Cargo is present
if (Test-Path $cargoBin) {
    $env:Path = "$cargoBin;$env:Path"
}

# ------------------------------------------------------------
# Verification
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "                 TOOLCHAIN VERIFICATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Git:" -ForegroundColor White
git --version

Write-Host ""
Write-Host "Node:" -ForegroundColor White
node --version

Write-Host ""
Write-Host "NPM:" -ForegroundColor White
npm --version

Write-Host ""
Write-Host "Rust:" -ForegroundColor White
rustc --version

Write-Host ""
Write-Host "Cargo:" -ForegroundColor White
cargo --version

Write-Host ""
Write-Host "Rustup:" -ForegroundColor White
rustup --version

Write-Host ""
Write-Host "Cargo location:" -ForegroundColor White
where.exe cargo

Write-Host ""
Write-Host "Rustup status:" -ForegroundColor White
rustup show

# ------------------------------------------------------------
# Visual C++ detection
# ------------------------------------------------------------

Write-Host ""
Write-Host "Visual Studio C++ Build Tools:" -ForegroundColor White

if (Test-Path $vswhere) {

    $vsInfo = & $vswhere `
        -products * `
        -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 `
        -latest `
        -property installationPath 2>$null

    if ($vsInfo) {
        Write-Host "[OK] C++ Build Tools detected:" -ForegroundColor Green
        Write-Host $vsInfo
    }
    else {
        Write-Host "[WARNING] C++ Build Tools not detected." -ForegroundColor Yellow
    }
}
else {
    Write-Host "[WARNING] vswhere.exe not found." -ForegroundColor Yellow
}

# ------------------------------------------------------------
# Final
# ------------------------------------------------------------

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "           WINDOWS BUILD ENVIRONMENT CHECK COMPLETE" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "Close this PowerShell window and open a NEW Administrator PowerShell"
Write-Host "before running the Gurukul AI Tauri build."
Write-Host ""

Write-Host "Then run:" -ForegroundColor Cyan
Write-Host ""
Write-Host "cd D:\GURUKUL-AI\frontend-nextjs"
Write-Host "npm run build"
Write-Host ""
Write-Host "cd D:\GURUKUL-AI\desktop"
Write-Host "npm run build"
Write-Host ""

Write-Host "============================================================" -ForegroundColor Green