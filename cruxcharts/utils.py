"""
    ASCENT2COLOR,
    DIFFICULTY2COLOR,
    GRADE2DIFFICULTY,
    HUECO2FONT,
    FONT2HUECO,
    YDS2FRENCH,
    FRENCH2YDS,
    YDS2BRITISH,
    BRITISH2YDS,
"""

from collections import defaultdict


ASCENT2COLOR = {
    "Solo": "#ffffb3",
    "O/S": "#8dd3c7",
    "β": "#80b1d3",
    "Redpoint": "#fb8072",
    "Repeat": "#b3b3b3"
}


DIFFICULTY2COLOR = {
    'EASY': '#66c2a5',
    'MODERATE': '#ff9933',
    'HARD': '#b30000',
    'VERYHARD': '#66ccff',
    'ELITE': '#e6e6e6'}


HUECO2FONT = {
    "VB":  ["f2", "f2+", "f3"],
    "V0":  ["f3+", "f4", "f4+"],
    "V1":  ["f5"],
    "V2":  ["f5+"],
    "V3":  ["f6A", "f6A+"],
    "V4":  ["f6B", "f6B+"],
    "V5":  ["f6C", "f6C+"],
    "V6":  ["f7A"],
    "V7":  ["f7A+"],
    "V8":  ["f7B", "f7B+"],
    "V9":  ["f7B+", "f7C"],
    "V10": ["f7C+"],
    "V11": ["f8A"],
    "V12": ["f8A+"],
    "V13": ["f8B"],
    "V14": ["f8B+"],
    "V15": ["f8C"],
    "V16": ["f8C+"],
    "V17": ["f9A"],
}


FONT2HUECO = defaultdict(list)
for (hueco, fonts) in HUECO2FONT.items():
    for f in fonts:
        FONT2HUECO[f].append(hueco)


YDS2FRENCH = {
    "5.1":   ["1"],
    "5.2":   ["2"],
    "5.3":   ["3a"],
    "5.4":   ["3b"],
    "5.5":   ["3c"],
    "5.6":   ["4a"],
    "5.7":   ["4b"],
    "5.8":   ["4c", "5a"],
    "5.9":   ["5b"],
    "5.10a": ["5c"],
    "5.10b": ["6a", "6a+"],
    "5.10c": ["6b"],
    "5.10d": ["6b+"],
    "5.11a": ["6b+", "6c"],
    "5.11b": ["6c"],
    "5.11c": ["6c+"],
    "5.11d": ["7a"],
    "5.12a": ["7a+"],
    "5.12b": ["7b"],
    "5.12c": ["7b+"],
    "5.12d": ["7c"],
    "5.13a": ["7c+"],
    "5.13b": ["8a"],
    "5.13c": ["8a+"],
    "5.13d": ["8b"],
    "5.14a": ["8b+"],
    "5.14b": ["8c"],
    "5.14c": ["8c+"],
    "5.14d": ["9a"],
    "5.15a": ["9a+"],
    "5.15b": ["9b"],
    "5.15c": ["9b+"],
    "5.15d": ["9c"],
}


FRENCH2YDS = defaultdict(list)
for (y, frenchies) in YDS2FRENCH.items():
    for f in frenchies:
        FRENCH2YDS[f].append(y)


# TODO: Add G, PG, R, X ratings to YDS
BRITISH2YDS = {
    "M":      ["5.1", "5.2"],
    "D":      ["5.2", "5.3"],
    "VD":     ["5.3", "5.4"],
    "HVD":    ["5.4", "5.5"],
    "S":      ["5.5", "5.6"],
    "HS":     ["5.5", "5.6", "5.7"],
    "VS 4a":  ["5.6"],
    "VS 4b":  ["5.7"],
    "VS 4c":  ["5.8"],
    "HVS 4c": ["5.8"],
    "HVS 5a": ["5.9"],
    "HVS 5b": ["5.10a"],
    "E1 5a":  ["5.9"],
    "E1 5b":  ["5.10a"],
    "E1 5c":  ["5.10b"],
    "E2 5b":  ["5.10b"],
    "E2 5c":  ["5.10b"],
    "E2 6a":  ["5.10c"],
    "E3 5c":  ["5.10c"],
    "E3 6a":  ["5.10d", "5.11a"],
    "E4 6a":  ["5.10d", "5.11a", "5.11b"],
    "E4 6b":  ["5.11b", "5.11c", "5.11d"],
    "E5 6a":  ["5.11b", "5.11c"],
    "E5 6b":  ["5.11d", "5.12a"],
    "E5 6c":  ["5.12a", "5.12b"],
    "E6 6b":  ["5.11d", "5.12b"],
    "E6 6c":  ["5.12c", "5.13a"],
    "E7 6c":  ["5.12b", "5.12c", "5.12d"],
    "E7 7a":  ["5.13a", "5.13b", "5.13c"],
    "E8 6c":  ["5.12d", "5.13a", "5.13b"],
    "E8 7a":  ["5.13c", "5.13d", "5.14a"],
    "E9 7a":  ["5.13a", "5.13b", "5.13c"],
    "E9 7b":  ["5.13d", "5.14a", "5.14b", "5.14c"],
    "E10 7a": ["5.13c", "5.13d", "5.14a", "5.14b"],
    "E10 7b": ["5.14c", "5.14d", "5.15a"],
    "E11 7a": ["5.14a", "5.14b", "5.14c"],
    "E11 7b": ["5.14d", "5.15a", "5.15b", "5.15c"],
}

YDS2BRITISH = defaultdict(list)
for (brit, ys) in BRITISH2YDS.items():
    for y in ys:
        YDS2BRITISH[y].append(brit)


GRADE2DIFFICULTY = {}
for (i, (hueco, fonts)) in enumerate(HUECO2FONT.items()):
    if i < 2:
        diff = "EASY"
    elif i < 4:
        diff = "MODERATE"
    elif i < 7:
        diff = "HARD"
    elif i < 11:
        diff = "VERYHARD"
    else:
        diff = "ELITE"
    GRADE2DIFFICULTY[hueco] = diff
    for font in fonts:
        GRADE2DIFFICULTY[font] = diff


