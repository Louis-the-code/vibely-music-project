# Changelog

Newest first. Updated after every task.

## 2026-11-07 (later)
- **Added House:** MASTER - House (groove-glue compressor), 6 VOX - House vocal presets, 2 delays (HOUSE - Groove 1-8 dotted, HOUSE - Wash 1-4). Doc: [docs/genres/house.md](docs/genres/house.md).
- **One-click installer:** `Install-Vibely.bat` + `Install-Vibely.ps1` (finds the FL user data folder incl. OneDrive, backs up the old script, `-DryRun` option).
- **Room for more genres:** all genre numbers moved to `fl-studio/tools/genres.py`; added `docs/genres/_template.md` and [docs/add-a-genre.md](docs/add-a-genre.md).
- Builder now runs from FL's Script output interpreter (no temporary hook in the Stem Mixer script).
- Guides and cheat sheet updated with House.

## 2026-11-07
- **Repo created:** README, docs, principles, projects section (SoundCloud slots), screenshots.
- **Added 18 vocal presets** (Hip Hop / Afrobeats / RnB × Male / Female × Lead / Backing / Adlibs). Built via FL scripting, verified by read-back.
- **Added Mixing Cheat Sheet** (4-page visual PDF + HTML source).
- **Added 5 Fruity Delay 3 presets** (tempo-synced, genre-matched).
- **Added 3 master presets** (Hip Hop, Afrobeats, RnB).
- **Stem Mixer v3:** one script, 23 tracks, automatic stem routing by file name; fixed the FL 21 channel API and full-volume sends.

## 2026-11-06
- Stem Mixer v1-v2 (genre scripts, 47 tracks), Quick Guide PDF.
- Diagnosed the install failure: FL user data lives in OneDrive\Documents.
