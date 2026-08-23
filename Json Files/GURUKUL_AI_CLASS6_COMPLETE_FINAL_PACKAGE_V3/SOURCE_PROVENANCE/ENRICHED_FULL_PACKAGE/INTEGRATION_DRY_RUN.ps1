param([Parameter(Mandatory=$true)][string]$RepoRoot)
Write-Host "DRY RUN ONLY - no files will be changed."
$src=Join-Path (Split-Path -Parent $PSScriptRoot) "content"
Write-Host "Enriched source: $src"
Write-Host "Repository target: $RepoRoot"
Write-Host "Review MASTER_MANIFEST.json before integration."
Write-Host "No assessment_bank.json will be replaced by this package."
