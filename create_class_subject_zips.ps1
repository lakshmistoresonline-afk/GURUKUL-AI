$ErrorActionPreference = "Stop"

$Root = "D:\GURUKUL-AI"
$Contents = Join-Path $Root "Contents"
$OutputRoot = Join-Path $Root "GURUKUL_CONTENT_PACKS"
$StageRoot = Join-Path $Root "_GURUKUL_CONTENT_STAGE"

Write-Host ""
Write-Host "=========================================================="
Write-Host " GURUKUL AI - CLASS + SUBJECT CONTENT PACK CREATOR"
Write-Host "=========================================================="
Write-Host ""

if (-not (Test-Path $Contents)) {
    throw "Contents folder not found: $Contents"
}

# Clean previous output.
if (Test-Path $OutputRoot) {
    Remove-Item $OutputRoot -Recurse -Force
}

if (Test-Path $StageRoot) {
    Remove-Item $StageRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
New-Item -ItemType Directory -Path $StageRoot -Force | Out-Null

$Classes = @(
    "Class 5",
    "Class 6",
    "Class 7"
)

$totalPacks = 0
$totalFiles = 0

foreach ($Class in $Classes) {

    $ClassSource = Join-Path $Contents $Class

    if (-not (Test-Path $ClassSource)) {
        Write-Warning "Skipping missing class: $Class"
        continue
    }

    Write-Host ""
    Write-Host "=========================================================="
    Write-Host " $Class"
    Write-Host "=========================================================="

    $ClassOutput = Join-Path $OutputRoot ($Class -replace " ", "_")
    $ClassStage = Join-Path $StageRoot ($Class -replace " ", "_")

    New-Item -ItemType Directory -Path $ClassOutput -Force | Out-Null
    New-Item -ItemType Directory -Path $ClassStage -Force | Out-Null

    # Find subject directories immediately under the class.
    $Subjects = Get-ChildItem `
        -Path $ClassSource `
        -Directory `
        -Force |
        Where-Object {
            $_.Name -notin @(
                ".git",
                "node_modules",
                "__pycache__",
                ".next"
            )
        }

    if ($Subjects.Count -eq 0) {
        Write-Warning "No subject directories found in $Class"
        continue
    }

    foreach ($Subject in $Subjects) {

        $SubjectName = $Subject.Name

        # Safe filename.
        $SafeSubjectName = $SubjectName -replace '[<>:"/\\|?*]', '_'
        $SafeSubjectName = $SafeSubjectName.Trim()

        if ([string]::IsNullOrWhiteSpace($SafeSubjectName)) {
            $SafeSubjectName = "Subject"
        }

        Write-Host ""
        Write-Host "  SUBJECT: $SubjectName"

        $SubjectStage = Join-Path $ClassStage $SafeSubjectName
        $SubjectZip = Join-Path $ClassOutput "$SafeSubjectName.zip"

        New-Item -ItemType Directory -Path $SubjectStage -Force | Out-Null

        # Copy only source files.
        Get-ChildItem `
            -Path $Subject.FullName `
            -Recurse `
            -File `
            -Force |
            Where-Object {

                $_.FullName -notmatch '\\\.git\\' -and
                $_.FullName -notmatch '\\node_modules\\' -and
                $_.FullName -notmatch '\\__pycache__\\' -and
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

                $Relative = $_.FullName.Substring(
                    $Subject.FullName.Length
                ).TrimStart('\')

                $Target = Join-Path $SubjectStage $Relative
                $TargetDir = Split-Path $Target -Parent

                if (-not (Test-Path $TargetDir)) {
                    New-Item `
                        -ItemType Directory `
                        -Path $TargetDir `
                        -Force |
                        Out-Null
                }

                Copy-Item `
                    -Path $_.FullName `
                    -Destination $Target `
                    -Force
            }

        $SubjectFiles = @(Get-ChildItem $SubjectStage -Recurse -File)

        if ($SubjectFiles.Count -eq 0) {
            Write-Warning "    No files found - ZIP not created."
            Remove-Item $SubjectStage -Recurse -Force
            continue
        }

        $SubjectFileCount = $SubjectFiles.Count

        Write-Host "    Files: $SubjectFileCount"

        # Create subject ZIP.
        Compress-Archive `
            -Path (Join-Path $SubjectStage "*") `
            -DestinationPath $SubjectZip `
            -CompressionLevel Optimal `
            -Force

        if (-not (Test-Path $SubjectZip)) {
            throw "Failed to create: $SubjectZip"
        }

        $ZipSize = [math]::Round(
            (Get-Item $SubjectZip).Length / 1MB,
            2
        )

        Write-Host "    CREATED: $SubjectZip"
        Write-Host "    SIZE   : $ZipSize MB"

        $totalPacks++
        $totalFiles += $SubjectFileCount
    }
}

# Remove staging.
Remove-Item $StageRoot -Recurse -Force

Write-Host ""
Write-Host "=========================================================="
Write-Host " COMPLETE"
Write-Host "=========================================================="
Write-Host ""
Write-Host "Output directory:"
Write-Host "  $OutputRoot"
Write-Host ""
Write-Host "Subject ZIP packages:"
Write-Host "  $totalPacks"
Write-Host ""
Write-Host "Source files packaged:"
Write-Host "  $totalFiles"
Write-Host ""

Write-Host "PACKAGE TREE:"
Get-ChildItem $OutputRoot -Recurse -File |
    Select-Object FullName, Length |
    Format-Table -AutoSize

Write-Host ""
Write-Host "IMPORTANT:"
Write-Host "  Only Contents data was packaged."
Write-Host "  Firebase credentials were NOT included."
Write-Host "  .env files were NOT intentionally included."
Write-Host "  Database files were NOT included."
Write-Host "  node_modules were excluded."
Write-Host "  .git data was excluded."
Write-Host ""
Write-Host "GURUKUL_CONTENT_PACK_CREATION_PASS"
