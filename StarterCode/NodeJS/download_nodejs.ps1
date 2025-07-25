$NodeVersion = "v22.14.0"
$BaseUrl = "https://nodejs.org/dist/$NodeVersion"

$Arch = $(if ([System.Environment]::Is64BitOperatingSystem) { 
    if ($ENV:PROCESSOR_ARCHITECTURE -eq "ARM64") { "arm64" } else { "x64" } 
} else { 
    "x86" 
})

$OS = $env:OS

if ($OS -match "Windows_NT") {
    switch ($Arch) {
        "arm64" {
            $NodeTar = "node-$NodeVersion-win-arm64.zip"
        }
        "x64" {
            $NodeTar = "node-$NodeVersion-win-x64.zip"
        }
        "x86" {
            $NodeTar = "node-$NodeVersion-win-x86.zip"
        }
        default {
            Write-Host "NodeJS deos not support this architecture: $Arch"
            exit 1
        }
    }
} else {
    Write-Host "Unsupported OS: $OS"
    exit 1
}

$NodeUrl = "$BaseURL/$NodeTar"
$NodeZip = "$PWD\$NodeTar"
$NodeDir = "$PWD\nodejs"

Write-Host "Downloading Node.js..."
Invoke-WebRequest -Uri $NodeUrl -OutFile $NodeZip

if (Test-Path $NodeDir) {
    Write-Host "Removing existing Node.js..."
    Remove-Item -Recurse $NodeDir
}

Write-Host "Extracting Node.js..."
Expand-Archive -Path $NodeZip -DestinationPath "$PWD"

Write-Host "Moving Node.js..."
$ExtractedFolder = Get-ChildItem -Path "$PWD" -Directory | Where-Object { $_.Name -match "node-$NodeVersion-win-" }
if ($ExtractedFolder) {
    Move-Item -Path $ExtractedFolder.FullName -Destination $NodeDir 
}

Remove-Item $NodeZip

Write-Host "Node.js installed in: $NodeDir"

