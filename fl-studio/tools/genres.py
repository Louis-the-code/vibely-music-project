# Vibely genre settings: the ONE place to add or change a genre.
# ---------------------------------------------------------------
# vocal_preset_builder.py reads this file. To add a genre:
#   1. Copy one entry in GENRES below, rename it, change the numbers.
#   2. Fill in the matching docs page (docs/genres/_template.md).
#   3. Build its presets in FL (see docs/add-a-genre.md).
# All values are researched STARTING POINTS. Tweak by ear.
#
# Units:  c1 / c2 = compressor (threshold dB, ratio, gain dB, attack ms, release ms)
#         rev     = Fruity Reeverb 2 (size %, decay s, predelay ms, wet %)
#         delay   = Fruity Delay 3 preset name + wet % per role
#         master  = master chain notes (used by docs and the guide)

VOICE = {
    "Male":   dict(hpf=90,  mud=300, nasal=1000, pres=3500, air=10000, deess=5000),
    "Female": dict(hpf=120, mud=450, nasal=1200, pres=5000, air=12000, deess=7000),
}

ROLES = ["Lead", "Backing", "Adlibs"]

GENRES = {
    "Hip Hop": dict(
        bpm=(80, 100), lufs=(-9, -7),
        c1=(-18, 4.0, 3.0, 1.5, 110), c2=(-18, 2.5, 1.5, 25, 220), nasal_cut=-1.5, air_boost=2.5,
        rev={"Lead": (30, 0.9, 25, 12), "Backing": (45, 1.5, 30, 22), "Adlibs": (40, 1.2, 30, 18)},
        delay={"Lead": ("HIP HOP - Vocal Throw 1-4", 15), "Backing": ("HIP HOP - Vocal Throw 1-4", 18),
               "Adlibs": ("HIP HOP - Adlib 1-8", 25)},
        master="EQ 20Hz+18kHz cut | Compressor 'Master 1' | Soft Clipper on | Limiter ceiling -1 dB"),
    "Afrobeats": dict(
        bpm=(95, 115), lufs=(-9, -8),
        c1=(-20, 3.0, 3.0, 5, 100), c2=(-18, 2.0, 1.0, 30, 200), nasal_cut=0.0, air_boost=3.5,
        rev={"Lead": (40, 1.2, 30, 15), "Backing": (55, 2.0, 35, 25), "Adlibs": (50, 1.5, 30, 20)},
        delay={"Lead": ("AFROBEATS - Last Word Throw 1-4", 15), "Backing": ("AFROBEATS - Bounce 1-8 dotted", 18),
               "Adlibs": ("AFROBEATS - Bounce 1-8 dotted", 25)},
        master="EQ 20Hz+18kHz cut | Compressor 'Light' | Soft Clipper on | Limiter ceiling -1 dB"),
    "RnB": dict(
        bpm=(60, 90), lufs=(-11, -9),
        c1=(-20, 3.0, 3.0, 15, 120), c2=(-18, 2.0, 1.0, 30, 250), nasal_cut=0.0, air_boost=3.0,
        rev={"Lead": (60, 2.2, 40, 18), "Backing": (75, 3.0, 45, 30), "Adlibs": (60, 2.0, 40, 22)},
        delay={"Lead": ("AFROBEATS - Bounce 1-8 dotted", 15), "Backing": ("RnB - Dreamy 1-4 dotted", 18),
               "Adlibs": ("AFROBEATS - Bounce 1-8 dotted", 25)},
        master="EQ 20Hz+18kHz cut | Compressor 'Light' | Soft Clipper off | Limiter ceiling -1 dB"),
    "House": dict(
        bpm=(120, 128), lufs=(-9, -8),
        c1=(-20, 4.0, 3.0, 3, 80), c2=(-18, 2.0, 1.0, 30, 200), nasal_cut=0.0, air_boost=3.5,
        rev={"Lead": (65, 1.8, 35, 15), "Backing": (80, 2.8, 40, 28), "Adlibs": (70, 2.2, 35, 22)},
        delay={"Lead": ("HOUSE - Groove 1-8 dotted", 15), "Backing": ("HOUSE - Wash 1-4", 20),
               "Adlibs": ("HOUSE - Groove 1-8 dotted", 25)},
        master="EQ 20Hz+18kHz cut | Compressor 2.2:1, 33 ms attack, 167 ms release (groove glue) | "
               "Soft Clipper on | Limiter ceiling -1 dB"),
    # "Amapiano": dict(...),   <- next genre goes here
}
