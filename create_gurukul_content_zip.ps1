$ErrorActionPreference = "Stop"

$Root = "D:\GURUKUL-AI"
$Contents = Join-Path $Root "Contents"
$Output = Join-Path $Root "GURUKUL_CONTENTS_CURRENT.zip"
$Temp = Join-Path $Root "_CONTENT_ZIP_STAGE"

Write-Host ""
Write-Host "==============================================="
Write-Host " GURUKUL AI - CONTENT SOURCE ZIP CREATOR"
Write-Host "==============================================="
Write-Host ""

if (-not (Test-Path $Contents)) {
    throw "Contents folder not found: $Contents"
}

# Remove previous staging directory.
if (Test-Path $Temp) {
    Remove-Item $Temp -Recurse -Force
}

# Remove previous ZIP.
if (Test-Path $Output) {
    Remove-Item $Output -Force
}

New-Item -ItemType Directory -Path $Temp | Out-Null

Write-Host "[1/6] Checking canonical class directories..."

$Classes = @(
    "Class 5",
    "Class 6",
    "Class 7"
)

foreach ($Class in $Classes) {
    $ClassPath = Join-Path $Contents $Class

    if (-not (Test-Path $ClassPath)) {
        throw "Missing canonical class directory: $ClassPath"
    }

    Write-Host "       OK: $Class"
}

Write-Host ""
Write-Host "[2/6] Copying canonical content..."

foreach ($Class in $Classes) {

    $Source = Join-Path $Contents $Class
    $Destination = Join-Path $Temp $Class

    New-Item -ItemType Directory -Path $Destination -Force | Out-Null

    # Copy only files. Exclusions below protect against temporary/generated
    # material being accidentally included in the source package.
    Get-ChildItem -Path $Source -Recurse -File |
        Where-Object {
            $_.FullName -notmatch '\\node_modules\\' -and
            $_.FullName -notmatch '\\\.git\\' -and
            $_.FullName -notmatch '\\__pycache__\\' -and
            $_.FullName -notmatch '\\\.pytest_cache\\' -and
            $_.FullName -notmatch '\\\.next\\' -and
            $_.FullName -notmatch '\\dist\\' -and
            $_.FullName -notmatch '\\build\\' -and
            $_.Name -notmatch '^\.DS_Store$' -and
            $_.Name -notmatch '^Thumbs\.db$' -and
            $_.Name -notmatch '\.tmp$' -and
            $_.Name -notmatch '\.bak$' -and
            $_.Name -notmatch '\.log$'
        } |
        ForEach-Object {

            $Relative = $_.FullName.Substring($Source.Length).TrimStart('\')
            $TargetFile = Join-Path $Destination $Relative
            $TargetDirectory = Split-Path $TargetFile -Parent

            if (-not (Test-Path $TargetDirectory)) {
                New-Item -ItemType Directory -Path $TargetDirectory -Force | Out-Null
            }

            Copy-Item $_.FullName $TargetFile -Force
        }
}

Write-Host ""
Write-Host "[3/6] Counting source files..."

$Files = Get-ChildItem $Temp -Recurse -File

$Class5Files = @(Get-ChildItem (Join-Path $Temp "Class 5") -Recurse -File).Count
$Class6Files = @(Get-ChildItem (Join-Path $Temp "Class 6") -Recurse -File).Count
$Class7Files = @(Get-ChildItem (Join-Path $Temp "Class 7") -Recurse -File).Count
$TotalFiles = $Files.Count

Write-Host "       Class 5 files : $Class5Files"
Write-Host "       Class 6 files : $Class6Files"
Write-Host "       Class 7 files : $Class7Files"
Write-Host "       Total files   : $TotalFiles"

if ($TotalFiles -eq 0) {
    throw "No source files were found."
}

Write-Host ""
Write-Host "[4/6] Creating ZIP..."

Compress-Archive `
    -Path (Join-Path $Temp "*") `
    -DestinationPath $Output `
    -CompressionLevel Optimal `
    -Force

if (-not (Test-Path $Output)) {
    throw "ZIP creation failed."
}

Write-Host ""
Write-Host "[5/6] Verifying ZIP..."

$ZipInfo = Get-Item $Output
$ZipSizeMB = [math]::Round($ZipInfo.Length / 1MB, 2)

Add-Type -AssemblyName System.IO.Compression.FileSystem

$Archive = [System.IO.Compression.ZipFile]::OpenRead($Output)

try {
    $Entries = @($Archive.Entries | Where-Object {
        -not [string]::IsNullOrWhiteSpace($_.Name)
    })

    $ZipEntryCount = $Entries.Count

    Write-Host "       ZIP entries : $ZipEntryCount"
    Write-Host "       ZIP size    : $ZipSizeMB MB"

    if ($ZipEntryCount -eq 0) {
        throw "ZIP contains no files."
    }

    # Verify all three canonical class roots exist in the archive.
    foreach ($Class in $Classes) {

        $Found = $Entries | Where-Object {
            $_.FullName -like "$Class/*" -or
            $_.FullName -like "$Class\*"
        }

        if (-not $Found) {
            throw "ZIP verification failed: $Class is missing."
        }

        Write-Host "       ZIP contains : $Class"
    }
}
finally {
    $Archive.Dispose()
}

Write-Host ""
Write-Host "[6/6] Cleaning staging directory..."

Remove-Item $Temp -Recurse -Force

Write-Host ""
Write-Host "==============================================="
Write-Host " CONTENT SOURCE ZIP CREATED SUCCESSFULLY"
Write-Host "==============================================="
Write-Host ""
Write-Host "Output:"
Write-Host "  $Output"
Write-Host ""
Write-Host "Files:"
Write-Host "  Class 5 : $Class5Files"
Write-Host "  Class 6 : $Class6Files"
Write-Host "  Class 7 : $Class7Files"
Write-Host "  Total   : $TotalFiles"
Write-Host ""
Write-Host "ZIP size:"
Write-Host "  $ZipSizeMB MB"
Write-Host ""
Write-Host "IMPORTANT:"
Write-Host "  This ZIP contains Contents only."
Write-Host "  It does NOT contain Firebase credentials."
Write-Host "  It does NOT contain the backend database."
Write-Host "  It does NOT contain node_modules."
Write-Host "  It does NOT contain .git."
Write-Host ""
