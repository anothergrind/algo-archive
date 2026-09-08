"""Run your own mine.py against the committed expected output.

usage: python stripe-oa-prep/check_mine.py [problem-substring] [part] [--show]

    python stripe-oa-prep/check_mine.py            # every problem, every part
    python stripe-oa-prep/check_mine.py fee        # just 1-fee-engine
    python stripe-oa-prep/check_mine.py fee 1      # just part 1 of it
    python stripe-oa-prep/check_mine.py fee 1 --show   # also spoil hidden cases

Pass the part you are actually on -- with no part filter this reports all four,
and the parts you have not written yet will read as a wall of failures.

Failures on `sample*` inputs print the full diff, because those samples are in
README.md already. Failures on `hidden*` inputs print only the case name unless
you pass --show: knowing which edge case broke is the useful half, and the
expected output is the part SPOILERS.md is meant to gate.
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

args = [a for a in sys.argv[1:] if a != "--show"]
show = "--show" in sys.argv[1:]
name_filter = args[0] if args else None
part_filter = int(args[1]) if len(args) > 1 else None
if part_filter is not None and part_filter not in (1, 2, 3, 4):
    print("part must be 1-4, got %d" % part_filter)
    sys.exit(2)

dirs = [d for d in sorted(glob.glob(os.path.join(ROOT, "*", "")))
        if os.path.exists(d + "mine.py")
        and (name_filter is None or name_filter in os.path.basename(d.rstrip("/\\")))]

if not dirs:
    print("no mine.py matching %r" % name_filter)
    sys.exit(1)

parts = [part_filter] if part_filter else [1, 2, 3, 4]
tally = {p: [0, 0] for p in parts}   # part -> [passed, total]
skipped = []

for d in dirs:
    tag = os.path.basename(d.rstrip("/\\"))
    for part in parts:
        for src in sorted(glob.glob(os.path.join(d, "tests", "*.in"))):
            dst = "%s.p%d.out" % (src[:-3], part)
            if not os.path.exists(dst):
                continue
            case = os.path.basename(src)[:-3]
            with open(src, "rb") as fh:
                r = subprocess.run([sys.executable, d + "mine.py", str(part)],
                                   stdin=fh, capture_output=True)
            got = r.stdout.decode().replace("\r\n", "\n").strip("\n")
            if r.returncode != 0:
                err = r.stderr.decode().strip().splitlines()
                got = "<<CRASH>> " + (err[-1] if err else "no stderr")
            want = open(dst).read().strip("\n")
            if want.startswith("<<CRASH>>"):
                # This input/part pairing is not one of the meaningful ones: the
                # input uses record types or guarantees that only a later part
                # is promised, so even the reference solution crashes on it.
                skipped.append("%s part %d %s" % (tag, part, case))
                continue
            tally[part][1] += 1
            if got == want:
                tally[part][0] += 1
            elif case.startswith("hidden") and not show:
                print("FAIL %s part %d  %s  (rerun with --show to see it)"
                      % (tag, part, case))
            else:
                print("FAIL %s part %d  %s\n  want: %r\n  got : %r"
                      % (tag, part, case, want, got))

print("")
if skipped:
    print("skipped %d input/part pairing(s) the problem never promises: %s"
          % (len(skipped), ", ".join(skipped)))
for part in parts:
    ok, tot = tally[part]
    print("part %d: %d/%d" % (part, ok, tot) + ("  <-- green" if ok == tot and tot else ""))
sys.exit(0 if all(ok == tot for ok, tot in tally.values()) else 1)
