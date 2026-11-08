# Add a genre

The system is built so a new genre (Amapiano, Drill, Dancehall, Pop...) is **one entry + one doc + a few presets**. No script changes.

## 1. Research and write it down
- Copy [`genres/_template.md`](genres/_template.md) to `genres/<genre>.md` and fill it in (tempo, loudness, compressor, reverb, delays, sources).
- Add the same numbers as a new entry in [`fl-studio/tools/genres.py`](../fl-studio/tools/genres.py) (copy the House entry and change it).

## 2. Delay presets (Fruity Delay 3, by hand)
FL's scripting can't set Delay 3, so: load the closest existing delay preset, change Time / Feedback / Cutoff (hover a knob to read its value, mouse-wheel to change it), then slot menu → **Save preset as** → `<GENRE> - <Name> <time>`.

## 3. Master preset
Load the closest `MASTER - ...` on the Master track, change the compressor, then select the Master and press **Ctrl+Shift+S** → `MASTER - <Genre>`.

## 4. Six vocal presets (builder does most of it)
1. Load the closest `VOX - ... - Male Lead` onto **Insert 1**.
2. **View → Script output → Interpreter**, then run:
   ```python
   import sys; sys.path.append(r"<path to fl-studio\tools>")
   import vocal_preset_builder as vj
   vj.build("<Genre>", "Male", "Lead")
   ```
   It sets EQ, de-esser, both compressors and reverb, and prints what it set.
3. Change the delay slot (step 2 settings, keep **dry 100%** and set wet), and rename the slot (F2) to the delay name.
4. Select Insert 1 → **Ctrl+Shift+S** → `VOX - <Genre> - Male Lead`.
5. For Female: keep the same track, run `vj.build("<Genre>", "Female", "Lead")`, save. Repeat for Backing and Adlibs.

## 5. Ship it
Copy the new `.fst` files into `fl-studio/presets/...`, update the tables in `docs/`, add a CHANGELOG line, and re-run the installer.
