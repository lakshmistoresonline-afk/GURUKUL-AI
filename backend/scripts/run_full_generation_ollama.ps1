$ErrorActionPreference = "Stop"

# ============================================================
# GURUKUL AI - FINAL AUTOMATED GENERATION V3
# FIXES:
#   1. No System.Net.Http.HttpClient
#   2. Ollama "empty response" protection
#   3. think=false for Qwen reasoning models
#   4. No format=json restriction that can suppress output
#   5. Explicit UTF-8 request body
#   6. Resume-safe validation
#   7. Retry with increasing delay
#   8. Final promotion/rebuild ONLY after complete queue
# ============================================================

$Repo = "D:\GURUKUL-AI"
$RunId = "20260909T083940Z"
$Model = "qwen3.5:2b-q4_K_M"

$OllamaBaseUrl = "http://127.0.0.1:11434"
$GenerateUrl = "$OllamaBaseUrl/api/generate"
$TagsUrl = "$OllamaBaseUrl/api/tags"

$RequestTimeoutSeconds = 1800
$MaxRetries = 3

$Orchestrator = Join-Path $Repo "backend\scripts\generate_all_valid_contents.py"
$Run = Join-Path $Repo "generation_staging\$RunId"
$JobsPath = Join-Path $Run "jobs"

function Get-CompletedCount {
    return @(
        Get-ChildItem $JobsPath -Directory |
        Where-Object {
            Test-Path (Join-Path $_.FullName "RAW_GENERATED.json")
        }
    ).Count
}

function Clean-ModelJson([string]$Text) {

    if ([string]::IsNullOrWhiteSpace($Text)) {
        throw "Ollama returned an empty response."
    }

    $s = $Text.Trim()

    # Remove markdown fences.
    $s = [regex]::Replace(
        $s,
        '^\s*```(?:json)?\s*',
        '',
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
    )

    $s = [regex]::Replace(
        $s,
        '\s*```\s*$',
        '',
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
    )

    $s = $s.Trim()

    # Locate JSON object even if the model added a tiny wrapper.
    $first = $s.IndexOf("{")
    $last = $s.LastIndexOf("}")

    if ($first -lt 0 -or $last -le $first) {
        throw "No JSON object found in Ollama response."
    }

    return $s.Substring($first, $last - $first + 1).Trim()
}

function Invoke-OllamaGenerate(
    [string]$Prompt,
    [string]$ChapterId,
    [string]$JobDirectory
) {

    $requestFile = Join-Path $JobDirectory "_OLLAMA_REQUEST.json"
    $responseFile = Join-Path $JobDirectory "_OLLAMA_RESPONSE.json"

    # IMPORTANT:
    # Do NOT use format=json here. Qwen can return an empty response when
    # structured-output enforcement conflicts with a large generated object.
    #
    # think=false is also important for Qwen models that expose reasoning
    # separately from the final response.

    $payload = [ordered]@{
        model = $Model
        prompt = [string]$Prompt
        stream = $false
        think = $false
        keep_alive = "10m"
        options = [ordered]@{
            temperature = 0.10
            num_ctx = 8192
        }
    }

    $requestJson = $payload | ConvertTo-Json -Depth 50 -Compress

    # Verify request JSON locally.
    try {
        $null = $requestJson | ConvertFrom-Json
    }
    catch {
        Set-Content -Path $requestFile -Value $requestJson -Encoding UTF8
        throw "Generated Ollama request is invalid JSON. Request saved: $requestFile"
    }

    Set-Content -Path $requestFile -Value $requestJson -Encoding UTF8

    $lastError = $null

    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {

        Write-Host "  Ollama attempt $attempt/$MaxRetries..." -ForegroundColor DarkCyan

        try {

            # Native Windows PowerShell request.
            # Explicit UTF-8 bytes avoid encoding problems with long prompts.
            $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($requestJson)

            $api = Invoke-RestMethod `
                -Uri $GenerateUrl `
                -Method Post `
                -ContentType "application/json; charset=utf-8" `
                -Body $bodyBytes `
                -TimeoutSec $RequestTimeoutSeconds `
                -ErrorAction Stop

            # Preserve the complete API response for diagnosis.
            $apiJson = $api | ConvertTo-Json -Depth 100
            Set-Content -Path $responseFile -Value $apiJson -Encoding UTF8

            if ($null -eq $api) {
                throw "Ollama returned no response object."
            }

            # Qwen may expose text in response, and in some configurations
            # reasoning can be present separately. We explicitly disabled
            # thinking above, but inspect both fields for resilience.
            $text = [string]$api.response

            if ([string]::IsNullOrWhiteSpace($text)) {

                $thinking = [string]$api.thinking

                if (-not [string]::IsNullOrWhiteSpace($thinking)) {
                    Write-Host "  Model returned reasoning but no final response; retrying." -ForegroundColor Yellow
                    throw "Ollama final response was empty."
                }

                $errorField = [string]$api.error

                if (-not [string]::IsNullOrWhiteSpace($errorField)) {
                    throw "Ollama API error: $errorField"
                }

                throw "Ollama final response was empty."
            }

            return $text
        }
        catch {

            $lastError = $_.Exception.Message

            Write-Host "  Attempt failed: $lastError" -ForegroundColor Yellow

            if ($attempt -lt $MaxRetries) {

                # Increasing retry delay: 5, 10 seconds.
                $delay = 5 * $attempt

                Write-Host "  Retrying in $delay seconds..." -ForegroundColor DarkYellow
                Start-Sleep -Seconds $delay
            }
        }
    }

    throw "Ollama generation failed for $ChapterId after $MaxRetries attempts. Last error: $lastError"
}

function Test-ExistingRaw([string]$RawFile, [string]$ExpectedChapterId) {

    try {

        $existing = Get-Content $RawFile -Raw | ConvertFrom-Json

        # Only use lightweight checks here.
        # The repository orchestrator remains the authoritative contract gate.
        if ([string]$existing.chapter_id -ne $ExpectedChapterId) {
            return $false
        }

        if ($null -eq $existing.pillars) {
            return $false
        }

        return $true
    }
    catch {
        return $false
    }
}

# ============================================================
# INITIAL CHECKS
# ============================================================

Set-Location $Repo

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " GURUKUL AI - FINAL AUTOMATED GENERATION V3" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Repository : $Repo"
Write-Host "Run ID     : $RunId"
Write-Host "Model      : $Model"
Write-Host ""

if (-not (Test-Path $Repo)) {
    throw "Repository not found: $Repo"
}

if (-not (Test-Path $Orchestrator)) {
    throw "Generation orchestrator not found: $Orchestrator"
}

if (-not (Test-Path $Run)) {
    throw "Generation run not found: $Run"
}

if (-not (Test-Path $JobsPath)) {
    throw "Jobs directory not found: $JobsPath"
}

# ============================================================
# OLLAMA CHECK
# ============================================================

Write-Host "Checking Ollama..." -ForegroundColor Cyan

try {
    $tags = Invoke-RestMethod `
        -Uri $TagsUrl `
        -Method Get `
        -TimeoutSec 15 `
        -ErrorAction Stop
}
catch {
    throw "Ollama API is unavailable at $OllamaBaseUrl. $($_.Exception.Message)"
}

$models = @(
    $tags.models |
    ForEach-Object {
        [string]$_.name
    }
)

if ($models -notcontains $Model) {

    Write-Host ""
    Write-Host "Installed models:" -ForegroundColor Yellow

    foreach ($m in $models) {
        Write-Host "  $m"
    }

    throw "Required model '$Model' is not installed."
}

Write-Host "Ollama API : READY" -ForegroundColor Green
Write-Host "Model      : $Model" -ForegroundColor Green
Write-Host "Thinking   : DISABLED" -ForegroundColor Green

# ============================================================
# QUEUE
# ============================================================

$jobs = @(
    Get-ChildItem $JobsPath -Directory |
    Sort-Object Name
)

$total = $jobs.Count
$completed = Get-CompletedCount

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " QUEUE STATUS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Total jobs     : $total"
Write-Host "Already done   : $completed"
Write-Host "Remaining      : $($total-$completed)"

$generatedThisRun = 0
$failedJobs = New-Object System.Collections.Generic.List[string]

# ============================================================
# GENERATION LOOP
# ============================================================

foreach ($job in $jobs) {

    $rawFile = Join-Path $job.FullName "RAW_GENERATED.json"
    $jobFile = Join-Path $job.FullName "JOB.json"
    $promptFile = Join-Path $job.FullName "PROMPT.txt"

    $errorFile = Join-Path $job.FullName "GENERATION_ERROR.txt"
    $invalidFile = Join-Path $job.FullName "RAW_GENERATED_INVALID.txt"

    if (-not (Test-Path $jobFile)) {
        $failedJobs.Add("$($job.Name) :: JOB.json missing")
        continue
    }

    $meta = Get-Content $jobFile -Raw | ConvertFrom-Json

    $id = [string]$meta.chapter.chapter_id
    $title = [string]$meta.chapter.chapter_title

    # Resume-safe.
    if (Test-Path $rawFile) {

        if (Test-ExistingRaw $rawFile $id) {
            Write-Host "SKIP $id - existing RAW_GENERATED.json is structurally readable." -ForegroundColor DarkGray
            continue
        }

        Write-Host ""
        Write-Host "Existing RAW_GENERATED.json is unusable for $id; regenerating." -ForegroundColor Yellow
        Remove-Item $rawFile -Force
    }

    if (-not (Test-Path $promptFile)) {
        $failedJobs.Add("$id | $title :: PROMPT.txt missing")
        continue
    }

    Write-Host ""
    Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host "GENERATING $id | $title" -ForegroundColor Yellow
    Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray

    $basePrompt = Get-Content $promptFile -Raw

    $prompt = @"
$basePrompt

FINAL OUTPUT RULES:

Return ONLY ONE valid JSON object.

Do not use Markdown.
Do not use ```json.
Do not use ```.

The first non-whitespace character MUST be {
The last non-whitespace character MUST be }

Use exactly:
chapter_id = "$id"
chapter_title = "$title"
source_bundle_sha256 = "$($meta.chapter.source_bundle_sha256)"

Generate ONLY the missing pillars requested by this job.

Every newly authored item MUST use:
"content_origin": "GENERATED"

A SOURCE_DERIVED item is allowed only when directly supported by the supplied repository source and MUST include source_ref.

Do not invent external facts, URLs, citations, page numbers, authors, names, media references, or source claims.

Do not create generic/meta questions about files, JSON, pipelines, validation, AI, generation, or software.

Keep all generated content chapter-specific, source-grounded, age-appropriate, and educational.
"@

    try {

        $rawResponse = Invoke-OllamaGenerate `
            $prompt `
            $id `
            $job.FullName

        $jsonText = Clean-ModelJson $rawResponse

        try {
            $generated = $jsonText | ConvertFrom-Json
        }
        catch {
            Set-Content `
                -Path $invalidFile `
                -Value $jsonText `
                -Encoding UTF8

            throw "Model response was not valid JSON: $($_.Exception.Message)"
        }

        # Essential identity checks before writing.
        if ([string]$generated.chapter_id -ne $id) {
            throw "Generated chapter_id '$($generated.chapter_id)' does not match '$id'."
        }

        if ($null -eq $generated.pillars) {
            throw "Generated object contains no pillars."
        }

        # Canonical pretty JSON.
        $canonical = $generated | ConvertTo-Json -Depth 100

        $tempFile = Join-Path $job.FullName "RAW_GENERATED.tmp.json"

        Set-Content `
            -Path $tempFile `
            -Value $canonical `
            -Encoding UTF8

        # Verify before promotion to final staging filename.
        $null = Get-Content $tempFile -Raw | ConvertFrom-Json

        Move-Item `
            -Path $tempFile `
            -Destination $rawFile `
            -Force

        if (Test-Path $invalidFile) {
            Remove-Item $invalidFile -Force
        }

        if (Test-Path $errorFile) {
            Remove-Item $errorFile -Force
        }

        $recordCount = 0

        foreach ($pillar in @($meta.missing_pillars)) {

            $pillarObject = $generated.pillars.$pillar

            if ($null -ne $pillarObject -and $null -ne $pillarObject.items) {
                $recordCount += @($pillarObject.items).Count
            }
        }

        $generatedThisRun++

        $nowDone = Get-CompletedCount

        Write-Host ""
        Write-Host "SUCCESS $id" -ForegroundColor Green
        Write-Host "Records : $recordCount" -ForegroundColor Green
        Write-Host "Progress: $nowDone / $total" -ForegroundColor Cyan
    }
    catch {

        $msg = $_.Exception.Message

        $failedJobs.Add("$id | $title :: $msg")

        Set-Content `
            -Path $errorFile `
            -Value "Chapter: $id`nTitle: $title`nTime: $(Get-Date -Format s)`nError: $msg" `
            -Encoding UTF8

        Write-Host ""
        Write-Host "FAILED $id :: $msg" -ForegroundColor Red
        Write-Host "Continuing to next job..." -ForegroundColor Yellow
    }
}

# ============================================================
# SUMMARY
# ============================================================

$done = Get-CompletedCount

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " GENERATION SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Total jobs         : $total"
Write-Host "Completed          : $done"
Write-Host "Remaining          : $($total-$done)"
Write-Host "Generated this run : $generatedThisRun"
Write-Host "Failed this run    : $($failedJobs.Count)"

if ($failedJobs.Count -gt 0) {

    $failureLog = Join-Path $Run "AUTOMATED_GENERATION_FAILURES.txt"

    Set-Content `
        -Path $failureLog `
        -Value ($failedJobs -join [Environment]::NewLine) `
        -Encoding UTF8

    Write-Host ""
    Write-Host "Failure log: $failureLog" -ForegroundColor Yellow
}

if ($done -ne $total) {

    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host " QUEUE INCOMPLETE - NO PROMOTION" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Rerun this SAME script."
    Write-Host "Successful jobs will be skipped."
    Write-Host "Failed jobs will be retried."

    exit 1
}

# ============================================================
# FINAL PROMOTION
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " FINAL PROMOTION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

& python $Orchestrator `
    --repo-root $Repo `
    --run-id $RunId `
    --promote

if ($LASTEXITCODE -ne 0) {
    throw "Final promotion failed."
}

Write-Host "Promotion completed." -ForegroundColor Green

# ============================================================
# FINAL REBUILD + GAP GATE
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " FINAL CANONICAL REBUILD + GAP GATE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

& python $Orchestrator `
    --repo-root $Repo `
    --run-id $RunId `
    --rebuild `
    --fail-on-gaps

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "FINAL REBUILD/GAP GATE FAILED." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " GURUKUL AI GENERATION COMPLETE" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "All staged jobs generated."
Write-Host "Final promotion completed."
Write-Host "Canonical rebuild completed."
Write-Host "Fail-on-gaps gate passed."
Write-Host ""
Write-Host "Run artifacts: $Run"
