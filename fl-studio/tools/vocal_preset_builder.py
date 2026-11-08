# Vocal Preset Builder (developer tool)
# -------------------------------------
# Used to build the VOX mixer presets (24 so far) in FL Studio 21 (scripting API v30).
# It sets every knob of a fixed 8-slot vocal chain by *displayed value*
# (Hz, dB, ms, ratio) using a bisection search, then prints a read-back line.
#
# How to run: in FL, View > Script output > Interpreter, with this folder on
# sys.path, while mixer Insert 1 holds this chain:
#   0 Pitcher | 1 Parametric EQ 2 | 2 Maximus
# (De-esser split band) | 3 Fruity Compressor | 4 Fruity Compressor |
# 5 Parametric EQ 2 | 6 Fruity Delay 3 | 7 Fruity Reeverb 2
#   >>> import sys; sys.path.append(r"<this folder>")
#   >>> import vocal_preset_builder as vj; vj.build("House", "Female", "Lead")
# Then set the delay slot by hand (see docs/add-a-genre.md) and save the track
# with Ctrl+Shift+S (Save mixer track state).
#
# Known limits (FL 21): plugins.setParamValue cannot write Fruity Delay 3
# (all values jump to max), so delays were set by loading Delay 3 presets.
# Track volume read-back in dB was unreliable, so faders are set to 0.8 (0 dB).
import plugins, mixer

TRACK = 1
MODE = "apply"        # "options" or "apply"
CURRENT = "Hip Hop|Male|Lead"

PITCH, EQ1, DEESS, COMP1, COMP2, EQ2, DLY, VERB = range(8)

# ------------------------------------------------------------ value helpers
def _num(s, ticks=False):
    s = s.strip()
    if ticks and ":" in s:
        a, b = s.split(":")[0], s.split(":")[1]
        return float(a) * 48 + float(b)          # steps:ticks
    out, seen = "", False
    for ch in s:
        if ch.isdigit() or ch == "." or (ch == "-" and not out):
            out += ch; seen = True
        elif seen:
            break
    if not out or out in ("-", "."):
        return None
    v = float(out)
    rest = s[len(out):].strip().lower() if s.startswith(out) else s.lower()
    if "khz" in rest:
        v *= 1000
    return v

def _str(slot, p):
    return plugins.getParamValueString(p, TRACK, slot)

def _set(slot, p, v):
    plugins.setParamValue(v, p, TRACK, slot)

def set_num(slot, p, target, ticks=False):
    _set(slot, p, 0.2); a = _num(_str(slot, p), ticks)
    _set(slot, p, 0.8); b = _num(_str(slot, p), ticks)
    up = (b is not None and a is not None and b > a)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        _set(slot, p, mid)
        val = _num(_str(slot, p), ticks)
        if val is None:
            val = float('inf') if (mid > 0.5) == up else float('-inf')
        if (val < target) == up:
            lo = mid
        else:
            hi = mid
    # pick the closer end
    best, bestd = None, None
    for v in (lo, hi):
        _set(slot, p, v)
        n = _num(_str(slot, p), ticks)
        d = abs(n - target) if n is not None else 1e18
        if bestd is None or d < bestd:
            best, bestd = v, d
    _set(slot, p, best)
    return _str(slot, p)

def set_enum(slot, p, label):
    for k in range(0, 201):
        v = k / 200.0
        _set(slot, p, v)
        if _str(slot, p).strip().lower() == label.lower():
            return _str(slot, p)
    return "!! no option " + label

def options(slot, p):
    seen = []
    for k in range(0, 201):
        _set(slot, p, k / 200.0)
        s = _str(slot, p)
        if s not in seen:
            seen.append(s)
    _set(slot, p, 0.5)
    return seen

def set_vol_db(db):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        mixer.setTrackVolume(TRACK, mid)
        if mixer.getTrackVolume(TRACK, 1) < db:
            lo = mid
        else:
            hi = mid
    mixer.setTrackVolume(TRACK, hi)
    return "%.1f dB" % mixer.getTrackVolume(TRACK, 1)

# ------------------------------------------------------------ presets
# Genre and voice numbers live in genres.py (same folder) so new genres
# can be added without touching this file.
from genres import VOICE, GENRES as GENRE

def build(genre, voice, role):
    v, g = VOICE[voice], GENRE[genre]
    log = []
    def L(tag, res):
        log.append("%s=%s" % (tag, res))
    # ---- EQ 1: clean-up
    hpf = v["hpf"] + {"Lead": 0, "Backing": 80, "Adlibs": 160}[role]
    L("HPF", set_enum(EQ1, 21, "High pass")); L("HPFf", set_num(EQ1, 7, hpf))
    L("MUDtype", set_enum(EQ1, 22, "Peaking")); L("MUDf", set_num(EQ1, 8, v["mud"]))
    L("MUDdb", set_num(EQ1, 1, {"Lead": -2.5, "Backing": -4.0, "Adlibs": -3.0}[role]))
    L("NASf", set_num(EQ1, 9, v["nasal"]))
    L("NASdb", set_num(EQ1, 2, g["nasal_cut"] if role == "Lead" else 0.0))
    for b in (3, 4, 5, 6):
        set_num(EQ1, b, 0.0)
    # ---- de-esser split frequency
    L("DEESS", set_num(DEESS, 0, v["deess"]))
    # ---- compressors
    thr, rat, gain, atk, rel = g["c1"]
    if role != "Lead":
        rat = 4.0
    for (slot, vals) in ((COMP1, (thr, rat, gain, atk, rel)), (COMP2, g["c2"])):
        t, r, gn, a, rl = vals
        L("C%dthr" % slot, set_num(slot, 0, t)); L("C%drat" % slot, set_num(slot, 1, r))
        L("C%dgain" % slot, set_num(slot, 2, gn)); L("C%datk" % slot, set_num(slot, 3, a))
        L("C%drel" % slot, set_num(slot, 4, rl))
    L("C2type", set_enum(COMP2, 5, "Soft"))
    # ---- EQ 2: tone
    for b in (0, 1, 2, 4, 5):
        set_num(EQ2, b, 0.0)
    L("PRESf", set_num(EQ2, 10, v["pres"]))
    L("PRESdb", set_num(EQ2, 3, {"Lead": 2.0, "Backing": -2.0, "Adlibs": 2.5}[role]))
    if role == "Backing":
        L("TOPtype", set_enum(EQ2, 27, "Low pass")); L("TOPf", set_num(EQ2, 13, 11000)); set_num(EQ2, 6, 0.0)
    else:
        L("TOPtype", set_enum(EQ2, 27, "High shelf")); L("TOPf", set_num(EQ2, 13, v["air"]))
        L("AIRdb", set_num(EQ2, 6, g["air_boost"] if role == "Lead" else 1.5))
    # ---- reverb
    size, decay, pre, rwet = g["rev"][role]
    L("Rlow", set_num(VERB, 0, 350)); L("Rhigh", set_num(VERB, 1, 7000 if role == "Lead" else 6000))
    L("Rpre", set_num(VERB, 2, pre)); L("Rsize", set_num(VERB, 3, size)); L("Rdecay", set_num(VERB, 5, decay))
    L("Rdry", set_num(VERB, 10, 100)); L("Rwet", set_num(VERB, 12, rwet))
    # ---- fader starting level
    mixer.setTrackVolume(TRACK, 0.8)

    print("[vocal_job] %s %s %s" % (genre, voice, role))
    print(" | ".join(log))

def run():
    if MODE == "check":
        T = 2
        def g(slot, p):
            return plugins.getParamValueString(p, T, slot)
        print("[check] slots:", [plugins.getPluginName(T, s) if plugins.isValid(T, s) else "-" for s in range(8)])
        print("[check] EQ1 HPF", g(EQ1, 21), g(EQ1, 7), "| mud", g(EQ1, 8), g(EQ1, 1), "| deess", g(DEESS, 0),
              "| C1", g(COMP1, 0), g(COMP1, 1), g(COMP1, 3), "| C2", g(COMP2, 1), g(COMP2, 3),
              "| pres", g(EQ2, 10), g(EQ2, 3), "| top", g(EQ2, 27), g(EQ2, 13),
              "| DLY time", g(DLY, 4), "fb", g(DLY, 14), "dry", g(DLY, 25), "wet", g(DLY, 23),
              "| REV", g(VERB, 5), g(VERB, 12), g(VERB, 10))
        return
    if MODE == "probe":
        for slot, p in ((DLY, 4), (DLY, 14), (DLY, 16), (DLY, 23), (VERB, 0), (VERB, 1)):
            out = []
            for v in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0):
                _set(slot, p, v)
                out.append("%.2f>%s(%.3f)" % (v, _str(slot, p), plugins.getParamValue(p, TRACK, slot)))
            print(slot, p, plugins.getParamName(p, TRACK, slot), " ".join(out))
        return
    if MODE == "options":
        print("EQ type:", options(EQ1, 21)); set_enum(EQ1, 21, "Low shelf")
        print("Delay filter:", options(DLY, 15))
        print("Comp type:", options(COMP1, 5))
    elif MODE == "apply":
        g, v, r = CURRENT.split("|")
        build(g, v, r)
