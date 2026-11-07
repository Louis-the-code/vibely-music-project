# name=Stem Mixer
# Stem Mixer v3 for FL Studio 21+  (one script for every genre)
#
# WHAT IT DOES when you pick "Stem Mixer" in Options > MIDI Settings > Controller type:
#   1. In an empty project: builds a simple, colour-coded 23-track mixer.
#   2. Routes every stem in the Channel Rack to the right mixer track by its file
#      name (kick -> KICK, vocal -> LEAD VOCAL, 808 -> 808 / BASS ...).
# Drag your stems in first, then pick (or re-pick) "Stem Mixer". Run it again any time.
# Safe: it never builds over a project whose mixer tracks you've already renamed,
# and it never moves a stem you've put on mixer track 24 or higher.

import mixer
import channels
import utils

MASTER = 0

# ---------------------------------------------------------------- layout
KICK, SNARE, PERC, DLOW, DMID, DHIGH, DLOOP = 1, 2, 3, 4, 5, 6, 7
BASS1, BASS2 = 8, 9
CHORDS, MEL1, MEL2, MEL3, FX = 10, 11, 12, 13, 14
LEADVOX, BACKVOX = 15, 16
REF = 17
DRUMS_BUS, BASS_BUS, MUSIC_BUS, VOCAL_BUS = 18, 19, 20, 21
REVERB, DELAY = 22, 23
LAST = 23

RED = (225, 55, 50); ORANGE = (245, 135, 30); AMBER = (250, 185, 50)
PURPLE = (145, 75, 215); BLUE = (55, 125, 235); TEAL = (35, 185, 170)
GREEN = (75, 195, 95); GOLD = (245, 200, 40); WHITE = (205, 205, 205)
PINK = (235, 95, 185)

SEND = 0.40   # starting send level (FL scale: 0.8 = 0 dB)

# (track, name, colour, destination, [(send track, level)], pan)
LAYOUT = [
    (KICK,   "KICK",             RED,    DRUMS_BUS, [], 0.0),
    (SNARE,  "SNARE / CLAP",     RED,    DRUMS_BUS, [(REVERB, SEND)], 0.0),
    (PERC,   "HATS / PERC",      ORANGE, DRUMS_BUS, [], 0.15),
    (DLOW,   "DRUMS LOW",        RED,    DRUMS_BUS, [], 0.0),
    (DMID,   "DRUMS MID",        ORANGE, DRUMS_BUS, [], 0.0),
    (DHIGH,  "DRUMS HIGH",       AMBER,  DRUMS_BUS, [], 0.0),
    (DLOOP,  "DRUM LOOP",        ORANGE, DRUMS_BUS, [], 0.0),
    (BASS1,  "808 / BASS",       PURPLE, BASS_BUS,  [], 0.0),
    (BASS2,  "BASS 2 / LOG DRUM", PURPLE, BASS_BUS, [], 0.0),
    (CHORDS, "CHORDS / KEYS",    BLUE,   MUSIC_BUS, [(REVERB, SEND)], 0.0),
    (MEL1,   "MELODY 1",         TEAL,   MUSIC_BUS, [(REVERB, SEND)], 0.0),
    (MEL2,   "MELODY 2",         TEAL,   MUSIC_BUS, [(REVERB, SEND)], -0.2),
    (MEL3,   "MELODY 3",         TEAL,   MUSIC_BUS, [(REVERB, SEND)], 0.2),
    (FX,     "FX / RISERS",      GREEN,  MUSIC_BUS, [(REVERB, SEND)], 0.0),
    (LEADVOX, "LEAD VOCAL",      GOLD,   VOCAL_BUS, [(REVERB, SEND), (DELAY, SEND)], 0.0),
    (BACKVOX, "BACKING / ADLIBS", GOLD,  VOCAL_BUS, [(REVERB, 0.5), (DELAY, SEND)], 0.0),
    (REF,    "FULL MIX (REF)",   WHITE,  MASTER,    [], 0.0),
    (DRUMS_BUS, "DRUMS BUS",     RED,    MASTER,    [], 0.0),
    (BASS_BUS,  "BASS BUS",      PURPLE, MASTER,    [], 0.0),
    (MUSIC_BUS, "MUSIC BUS",     BLUE,   MASTER,    [], 0.0),
    (VOCAL_BUS, "VOCAL BUS",     GOLD,   MASTER,    [], 0.0),
    (REVERB, "REVERB",           PINK,   MASTER,    [], 0.0),
    (DELAY,  "DELAY",            PINK,   MASTER,    [], 0.0),
]
NAMES = {t[0]: t[1] for t in LAYOUT}

# ---------------------------------------------------------------- stem matching
# Plain-text matching (no extra Python modules needed).
# "word" = must be a whole word, otherwise any part of the name matches.
def _has(n, words, any_part):
    padded = " " + n + " "
    for w in words:
        if (w in n) if any_part else ((" " + w + " ") in padded):
            return True
    return False

DRUMWORDS = ["drum", "perc", "kit"]

def _band(n, words):
    return _has(n, DRUMWORDS, True) and _has(n, words, False)

def _is_backing(n):
    return _has(n, ["backing", "bgv", "harmon", "double", "adlib", "ad lib", "choir",
                    "chant", "stack", "response", "dbl"], True) or _has(n, ["bv", "bvs"], False)

def _is_vocal(n):
    return _has(n, ["vox", "vocal", "voice", "acapella", "acappella", "lead vo", "singing"], True) \
        or _has(n, ["hook", "verse", "rap", "sing"], False)

RULES = [
    (REF,     lambda n: _has(n, ["full mix", "fullmix", "mixdown", "mix down", "reference",
                                 "instrumental", "full song"], True)
                        or _has(n, ["ref", "master", "mastered", "demo"], False)),
    (BACKVOX, lambda n: _is_backing(n) and (_is_vocal(n) or _has(n, ["adlib", "ad lib", "choir", "chant", "bgv"], True))),
    (LEADVOX, _is_vocal),
    (FX,      lambda n: _has(n, ["riser", "uplift", "downlift", "impact", "sweep", "whoosh",
                                 "reverse", "transition"], True)
                        or _has(n, ["fx", "sfx", "rise", "noise", "boom"], False)),
    (KICK,    lambda n: _has(n, ["kick"], True) or _has(n, ["kik", "bd"], False)),
    (SNARE,   lambda n: _has(n, ["snare", "clap", "snap"], True) or _has(n, ["rim", "rimshot", "sd"], False)),
    (DLOW,    lambda n: _band(n, ["low", "lo", "lows"])),
    (DMID,    lambda n: _band(n, ["mid", "mids", "middle"])),
    (DHIGH,   lambda n: _band(n, ["high", "hi", "highs"]) and not _has(n, ["hat"], True)),
    (BASS2,   lambda n: _has(n, ["log drum", "logdrum"], True)),
    (BASS1,   lambda n: _has(n, ["808", "bass"], True) or _has(n, ["sub"], False)),
    (PERC,    lambda n: _has(n, ["hat", "shaker", "shkr", "perc", "conga", "bongo", "cymbal", "crash",
                                 "tamb", "cowbell", "djembe", "talking drum", "clave", "guiro",
                                 "cabasa", "agogo"], True)
                        or _has(n, ["hh", "top", "tops", "tom", "toms", "ride"], False)),
    (DLOOP,   lambda n: not _has(n, ["melod"], True) and (_has(n, ["drum", "groove", "break"], True) or _has(n, ["kit"], False))),
    (CHORDS,  lambda n: _has(n, ["chord", "keys", "piano", "rhodes", "organ", "wurli", "epiano"], True)
                        or _has(n, ["pad", "pads", "ep"], False)),
]
MELODY_SLOTS = [MEL1, MEL2, MEL3]


def _clean(name):
    out = []
    for ch in name.lower():
        out.append(ch if ch.isalnum() else " ")
    return " ".join("".join(out).split())


def pick_track(name, melody_map):
    n = _clean(name)
    for track, test in RULES:
        if test(n):
            return track
    # everything else is a melody: spread across MELODY 1-3
    if n not in melody_map:
        melody_map[n] = MELODY_SLOTS[len(melody_map) % len(MELODY_SLOTS)]
    return melody_map[n]


# ---------------------------------------------------------------- helpers
def _rgb(c):
    return utils.RGBToColor(c[0], c[1], c[2])


def _route(src, dst, on):
    try:
        mixer.setRouteTo(src, dst, on, False)
    except TypeError:
        mixer.setRouteTo(src, dst, on)


def layout_present():
    return mixer.getTrackName(DRUMS_BUS) == NAMES[DRUMS_BUS]


def mixer_is_untouched():
    for i in range(1, LAST + 1):
        n = mixer.getTrackName(i)
        if n and n != "Insert %d" % i:
            return False
    return True


# ---------------------------------------------------------------- build
def build():
    for idx, name, colour, dest, sends, pan in LAYOUT:
        mixer.setTrackName(idx, name)
        mixer.setTrackColor(idx, _rgb(colour))
        try:
            mixer.setTrackPan(idx, pan)
        except Exception:
            pass
    for idx, name, colour, dest, sends, pan in LAYOUT:
        if dest != MASTER:
            _route(idx, MASTER, False)
        _route(idx, dest, True)
    mixer.afterRoutingChanged()
    # Sends: only if this FL version lets us set their level (FL 21 / API 30 can't).
    # Otherwise a full-level send would play those sounds twice.
    sends_ok = True
    for idx, name, colour, dest, sends, pan in LAYOUT:
        for s, lvl in sends:
            _route(idx, s, True)
            try:
                mixer.setRouteToLevel(idx, s, lvl)
            except Exception:
                _route(idx, s, False)
                sends_ok = False
    mixer.afterRoutingChanged()
    if not sends_ok:
        print("[Stem Mixer] Note: this FL version can't set send levels, so no reverb/delay "
              "sends were made. See the guide to add them by hand.")
    try:
        if not mixer.isTrackMuted(REF):
            mixer.muteTrack(REF)
    except Exception:
        pass
    print("[Stem Mixer] Mixer built: 23 tracks.")


# ---------------------------------------------------------------- route stems
def route_stems():
    # FL 21 (scripting v30): use plain channel numbers (no "global index" argument)
    count = channels.channelCount()
    melody_map = {}
    moved = 0
    for i in range(count):
        try:
            name = channels.getChannelName(i)
            target = channels.getTargetFxTrack(i)
        except Exception as e:
            print("[Stem Mixer] could not read channel %d: %r" % (i, e))
            continue
        if target > LAST:          # you placed it yourself: leave it
            continue
        if name.strip().lower() in ("sampler", "3x osc", "fpc"):  # empty default channels
            continue
        track = pick_track(name, melody_map)
        if track != target:
            try:
                channels.setTargetFxTrack(i, track)
            except Exception as e:
                print("[Stem Mixer] could not route %s: %r" % (name, e))
                continue
            moved += 1
        print("[Stem Mixer]  %-40s -> %d %s" % (name[:40], track, NAMES[track]))
    print("[Stem Mixer] Routed %d stem(s). Check the list above; fix any by hand." % moved)


def run():
    if not layout_present():
        if mixer_is_untouched():
            build()
        else:
            print("[Stem Mixer] This project already has its own mixer names, so I left it "
                  "alone. Use File > New, then pick Stem Mixer again.")
            return
    route_stems()




def OnInit():
    try:
        run()
    except Exception as e:
        print("[Stem Mixer] ERROR: %r" % (e,))


def OnMidiMsg(event):
    # any note C5 (60) re-runs it, if you have a keyboard
    if (event.status & 0xF0) == 0x90 and event.data1 == 60 and event.data2 > 0:
        run()
        event.handled = True

