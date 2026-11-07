# Install (Windows, FL Studio 21)

1. **Find your FL user data folder:** *Options → File settings → User data folder.*
   ⚠️ It may be in **OneDrive** (`...\OneDrive\Documents\Image-Line\`), not your normal Documents. Our first install failed because of this.
2. **Script:** copy the folder `fl-studio/scripts/StemMixer` to `<user data>\FL Studio\Settings\Hardware\`. It must sit **directly** inside `Hardware`, one level deep.
3. **Presets:**
   - `fl-studio/presets/mixer/*.fst` → `<user data>\FL Studio\Presets\Mixer presets\`
   - `fl-studio/presets/fruity-delay-3/*.fst` → `<user data>\FL Studio\Presets\Plugin presets\Effects\Fruity Delay 3\`
4. **Virtual MIDI port:** install loopMIDI and add a port (Mac: enable the IAC Driver).
5. **Restart FL Studio** (fully: check Task Manager).
6. **Options → MIDI Settings** → click the loopMIDI input → Enable → **Controller type: Stem Mixer**.
7. Check **View → Script output** if anything looks wrong.

## Every song
File → New → drag stems → select Stem Mixer (or switch away and back) → F9 → load VOX presets on vocals → set levels → sidechain kick → bass → load a MASTER preset → set limiter gain to the LUFS target.
