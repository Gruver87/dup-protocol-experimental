# Legacy alias -> verify_dup_suite.ps1
param(
    [ValidateSet("Quick", "Standard", "Full", "Max")]
    [string]$Mode = "Standard",
    [string]$HybridRoot = "",
    [double]$MinSoakHours = 48,
    [switch]$SkipHybrid,
    [switch]$SkipExperimentalRd,
    [switch]$SkipLibp2p,
    [switch]$RebuildLibp2p,
    [switch]$KeepGoing,
    [switch]$Quiet,
    [switch]$Help
)

$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$fwd = Join-Path $here "verify_dup_suite.ps1"
Write-Host "NOTE: verify_absolute_unified.ps1 -> verify_dup_suite.ps1" -ForegroundColor DarkYellow
& $fwd -Mode $Mode -PinRoot $HybridRoot -MinSoakHours $MinSoakHours `
    -SkipPin:$SkipHybrid -SkipExperimentalRd:$SkipExperimentalRd `
    -SkipLibp2p:$SkipLibp2p -RebuildLibp2p:$RebuildLibp2p `
    -KeepGoing:$KeepGoing -Quiet:$Quiet -Help:$Help
exit $LASTEXITCODE
