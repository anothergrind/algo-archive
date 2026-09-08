"""Differential-test your own mine.py against the naive oracle in brute.py.

This is worth more than check_mine.py. The five committed test cases are five
cases; this throws thousands of small random inputs at your solve() and at a
brute force written a different way, and prints the first input where they
disagree. That is what actually catches a wrong window boundary or a tie-break
you got backwards.

usage: python roblox-oa-prep/fuzz_mine.py [problem-substring] [iterations]

    python roblox-oa-prep/fuzz_mine.py                # all five, 3000 each
    python roblox-oa-prep/fuzz_mine.py session        # just 2-longest-session
    python roblox-oa-prep/fuzz_mine.py 2              # same, matched by number
    python roblox-oa-prep/fuzz_mine.py session 20000  # harder

An empty stub returns [] and diverges on iteration 0 -- that is expected, not a
bug in the harness. Note the printed divergence is a random input, not a hidden
test, so this spoils nothing.
"""
import glob
import importlib.util
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

args = sys.argv[1:]
name_filter = args[0] if args else None   # `4` matches 4-tower-builds, not an iteration count
iters = int(args[1]) if len(args) > 1 else 3000


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dirs = [d for d in sorted(glob.glob(os.path.join(ROOT, "part1-coding", "*", "")))
        if name_filter is None or name_filter in os.path.basename(d.rstrip("/\\"))]
if not dirs:
    print("no problem matching %r" % name_filter)
    sys.exit(1)

bad = 0
for d in dirs:
    tag = os.path.basename(d.rstrip("/\\"))
    missing = [f for f in ("mine.py", "brute.py", "fuzz_gen.py")
               if not os.path.exists(d + f)]
    if missing:
        print("SKIP %-21s (no %s)" % (tag, ", ".join(missing)))
        continue
    mine = load(d + "mine.py", tag + "_mine")
    bru = load(d + "brute.py", tag + "_bru")
    gen = load(d + "fuzz_gen.py", tag + "_gen")

    rng = random.Random(20260906)
    for i in range(iters):
        text = gen.gen(rng)
        lines = text.splitlines()
        try:
            a = mine.solve(list(lines))
        except Exception as exc:
            a = "<<CRASH>> %s: %s" % (type(exc).__name__, exc)
        b = bru.solve(list(lines))
        if a != b:
            bad += 1
            print("DIVERGENCE in %s at iteration %d" % (tag, i))
            print("--- input ---\n%s" % text)
            print("--- mine.py  -> %r" % (a,))
            print("--- brute.py -> %r" % (b,))
            break
    else:
        print("%-26s %d random inputs, no divergence" % (tag, iters))

sys.exit(1 if bad else 0)
