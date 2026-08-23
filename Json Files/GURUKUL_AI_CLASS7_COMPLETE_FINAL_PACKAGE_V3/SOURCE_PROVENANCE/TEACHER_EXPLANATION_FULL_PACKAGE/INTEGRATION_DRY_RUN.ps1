param([Parameter(Mandatory=$true)][string]$RepoRoot)
Write-Host "DRY RUN ONLY - no existing Gurukul files will be changed."
Write-Host "Package root: $(Split-Path -Parent $PSScriptRoot)"
Write-Host "Repository: $RepoRoot"
Write-Host "Use the manifest to map class + subject + chapter_id."
Write-Host "Do not overwrite existing assessment_bank.json or lesson components."
