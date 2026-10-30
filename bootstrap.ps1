param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ToolkitArgs)
$ErrorActionPreference = 'Stop'
$entry = Join-Path $PSScriptRoot 'toolkit.py'
if (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 $entry @ToolkitArgs
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  & python $entry @ToolkitArgs
} else {
  Write-Error 'Python 3.11+ is required. Open START-HERE.md in Claude for setup.'
  exit 2
}
exit $LASTEXITCODE
