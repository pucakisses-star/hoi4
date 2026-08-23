<#
    bisect-mod.ps1 - narrow down which part of the mod causes the crash.

    HOI4 only loads directories it recognises, so renaming one to <name>_off
    makes the game skip it. Each test is therefore one rename and one launch.

    USAGE
        .\bisect-mod.ps1                 show current state
        .\bisect-mod.ps1 -Off history    disable MOD/history
        .\bisect-mod.ps1 -On  history    re-enable it
        .\bisect-mod.ps1 -Reset          re-enable everything

    The mod will look broken while a directory is disabled. That does not
    matter - the only question being asked is whether it reaches the main menu.

    ORDER TO TEST
        1  history      2  map      3  common      4  events

    Whichever one stops the crash contains the cause. Then bisect inside it:
    common splits readily into ideas, technologies, units, countries.
#>
param(
    [string]$Off,
    [string]$On,
    [switch]$Reset,
    [string]$ModPath
)

function Find-ModPath {
    if ($ModPath) { return $ModPath }
    $roots = @(
        "$env:USERPROFILE\Documents\Paradox Interactive\Hearts of Iron IV\mod",
        "$env:USERPROFILE\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod"
    )
    foreach ($r in $roots) {
        if (-not (Test-Path $r)) { continue }
        # the mod folder is whichever subdirectory holds descriptor.mod
        $c = Get-ChildItem $r -Directory -ErrorAction SilentlyContinue |
             Where-Object { Test-Path (Join-Path $_.FullName 'descriptor.mod') }
        if ($c) { return $c[0].FullName }
    }
    return $null
}

$mod = Find-ModPath
if (-not $mod) {
    Write-Host "Could not find the mod folder." -ForegroundColor Red
    Write-Host "Pass it explicitly:  .\bisect-mod.ps1 -ModPath 'C:\path\to\mod\folder' -Off history"
    exit 1
}
Write-Host "Mod folder: $mod" -ForegroundColor Cyan

$targets = @('history','map','common','events','gfx','interface','localisation')

if ($Reset) {
    foreach ($t in $targets) {
        $d = Join-Path $mod "${t}_off"
        if (Test-Path $d) { Rename-Item $d (Join-Path $mod $t); Write-Host "  re-enabled $t" -ForegroundColor Green }
    }
}
elseif ($Off) {
    $src = Join-Path $mod $Off
    if (-not (Test-Path $src)) { Write-Host "  $Off is not there (already disabled?)" -ForegroundColor Yellow; exit 1 }
    Rename-Item $src (Join-Path $mod "${Off}_off")
    Write-Host "  DISABLED $Off  -> launch the game now" -ForegroundColor Yellow
}
elseif ($On) {
    $src = Join-Path $mod "${On}_off"
    if (-not (Test-Path $src)) { Write-Host "  ${On}_off is not there" -ForegroundColor Yellow; exit 1 }
    Rename-Item $src (Join-Path $mod $On)
    Write-Host "  re-enabled $On" -ForegroundColor Green
}

Write-Host "`nCurrent state:"
foreach ($t in $targets) {
    $on  = Test-Path (Join-Path $mod $t)
    $off = Test-Path (Join-Path $mod "${t}_off")
    if ($on)      { Write-Host ("  {0,-14} loaded"   -f $t) -ForegroundColor Green }
    elseif ($off) { Write-Host ("  {0,-14} DISABLED" -f $t) -ForegroundColor Yellow }
}
