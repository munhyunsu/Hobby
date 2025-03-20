$FlutterVersion = "3.29.2"

# Determine architecture
$Arch = if ($ENV:PROCESSOR_ARCHITECTURE -eq "ARM64") { "arm64" } else { "x64" }

# OS check (Windows only)
$OS = $env:OS
if ($OS -notmatch "Windows_NT") {
    Write-Host "Unsupported OS: $OS"
    exit 1
}

# Determine filename and URL
if ($Arch -eq "arm64") {
    $FlutterZip = "flutter_windows_arm64_$FlutterVersion-stable.zip"
} else {
    $FlutterZip = "flutter_windows_$FlutterVersion-stable.zip"
}
$FlutterUrl = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/$FlutterZip"

$ZipPath = "$PWD\$FlutterZip"
$FlutterDir = "$PWD\flutter"

# Download
Write-Host "Downloading Flutter SDK from: $FlutterUrl"
Invoke-WebRequest -Uri $FlutterUrl -OutFile $ZipPath

# Remove existing flutter directory if exists
if (Test-Path $FlutterDir) {
    Write-Host "Removing existing Flutter directory..."
    Remove-Item -Recurse -Force $FlutterDir
}

# Extract
Write-Host "Extracting Flutter SDK..."
Expand-Archive -Path $ZipPath -DestinationPath "$PWD"

# Move to target flutter directory if needed
$ExtractedFolder = Get-ChildItem -Path "$PWD" -Directory | Where-Object { $_.Name -like "flutter" }
if ($ExtractedFolder -and $ExtractedFolder.FullName -ne $FlutterDir) {
    Move-Item -Path $ExtractedFolder.FullName -Destination $FlutterDir
}

# Cleanup
Remove-Item $ZipPath

Write-Host "Flutter $FlutterVersion 설치 완료!"
Write-Host "설치 경로: $FlutterDir"

