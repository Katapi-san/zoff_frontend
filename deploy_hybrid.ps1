# Hybrid Deployment Script
# Allows selection between GitHub backup and Azure live deployment

$ErrorActionPreference = "Stop"

Write-Host "=== Deployment Menu ===" -ForegroundColor Cyan
Write-Host "1. GitHub Only (Backup/History)"
Write-Host "2. Azure Only (Live Update)"
Write-Host "3. Both (Hybrid Default)"
$choice = Read-Host "Please select an option (1-3)"

if ($choice -notin "1", "2", "3") {
    Write-Error "Invalid selection. Please run the script again and select 1, 2, or 3."
}

# 0. Build
# Always build to ensure code validity before pushing or deploying
Write-Host "0. Building Application..." -ForegroundColor Yellow
Set-Location "$PSScriptRoot\apps\customer"
npm run build
if ($LASTEXITCODE -ne 0) { Write-Error "Build failed!" }
Set-Location $PSScriptRoot

# 1. Deploy to GitHub
if ($choice -eq "1" -or $choice -eq "3") {
    Write-Host "`n=== 1. Deploying to GitHub ===`n" -ForegroundColor Cyan
    ./deploy_to_github.ps1
}

# 2. Deploy to Azure
if ($choice -eq "2" -or $choice -eq "3") {
    Write-Host "`n=== 2. Deploying to Azure (Direct Zip) ===`n" -ForegroundColor Cyan
    ./sync_frontend.ps1
}

Write-Host "`n=== Deployment Sequence Complete! ===" -ForegroundColor Green
if ($choice -eq "2" -or $choice -eq "3") {
    Write-Host "Check the site: https://zoff-scope-frontend.azurewebsites.net/stores" -ForegroundColor Green
}
