# File: elevate_and_setup.ps1

# === 1) Ensure we’re running as Admin ===
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {
    # Re-launch this script as Administrator
    Start-Process -FilePath PowerShell -Verb RunAs `
        -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

# === 2) Change this to your actual project path ===
$projectPath = 'C:\path\to\your\ai-finance-app'

# Try to switch to that directory
try {
    Set-Location -Path $projectPath -ErrorAction Stop
} catch {
    Write-Error "Cannot cd to '$projectPath'. Please edit the script and set \$projectPath correctly."
    exit 1
}

# === 3) Create integrations package folder ===
if (!(Test-Path -Path 'integrations' -PathType Container)) {
    New-Item -Path . -Name 'integrations' -ItemType Directory | Out-Null
    Write-Host "Created folder: integrations"
} else {
    Write-Host "Folder 'integrations' already exists"
}

# Create __init__.py if missing
$initFile = Join-Path 'integrations' '__init__.py'
if (!(Test-Path -Path $initFile -PathType Leaf)) {
    New-Item -Path 'integrations' -Name '__init__.py' -ItemType File | Out-Null
    Write-Host "Created file: integrations\__init__.py"
} else {
    Write-Host "File integrations\__init__.py already exists"
}

Write-Host "`n✅ integrations package is ready!`n"