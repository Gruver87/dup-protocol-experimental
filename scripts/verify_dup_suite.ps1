# DUP Protocol — ONE operator entry for pin + Experimental verify
#
# Does NOT start 48h soak. Does NOT rebuild Docker (except optional -RebuildLibp2p).
# PASS != public mainnet / firm audit / invented soak PASS.
#
# From Experimental repo root:
#   .\scripts\verify_dup_suite.ps1
#   .\scripts\verify_dup_suite.ps1 -Mode Quick
#   .\scripts\verify_dup_suite.ps1 -Mode Standard
#   .\scripts\verify_dup_suite.ps1 -Mode Full
#   .\scripts\verify_dup_suite.ps1 -Mode Max
#   .\scripts\verify_dup_suite.ps1 -Mode Standard -PinRoot "C:\Users\vovun\Desktop\Absolute_Blockchain_Ultimate_Hybrid"
#   .\scripts\verify_dup_suite.ps1 -Mode Quick -WithMeshProbe
#
# Alias (legacy name): .\scripts\verify_absolute_unified.ps1
# Report: data\verify_dup_suite.json
# Doc:    docs\VERIFY_SUITE.md

param(
    [ValidateSet("Quick", "Standard", "Full", "Max")]
    [string]$Mode = "Standard",
    [string]$PinRoot = "",
    [string]$HybridRoot = "",
    [double]$MinSoakHours = 48,
    [switch]$SkipPin,
    [switch]$SkipHybrid,
    [switch]$SkipExperimentalRd,
    [switch]$SkipLibp2p,
    [switch]$SkipMidsoak,
    [switch]$SkipLabs,
    [switch]$SkipGate,
    [switch]$RebuildLibp2p,
    [switch]$WithMeshProbe,
    [switch]$KeepGoing,
    [switch]$Quiet,
    [switch]$Help
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if ($Help) {
    Write-Host ""
    Write-Host "verify_dup_suite.ps1 - pin + Experimental as one operator view"
    Write-Host ""
    Write-Host "  Quick      pin quick + Exp gate + midsoak units + AI/NFT labs + showcase"
    Write-Host "  Standard   + Exp RD labs + ADR 0019 hard"
    Write-Host "  Full       pin industrial + Standard"
    Write-Host "  Max        Full + live mesh probe + verify_full_blockchain --hard"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\scripts\verify_dup_suite.ps1 -Mode Quick"
    Write-Host "  .\scripts\verify_dup_suite.ps1 -Mode Standard"
    Write-Host "  .\scripts\verify_dup_suite.ps1 -Mode Full"
    Write-Host "  .\scripts\verify_dup_suite.ps1 -Mode Max"
    Write-Host ""
    Write-Host "Per-repo alone:"
    Write-Host "  Pin:  cd Hybrid; .\scripts\verify_project.ps1 -Mode Industrial"
    Write-Host "  Exp:  .\scripts\verify_hard_all.ps1"
    Write-Host ""
    Write-Host "Report: data\verify_dup_suite.json"
    Write-Host "Honesty: green != mainnet / != soak PASS / != merged tree"
    Write-Host ""
    exit 0
}

$modeArg = $Mode.ToLowerInvariant()
$pin = if ($PinRoot) { $PinRoot } elseif ($HybridRoot) { $HybridRoot } else { "" }

$pyArgs = @(
    "scripts\verify_dup_suite.py"
    "--mode", $modeArg
    "--min-soak-hours", "$MinSoakHours"
)
if ($pin) { $pyArgs += @("--pin-root", $pin) }
if ($SkipPin -or $SkipHybrid) { $pyArgs += "--skip-pin" }
if ($SkipExperimentalRd) { $pyArgs += "--skip-experimental-rd" }
if ($SkipLibp2p) { $pyArgs += "--skip-libp2p" }
if ($SkipMidsoak) { $pyArgs += "--skip-midsoak" }
if ($SkipLabs) { $pyArgs += "--skip-labs" }
if ($SkipGate) { $pyArgs += "--skip-gate" }
if ($RebuildLibp2p) { $pyArgs += "--rebuild-libp2p" }
if ($WithMeshProbe) { $pyArgs += "--with-mesh-probe" }
if ($KeepGoing) { $pyArgs += "--keep-going" }
if ($Quiet) { $pyArgs += "-q" }

Write-Host "DUP SUITE: python $($pyArgs -join ' ')" -ForegroundColor Cyan
Write-Host "honesty: pin TCP+TLS + Exp R&D — not one merged prod tree; soak NOT started" -ForegroundColor DarkYellow
& python @pyArgs
exit $LASTEXITCODE
