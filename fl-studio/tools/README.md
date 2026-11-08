# Tools
- `genres.py`: **all genre settings in one place** (compressors, reverb, delays, loudness, master notes). Add a genre here first. See [docs/add-a-genre.md](../../docs/add-a-genre.md).
- `vocal_preset_builder.py`: the developer tool that built the 24 VOX presets by setting plugin values through FL Studio's scripting API and reading them back. It reads `genres.py`. See the header comment and [docs/how-it-was-built.md](../../docs/how-it-was-built.md). Not needed to *use* the presets.
