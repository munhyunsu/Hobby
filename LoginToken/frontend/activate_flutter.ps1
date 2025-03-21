$global:OLD_PATH = $env:Path
$global:OLD_PROMPT = $host.UI.RawUI.WindowTitle
$global:OLD_PROMPT_FUNCTION = $function:prompt

$DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

$env:Path = "$DIR\flutter\bin;$env:Path"
$host.UI.RawUI.WindowTitle = "(flutter) $($host.UI.RawUI.WindowTitle)"

function global:prompt {
    Write-Host "(flutter) " -NoNewLine -ForegroundColor Cyan
    & $global:OLD_PROMPT_FUNCTION
}

function global:deactivate_flutter {
    $env:Path = $global:OLD_PATH
    $host.UI.RawUI.WindowTitle = $global:OLD_PROMPT
    $function:prompt = $global:OLD_PROMPT_FUNCTION
    Remove-Variable OLD_PATH -Scope Global
    Remove-Variable OLD_PROMPT -Scope Global
    Remove-Variable OLD_PROMPT_FUNCTION -Scope Global
    Remove-Item function:\deactivate_flutter
    Write-Host "Environment deactivated. PATH restored."
}

Write-Host "Flutter environment activated. Use 'deactivate_flutter' to revert."

