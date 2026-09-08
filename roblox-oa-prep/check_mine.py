"""Run your own mine.py against the committed expected output.

usage: python roblox-oa-prep/check_mine.py [problem-substring] [--show]

    python roblox-oa-prep/check_mine.py           # all five part1 problems
    python roblox-oa-prep/check_mine.py session   # just 2-longest-session
    python roblox-oa-prep/check_mine.py session --show   # also spoil hidden cases

Failures on `sample*` inputs print the full diff -- those samples are worked in
README.md already. Failures on `hidden*` inputs print only the case name unless
you pass --show, so you learn which edge case broke without being handed the
answer SOLUTION.md is meant to gate.
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

args = [a for a in sys.argv[1:] if a != "--show"]
show = "--show" in sys.argv[1:]
name_filter = args[0] if args else None

dirs = [d for d in sorted(glob.glob(os.path.join(ROOT, "part1-coding", "*", "")))
        if os.path.exists(d + "mine.py")
        and (name_filter is None or name_filter in os.path.basename(d.rstrip("/\\")))]

if not dirs:
    print("no mine.py matching %r" % name_filter)
    sys.exit(1)

fails = total = 0
for d in dirs:
    tag = os.path.basename(d.rstrip("/\\"))
    ok = n = 0
    for src in sorted(glob.glob(os.path.join(d, "tests", "*.in"))):
        dst = src[:-3] + ".out"
        if not os.path.exists(dst):
            continue
        case = os.path.basename(src)[:-3]
        with open(src, "rb") as fh:
            r = subprocess.run([sys.executable, d + "mine.py"],
                               stdin=fh, capture_output=True)
        got = r.stdout.decode().replace("\r\n", "\n").strip("\n")
        if r.returncode != 0:
            err = r.stderr.decode().strip().splitlines()
            got = "<<CRASH>> " + (err[-1] if err else "no stderr")
        want = open(dst).read().strip("\n")
        n += 1
        if got == want:
            ok += 1
        elif case.startswith("hidden") and not show:
            print("FAIL %s  %s  (rerun with --show to see it)" % (tag, case))
        else:
            print("FAIL %s  %s\n  want: %r\n  got : %r" % (tag, case, want, got))
    print("%-26s %d/%d" % (tag, ok, n) + ("  <-- green" if ok == n and n else ""))
    total += n
    fails += n - ok

print("\n%d/%d cases match" % (total - fails, total))
sys.exit(1 if fails else 0)
