# ============================================================
# GURUKUL AI
# PERMANENT PACKAGE NAMING CONVENTION MIGRATION
#
# Scope:
#   D:\GURUKUL-AI\Contents\Class 5
#   D:\GURUKUL-AI\Contents\Class 6
#   D:\GURUKUL-AI\Contents\Class 7
#
# DEFAULT MODE:
#   DRY RUN
#
# To actually rename after reviewing the plan:
#   .\migrate_gurukul_naming.ps1 -Execute
#
# SAFETY:
#   - Only renames existing MASTER PACKAGE directories
#   - Does NOT rename source files
#   - Does NOT rename curriculum files
#   - Does NOT rename chapter directories
#   - Does NOT modify runtime-data
#   - Does NOT modify processors
#   - Does NOT modify audit files
#   - Does NOT modify package contents
#   - Does NOT delete anything
# ============================================================

param(
    [switch]$Execute
)

$ErrorActionPreference = "Stop"

# ============================================================
# CONFIGURATION
# ============================================================

$ProjectRoot  = "D:\GURUKUL-AI"
$ContentsRoot = Join-Path $ProjectRoot "Contents"

$ManifestPath = Join-Path $ProjectRoot "NAMING_MIGRATION_MANIFEST.csv"
$ConventionPath = Join-Path $ProjectRoot "NAMING_CONVENTION.json"

# ============================================================
# HEADER
# ============================================================

Write-Host ""
Write-Host "============================================================"
Write-Host " GURUKUL AI - PERMANENT NAMING CONVENTION MIGRATION"
Write-Host "============================================================"
Write-Host ""

Write-Host "Project Root : $ProjectRoot"
Write-Host "Contents Root: $ContentsRoot"

if ($Execute) {
    Write-Host "Mode         : EXECUTE"
}
else {
    Write-Host "Mode         : DRY RUN"
}

Write-Host ""

# ============================================================
# ROOT VALIDATION
# ============================================================

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
    throw "Project root does not exist: $ProjectRoot"
}

if (-not (Test-Path -LiteralPath $ContentsRoot -PathType Container)) {
    throw "Contents root does not exist: $ContentsRoot"
}

# ============================================================
# PERMANENT NAMING CONVENTION
# ============================================================

$NamingConvention = [ordered]@{

    schema_version = "1.0"

    project = "GURUKUL-AI"

    artifact_pattern = "<TYPE>__C<CLASS>__<SUBJECT>__<TEXTBOOK>__P<PART>__V<VERSION>"

    artifact_types = [ordered]@{
        SOURCE    = "Authoritative curriculum source"
        MASTER    = "Generated canonical/master package"
        PROCESSED = "Processor-generated intermediate/output"
        RUNTIME   = "Runtime projection/cache"
        AUDIT     = "Audit and verification artifacts"
        ARCHIVE   = "Historical frozen artifact"
    }

    subjects = @(
        "ENGLISH"
        "HINDI"
        "MATHEMATICS"
        "EVS"
        "SCIENCE"
        "SOCIAL_SCIENCE"
    )

    part_rule = [ordered]@{
        P00 = "Single-volume / no explicit part"
        P01 = "Part 1"
        P02 = "Part 2"
        P03 = "Part 3"
        P04 = "Part 4"
        P05 = "Part 5"
        P06 = "Part 6"
    }

    authority = [ordered]@{
        SOURCE    = "AUTHORITATIVE"
        MASTER    = "NON_AUTHORITATIVE_GENERATED"
        PROCESSED = "NON_AUTHORITATIVE_GENERATED"
        RUNTIME   = "NON_AUTHORITATIVE_RUNTIME"
        AUDIT     = "VERIFICATION"
        ARCHIVE   = "HISTORICAL"
    }

    rules = @(
        "SOURCE is authoritative curriculum input."
        "MASTER is generated output and is never authoritative source."
        "PROCESSED is generated/intermediate output."
        "RUNTIME is never authoritative source."
        "AUDIT contains verification artifacts."
        "ARCHIVE contains historical frozen artifacts."
        "Class is represented as C##."
        "Subject uses one canonical identifier."
        "MATHEMATICS is the canonical Mathematics identifier."
        "SOCIAL_SCIENCE is the canonical Social Science identifier."
        "Part is represented separately as P##."
        "P00 means single-volume/non-partitioned."
        "Part numbers must never become separate logical subjects."
        "Generated artifact version must not be interpreted as textbook edition."
        "Textbook names must come from actual source/package metadata."
        "Do not invent textbook names."
        "Existing package contents must not be modified during naming migration."
    )

    migration_scope = "MASTER package directories only"

    classes = @(
        "C05"
        "C06"
        "C07"
    )
}

# ============================================================
# WRITE NAMING CONVENTION
# ============================================================

$NamingConvention |
    ConvertTo-Json -Depth 10 |
    Set-Content -LiteralPath $ConventionPath -Encoding UTF8

Write-Host "Naming convention written to:"
Write-Host "  $ConventionPath"
Write-Host ""

# ============================================================
# FUNCTION:
# CANONICAL SUBJECT + TEXTBOOK EXTRACTION
# ============================================================

function Get-SubjectAndTextbook {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Body
    )

    # --------------------------------------------------------
    # SOCIAL SCIENCE
    # --------------------------------------------------------

    if ($Body -match '^Social_Science_(.+)$') {

        return [PSCustomObject]@{
            Subject  = "SOCIAL_SCIENCE"
            Remaining = $Matches[1]
        }
    }

    # --------------------------------------------------------
    # MATHEMATICS
    # --------------------------------------------------------

    if ($Body -match '^Mathematics_(.+)$') {

        return [PSCustomObject]@{
            Subject  = "MATHEMATICS"
            Remaining = $Matches[1]
        }
    }

    if ($Body -match '^Maths_(.+)$') {

        return [PSCustomObject]@{
            Subject  = "MATHEMATICS"
            Remaining = $Matches[1]
        }
    }

    # --------------------------------------------------------
    # ENGLISH
    # --------------------------------------------------------

    if ($Body -match '^English_(.+)$') {

        return [PSCustomObject]@{
            Subject  = "ENGLISH"
            Remaining = $Matches[1]
        }
    }

    # --------------------------------------------------------
    # HINDI
    # --------------------------------------------------------

    if ($Body -match '^Hindi_(.+)$') {

        return [PSCustomObject]@{
            Subject  = "HINDI"
            Remaining = $Matches[1]
        }
    }

    # --------------------------------------------------------
    # SCIENCE
    # --------------------------------------------------------

    if ($Body -match '^Science_(.+)$') {

        return [PSCustomObject]@{
            Subject  = "SCIENCE"
            Remaining = $Matches[1]
        }
    }

    # --------------------------------------------------------
    # EVS
    # --------------------------------------------------------

    if ($Body -match '^EVS_(.+)$') {

        return [PSCustomObject]@{
            Subject  = "EVS"
            Remaining = $Matches[1]
        }
    }

    return $null
}

# ============================================================
# FUNCTION:
# NORMALIZE TEXTBOOK NAME
# ============================================================

function Normalize-Textbook {
    param(
        [string]$Textbook
    )

    if ([string]::IsNullOrWhiteSpace($Textbook)) {
        return "UNSPECIFIED"
    }

    $Result = $Textbook.ToUpperInvariant()

    # Replace spaces/hyphens with underscore.
    $Result = $Result -replace '[\s\-]+', '_'

    # Remove unsupported characters.
    $Result = $Result -replace '[^A-Z0-9_]', '_'

    # Collapse repeated underscores.
    $Result = $Result -replace '_+', '_'

    # Trim underscores.
    $Result = $Result.Trim('_')

    if ([string]::IsNullOrWhiteSpace($Result)) {
        return "UNSPECIFIED"
    }

    return $Result
}

# ============================================================
# DISCOVER CLASS DIRECTORIES
# ============================================================

$ClassNumbers = @(5, 6, 7)

$Plan = @()

foreach ($ClassNumber in $ClassNumbers) {

    $ClassRoot = Join-Path $ContentsRoot ("Class {0}" -f $ClassNumber)

    if (-not (Test-Path -LiteralPath $ClassRoot -PathType Container)) {

        Write-Warning "Class directory not found:"
        Write-Warning "  $ClassRoot"

        continue
    }

    Write-Host "Scanning:"
    Write-Host "  $ClassRoot"
    Write-Host ""

    # Only immediate child directories.
    # We deliberately do NOT recursively rename folders.
    $Folders = Get-ChildItem `
        -LiteralPath $ClassRoot `
        -Directory `
        -ErrorAction Stop

    foreach ($Folder in $Folders) {

        $OldName = $Folder.Name

        # ====================================================
        # ONLY MATCH GENERATED MASTER PACKAGE DIRECTORIES
        # ====================================================

        if ($OldName -notmatch '^Class(?<Class>[567])_(?<Body>.+)_Master_Package_v(?<Version>[0-9]+)$') {
            continue
        }

        $DetectedClass = [int]$Matches["Class"]
        $Body          = $Matches["Body"]
        $Version       = [int]$Matches["Version"]

        # ====================================================
        # DETERMINE SUBJECT
        # ====================================================

        $SubjectResult = Get-SubjectAndTextbook -Body $Body

        if ($null -eq $SubjectResult) {

            $Plan += [PSCustomObject]@{
                Status    = "REVIEW"
                Class     = "C{0:D2}" -f $DetectedClass
                Subject   = "UNKNOWN"
                Textbook  = "UNSPECIFIED"
                Part      = "P00"
                Version   = "V{0:D2}" -f $Version
                OldName   = $OldName
                NewName   = ""
                OldPath   = $Folder.FullName
                NewPath   = ""
                Reason    = "Subject could not be safely identified"
            }

            continue
        }

        $Subject   = $SubjectResult.Subject
        $Remaining = $SubjectResult.Remaining

        # ====================================================
        # REMOVE ARTIFACT DESCRIPTION
        # ====================================================

        # "Revised" describes generated artifact history.
        # It is NOT part of textbook identity.
        $Remaining = $Remaining -replace '_Revised$', ''

        # ====================================================
        # DETECT PART
        #
        # Handles:
        #
        # Part1
        # Part2
        # Part_1
        # Part_2
        # _Part1
        # _Part2
        # ====================================================

        $PartNumber = 0

        if ($Remaining -match '^(?<Book>.*?)(?:_)?Part_?(?<Part>[0-9]+)$') {

            $Remaining  = $Matches["Book"]
            $PartNumber = [int]$Matches["Part"]

            $Remaining = $Remaining.Trim('_')
        }

        # ====================================================
        # TEXTBOOK
        # ====================================================

        $Textbook = Normalize-Textbook -Textbook $Remaining

        # ====================================================
        # CODES
        # ====================================================

        $ClassCode   = "C{0:D2}" -f $DetectedClass
        $PartCode    = "P{0:D2}" -f $PartNumber
        $VersionCode = "V{0:D2}" -f $Version

        # ====================================================
        # FINAL CANONICAL NAME
        # ====================================================

        $NewName = "MASTER__{0}__{1}__{2}__{3}__{4}" -f `
            $ClassCode,
            $Subject,
            $Textbook,
            $PartCode,
            $VersionCode

        $NewPath = Join-Path $Folder.Parent.FullName $NewName

        # ====================================================
        # SAFETY STATUS
        # ====================================================

        $Status = "READY"
        $Reason = ""

        # Same name means nothing to do.
        if ($OldName -eq $NewName) {

            $Status = "ALREADY_CANONICAL"
            $Reason = "Folder already follows canonical convention"
        }
        elseif (Test-Path -LiteralPath $NewPath) {

            $Status = "BLOCKED"
            $Reason = "Destination already exists"
        }

        # ====================================================
        # PLAN ENTRY
        # ====================================================

        $Plan += [PSCustomObject]@{
            Status    = $Status
            Class     = $ClassCode
            Subject   = $Subject
            Textbook  = $Textbook
            Part      = $PartCode
            Version   = $VersionCode
            OldName   = $OldName
            NewName   = $NewName
            OldPath   = $Folder.FullName
            NewPath   = $NewPath
            Reason    = $Reason
        }
    }
}

# ============================================================
# DISPLAY PLAN
# ============================================================

Write-Host ""
Write-Host "============================================================"
Write-Host " PROPOSED RENAME PLAN"
Write-Host "============================================================"
Write-Host ""

if ($Plan.Count -eq 0) {

    Write-Warning "No Master Package directories were discovered."

    exit 0
}

$Plan |
    Select-Object `
        Status,
        Class,
        Subject,
        Textbook,
        Part,
        Version,
        OldName,
        NewName |
    Format-Table -AutoSize -Wrap

# ============================================================
# WRITE MANIFEST
# ============================================================

$Plan |
    Export-Csv `
        -LiteralPath $ManifestPath `
        -NoTypeInformation `
        -Encoding UTF8

Write-Host ""
Write-Host "Migration manifest:"
Write-Host "  $ManifestPath"
Write-Host ""

# ============================================================
# VALIDATION
# ============================================================

$BlockingItems = @(
    $Plan |
    Where-Object {
        $_.Status -eq "BLOCKED" -or
        $_.Status -eq "REVIEW"
    }
)

if ($BlockingItems.Count -gt 0) {

    Write-Host ""
    Write-Host "============================================================"
    Write-Host " MIGRATION BLOCKED"
    Write-Host "============================================================"
    Write-Host ""

    foreach ($Item in $BlockingItems) {

        Write-Host "Status : $($Item.Status)"
        Write-Host "Old    : $($Item.OldName)"
        Write-Host "New    : $($Item.NewName)"
        Write-Host "Reason : $($Item.Reason)"
        Write-Host ""
    }

    Write-Host "NO RENAMES PERFORMED."
    exit 1
}

# ============================================================
# CHECK DUPLICATE TARGETS
# ============================================================

$Targets = @(
    $Plan |
    Where-Object {
        $_.Status -eq "READY"
    } |
    Group-Object NewPath |
    Where-Object {
        $_.Count -gt 1
    }
)

if ($Targets.Count -gt 0) {

    Write-Host ""
    Write-Host "============================================================"
    Write-Host " DUPLICATE DESTINATIONS DETECTED"
    Write-Host "============================================================"
    Write-Host ""

    foreach ($Target in $Targets) {

        Write-Host $Target.Name
    }

    Write-Host ""
    Write-Host "NO RENAMES PERFORMED."

    exit 1
}

# ============================================================
# DRY RUN
# ============================================================

if (-not $Execute) {

    Write-Host ""
    Write-Host "============================================================"
    Write-Host " DRY RUN COMPLETE"
    Write-Host "============================================================"
    Write-Host ""

    Write-Host "Nothing was renamed."
    Write-Host ""

    Write-Host "Review:"
    Write-Host "  $ManifestPath"
    Write-Host ""

    Write-Host "If the mapping is correct, execute:"
    Write-Host ""
    Write-Host "  .\migrate_gurukul_naming.ps1 -Execute"
    Write-Host ""

    exit 0
}

# ============================================================
# EXECUTION CONFIRMATION
# ============================================================

Write-Host ""
Write-Host "============================================================"
Write-Host " EXECUTING APPROVED RENAMES"
Write-Host "============================================================"
Write-Host ""

# ============================================================
# EXECUTE RENAMES
# ============================================================

foreach ($Item in $Plan) {

    if ($Item.Status -ne "READY") {
        continue
    }

    Write-Host "RENAMING:"
    Write-Host "  OLD: $($Item.OldName)"
    Write-Host "  NEW: $($Item.NewName)"

    Rename-Item `
        -LiteralPath $Item.OldPath `
        -NewName $Item.NewName

    Write-Host "  STATUS: OK"
    Write-Host ""
}

# ============================================================
# FINAL VERIFICATION
# ============================================================

Write-Host ""
Write-Host "============================================================"
Write-Host " FINAL VERIFICATION"
Write-Host "============================================================"
Write-Host ""

$VerificationFailed = $false

foreach ($Item in $Plan) {

    if ($Item.Status -ne "READY") {
        continue
    }

    $OldExists = Test-Path -LiteralPath $Item.OldPath
    $NewExists = Test-Path -LiteralPath $Item.NewPath

    if ($OldExists) {

        Write-Error "OLD DIRECTORY STILL EXISTS:"
        Write-Error "  $($Item.OldPath)"

        $VerificationFailed = $true
    }

    if (-not $NewExists) {

        Write-Error "NEW DIRECTORY NOT FOUND:"
        Write-Error "  $($Item.NewPath)"

        $VerificationFailed = $true
    }
}

if ($VerificationFailed) {

    Write-Error "FINAL VERIFICATION FAILED."

    exit 1
}

# ============================================================
# UPDATE MANIFEST
# ============================================================

$Plan |
    Export-Csv `
        -LiteralPath $ManifestPath `
        -NoTypeInformation `
        -Encoding UTF8

# ============================================================
# COMPLETE
# ============================================================

Write-Host ""
Write-Host "============================================================"
Write-Host " NAMING MIGRATION COMPLETE"
Write-Host "============================================================"
Write-Host ""

Write-Host "Packages processed:"
Write-Host "  $($Plan.Count)"
Write-Host ""

Write-Host "Naming convention:"
Write-Host "  $ConventionPath"
Write-Host ""

Write-Host "Migration manifest:"
Write-Host "  $ManifestPath"
Write-Host ""

Write-Host "IMPORTANT:"
Write-Host "Review Git status and application references before committing."
Write-Host ""