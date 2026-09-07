"""Deliberately naive oracle for P5: pairwise grouping, selection sort.

time O(n^2). Only used by fuzz.py to differential-test code.py.
"""


def normalise(name):
    s = ""
    for c in name.lower():
        if c != "_" and c != "." and c != "-":
            s += c
    trimmed = s
    while trimmed and trimmed[-1] in "0123456789":
        trimmed = trimmed[:-1]
    return trimmed if trimmed else s


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    n = int(rows[0])

    uniq = []
    for name in rows[1:1 + n]:
        if name not in uniq:
            uniq.append(name)

    keys, members = [], []
    for name in uniq:
        k = normalise(name)
        if k in keys:
            members[keys.index(k)].append(name)
        else:
            keys.append(k)
            members.append([name])

    out = []
    while keys:
        best = 0
        for i in range(1, len(keys)):
            if len(members[i]) > len(members[best]):
                best = i
            elif len(members[i]) == len(members[best]) and keys[i] < keys[best]:
                best = i
        out.append("%s %d %s" % (keys[best], len(members[best]),
                                 " ".join(members[best])))
        keys.pop(best)
        members.pop(best)
    return out
