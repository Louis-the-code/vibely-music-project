# Vibely Music Project - one-click installer for FL Studio (Windows)
# Run it by double-clicking Install-Vibely.bat (same folder).
#
# What it does:
#   1. Finds your FL Studio user data folder (also inside OneDrive).
#   2. Copies the Stem Mixer script, mixer presets (MASTER + VOX) and
#      Fruity Delay 3 presets into the right places.
#   3. Backs up an older Stem Mixer script before replacing it.
# It never deletes anything. Use -DryRun to see what it would do.

param(
    [string]$UserData = "",   # optional: path that CONTAINS the "FL Studio" folder
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Src  = Join-Path $Here "fl-studio"

function Say($msg, $color = "Gray") { Write-Host $msg -ForegroundColor $color }

Say ""
Say "  VIBELY MUSIC PROJECT - installer" "Cyan"
Say "  AI does the setup. You make the music." "DarkCyan"
Say ""

if (-not (Test-Path (Join-Path $Src "scripts\StemMixer\device_StemMixer.py"))) {
    Say "Can't find the 'fl-studio' folder next to this installer." "Red"
    Say "Unzip the whole project first, then run Install-Vibely.bat from inside it." "Red"
    exit 1
}

# ---------------------------------------------------------------- 1. find FL user data
function Test-FLUserData($dir) {
    if (-not $dir) { return $false }
    $fl = Join-Path $dir "FL Studio"
    return (Test-Path (Join-Path $fl "Settings")) -or (Test-Path (Join-Path $fl "Presets"))
}

$candidates = @()
if ($UserData) {
    $candidates += $UserData
} else {
    $docs = @(
        [Environment]::GetFolderPath("MyDocuments"),
        (Join-Path $env:USERPROFILE "Documents")
    )
    foreach ($od in @($env:OneDrive, $env:OneDriveConsumer, $env:OneDriveCommercial)) {
        if ($od) { $docs += (Join-Path $od "Documents"); $docs += (Join-Path $od "Dokumente") }
    }
    # Any "OneDrive*" folder in the user profile (e.g. "OneDrive - Company")
    Get-ChildItem -Path $env:USERPROFILE -Directory -Filter "OneDrive*" -ErrorAction SilentlyContinue |
        ForEach-Object { $docs += (Join-Path $_.FullName "Documents"); $docs += (Join-Path $_.FullName "Dokumente") }
    foreach ($d in $docs) { if ($d) { $candidates += (Join-Path $d "Image-Line") } }
}

$found = @()
foreach ($c in $candidates) {
    try { $full = (Resolve-Path $c -ErrorAction Stop).Path } catch { continue }
    if ((Test-FLUserData $full) -and ($found -notcontains $full)) { $found += $full }
}

if ($found.Count -eq 0) {
    Say "I couldn't find your FL Studio user data folder automatically." "Yellow"
    Say "In FL Studio: Options > File settings > 'User data folder'. Paste that path here."
    Say "(It usually ends in ...\Documents\Image-Line)"
    $typed = (Read-Host "Path").Trim('"', ' ')
    if ($typed -match "\\FL Studio\\?$") { $typed = Split-Path -Parent $typed }
    if (-not (Test-FLUserData $typed)) {
        Say "That folder doesn't contain an 'FL Studio' folder with Settings or Presets. Nothing was changed." "Red"
        exit 1
    }
    $found = @((Resolve-Path $typed).Path)
}

if ($found.Count -gt 1) {
    Say "I found more than one FL Studio user data folder:" "Yellow"
    for ($i = 0; $i -lt $found.Count; $i++) { Say ("  [{0}] {1}" -f ($i + 1), $found[$i]) }
    Say "Check FL Studio: Options > File settings > User data folder, to see which one it uses."
    $pick = Read-Host "Type the number to install into (or A for all)"
    if ($pick -match "^[aA]$") { $targets = $found }
    elseif ($pick -match "^\d+$" -and [int]$pick -ge 1 -and [int]$pick -le $found.Count) { $targets = @($found[[int]$pick - 1]) }
    else { Say "Not a valid choice. Nothing was changed." "Red"; exit 1 }
} else {
    $targets = $found
}

# ---------------------------------------------------------------- warn if FL is open
if (Get-Process -Name "FL64", "FL", "FL Studio*" -ErrorAction SilentlyContinue) {
    Say "FL Studio is open. That's OK, but you must RESTART it after installing to see the script." "Yellow"
}

# ---------------------------------------------------------------- 2. copy
function Copy-Set($from, $pattern, $to) {
    $files = @(Get-ChildItem -Path $from -Filter $pattern -File -ErrorAction SilentlyContinue)
    if ($files.Count -eq 0) { return 0 }
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $to | Out-Null }
    foreach ($f in $files) {
        if ($DryRun) { Say ("    would copy {0}" -f $f.Name) "DarkGray" }
        else { Copy-Item -LiteralPath $f.FullName -Destination (Join-Path $to $f.Name) -Force }
    }
    return $files.Count
}

foreach ($ud in $targets) {
    $fl = Join-Path $ud "FL Studio"
    Say ""
    Say ("Installing into: {0}" -f $fl) "Cyan"

    # Script
    $hw = Join-Path $fl "Settings\Hardware\StemMixer"
    $old = Join-Path $hw "device_StemMixer.py"
    if ((Test-Path $old) -and -not $DryRun) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $bakDir = Join-Path $fl "Settings\Hardware\_vibely_backup"
        New-Item -ItemType Directory -Force -Path $bakDir | Out-Null
        Copy-Item -LiteralPath $old -Destination (Join-Path $bakDir "device_StemMixer.$stamp.py") -Force
        Say "  backed up the old Stem Mixer script to Settings\Hardware\_vibely_backup" "DarkGray"
    }
    $n1 = Copy-Set (Join-Path $Src "scripts\StemMixer") "*.py" $hw
    $n2 = Copy-Set (Join-Path $Src "presets\mixer") "*.fst" (Join-Path $fl "Presets\Mixer presets")
    $n3 = Copy-Set (Join-Path $Src "presets\fruity-delay-3") "*.fst" (Join-Path $fl "Presets\Plugin presets\Effects\Fruity Delay 3")

    Say ("  Stem Mixer script ......... {0} file(s)" -f $n1) "Green"
    Say ("  MASTER + VOX presets ...... {0} file(s)" -f $n2) "Green"
    Say ("  Fruity Delay 3 presets .... {0} file(s)" -f $n3) "Green"
}

Say ""
if ($DryRun) { Say "Dry run only: nothing was copied." "Yellow" }
else { Say "Done!" "Green" }
Say ""
Say "Next steps:" "Cyan"
Say "  1. Install loopMIDI (free) and add one port, if you haven't yet."
Say "  2. Fully close and reopen FL Studio."
Say "  3. File > New, drag your stems in."
Say "  4. Options > MIDI Settings > select the loopMIDI input > Controller type: Stem Mixer."
Say "  5. Drag a VOX preset onto your vocal track and a MASTER preset onto the Master. Then use your ears."
Say ""
