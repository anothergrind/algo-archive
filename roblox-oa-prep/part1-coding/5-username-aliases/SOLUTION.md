# P5 — Username Aliases — solution

**Do not read this until you have an answer.** Back to the problem:
[README.md](README.md)

---

## Approach — canonicalise, bucket, sort by a compound key

Three independent pieces, and the marks are lost in the third one far more often than
the first.

**Canonicalise.** Lowercase, filter out the three separator characters, then walk
backwards over the trailing digits. The "unless it would leave nothing" clause means
you compute the trimmed string and fall back to the untrimmed one when the trim is
total — an all-digit name like `007` keeps its digits and is its own canonical form.

**Bucket.** A dict from canonical form to a list of members, appending in input order,
gives the required member ordering for free. Deduplicate the *raw* username with a
separate `set` before bucketing — the dedup is on exact spelling, not on canonical
form, so it cannot be folded into the grouping.

**Order.** Sort the keys by `(-size, key)`. Sorting by size alone leaves equal-size
groups in dict-insertion order, which is stable but is not what the spec asks for and
will diverge on inputs where the first-seen order differs from ASCII order.

### Complexity

- **Time:** `O(n·L + G log G)` where `L` is the maximum username length (20) and `G` is
  the number of groups. Canonicalising is linear per name; the sort is over groups, not
  names.
- **Space:** `O(n·L)`.

### Reference solution

```python
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
```

Verified against `brute.py` — an `O(n²)` oracle that groups by linear search and orders
by repeated selection — over 4000 random name lists built from an alphabet of letters,
digits, separators and mixed case, with repeats forced so exact duplicates occur.
Run `python roblox-oa-prep/fuzz.py`.

---

## Hidden edge-case tests

### Hidden 1 — exact duplicates and all-digit names (`tests/hidden1_dupes_digits.in`)

```
5
12345
12345
007
bob
bob.
```

```
bob 2 bob bob.
007 1 007
12345 1 12345
```

Three traps at once. The repeated `12345` collapses to a single member, so its group
has size 1 and not 2. Both `12345` and `007` are entirely digits — trimming the
trailing run would empty them, so they keep their digits and, crucially, remain in
*separate* groups; a solution that maps both to the empty string merges them. And the
two size-1 groups tie, so ASCII decides: `007` before `12345`.

### Hidden 2 — empty input (`tests/hidden2_empty.in`)

```
0
```

Output: nothing at all. The count line is present but there are no usernames. Code that
indexes `rows[1]` unconditionally raises here.

### Hidden 3 — digits that are not trailing (`tests/hidden3_inner_digits.in`)

```
4
a1b
a1b2
_-_a_-_
A
```

```
a 2 _-_a_-_ A
a1b 2 a1b a1b2
```

`a1b` keeps its interior `1` — only the trailing run goes, which is why `a1b` and
`a1b2` are aliases while neither is an alias of `ab`. Meanwhile `_-_a_-_` reduces to a
bare `a` and pairs with `A` by lowercasing. Both groups have size 2, so the tie-break
runs, and `a` sorts before `a1b`. A regex like `\d+` applied globally instead of
anchored to the end merges all four into one group.

---

## What this problem is testing

Whether you implement the stated transformation exactly rather than approximately —
"strip digits" versus "strip *trailing* digits", "dedupe exact" versus "dedupe
canonical" — and whether you notice that the output ordering is a compound key. The
algorithm is trivial; every point here is in the specification reading.
