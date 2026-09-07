"""P5 Username Aliases -- reference solution. Normalise, group, order.

time  O(n * L + G log G)   L = username length, G = number of groups
space O(n * L)
"""
import sys

STRIP = set("_.-")


def normalise(name):
    s = "".join(c for c in name.lower() if c not in STRIP)
    i = len(s)
    while i > 0 and s[i - 1].isdigit():
        i -= 1
    return s[:i] if i > 0 else s        # all-digit names keep their digits


def solve(lines):
    rows = [ln for ln in lines if ln.strip()]
    if not rows:
        return []
    n = int(rows[0])
    groups = {}                          # key -> [members in first-seen order]
    seen = set()                         # exact duplicates collapse
    for name in rows[1:1 + n]:
        if name in seen:
            continue
        seen.add(name)
        groups.setdefault(normalise(name), []).append(name)

    order = sorted(groups, key=lambda k: (-len(groups[k]), k))
    return ["%s %d %s" % (k, len(groups[k]), " ".join(groups[k])) for k in order]


if __name__ == "__main__":
    out = solve(sys.stdin.read().splitlines())
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
