
# Script to Deploy Frontend Build Artifacts DIRECTLY to Azure (Local Git)
# This bypasses GitHub actions and pushes directly to the Azure SCM endpoint.

$AZURE_GIT_URL = "https://zoff-scope-frontend.scm.azurewebsites.net:443/zoff-scope-frontend.git"
$SOURCE_DIR = "$PSScriptRoot\apps\customer"
$TEMP_DIR = "$PSScriptRoot\temp_azure_deploy"

# 1. Prepare Temp Directory
Write-Host "1. Preparing deployment directory..."
if (Test-Path $TEMP_DIR) { Remove-Item -Force -Recurse $TEMP_DIR }
New-Item -ItemType Directory -Path $TEMP_DIR | Out-Null

# 2. Copy Artifacts (Next.js Standalone Build)
Write-Host "2. Copying Standalone Artifacts..."
# Copy .next/standalone content to root
robocopy "$SOURCE_DIR\.next\standalone" "$TEMP_DIR" /E /NFL /NDL /NJH /NJS
# Copy .next/static to .next/static
New-Item -ItemType Directory -Path "$TEMP_DIR\.next\static" -Force | Out-Null
robocopy "$SOURCE_DIR\.next\static" "$TEMP_DIR\.next\static" /E /NFL /NDL /NJH /NJS
# Copy public to public
New-Item -ItemType Directory -Path "$TEMP_DIR\public" -Force | Out-Null
robocopy "$SOURCE_DIR\public" "$TEMP_DIR\public" /E /NFL /NDL /NJH /NJS

# 3. FIX START SCRIPT & CLEANUP
Write-Host "3. Configuring package.json for Azure..."
$pkgJsonPath = "$TEMP_DIR\package.json"
$pkgJson = Get-Content $pkgJsonPath -Raw | ConvertFrom-Json
$pkgJson.scripts.start = "node server.js"
$pkgJson | ConvertTo-Json -Depth 10 | Set-Content $pkgJsonPath

# 4. Git Initialization & Push
Write-Host "4. Pushing to Azure..."
Set-Location $TEMP_DIR
git init
git config user.name "DeployBot"
git config user.email "deploy@local"
git add .
git commit -m "Direct Deploy: Azure Local Git"

# Add remote with credentials embedded (Careful with logs!)
# Using the provided credentials directly
$KV_URL = $AZURE_GIT_URL.Replace("https://", "https://$zoff-scope-frontend:2eTLRd9aco4QpLcH3rh3GhGR8DaMBtMSBRg3i4lzEtjQQ5X9Rd49XoXa6vN9@")
git remote add azure $KV_URL

# Force push to master (Azure Local Git usually uses master)
Write-Host "Pushing to Azure master branch... (This may take a minute)"
git push azure master --force

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Deployment pushed to Azure."
}
else {
    Write-Error "FAILED: git push returned error code $LASTEXITCODE"
}
