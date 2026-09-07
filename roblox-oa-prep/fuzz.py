"""Differential-test each reference solution against its naive oracle.

Every part1 problem ships a brute.py written a deliberately different way and a
fuzz_gen.py that emits small random inputs. If code.py and brute.py ever disagree,
the reference is wrong (or the problem is under-specified) -- print the input and
exit nonzero.

usage: python roblox-oa-prep/fuzz.py [iterations]
"""
import glob
import importlib.util
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ITERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3000


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bad = 0
for d in sorted(glob.glob(os.path.join(ROOT, "part1-coding", "*", ""))):
    need = ["code.py", "brute.py", "fuzz_gen.py"]
    if not all(os.path.exists(d + f) for f in need):
        print("SKIP %s (missing oracle)" % os.path.relpath(d, ROOT))
        continue
    tag = os.path.basename(d.rstrip("/\\"))
    ref = load(d + "code.py", tag + "_ref")
    bru = load(d + "brute.py", tag + "_bru")
    gen = load(d + "fuzz_gen.py", tag + "_gen")

    rng = random.Random(20260906)
    for i in range(ITERS):
        text = gen.gen(rng)
        lines = text.splitlines()
        a = ref.solve(list(lines))
        b = bru.solve(list(lines))
        if a != b:
            bad += 1
            print("DIVERGENCE in %s at iteration %d" % (tag, i))
            print("--- input ---\n%s" % text)
            print("--- code.py  -> %r" % (a,))
            print("--- brute.py -> %r" % (b,))
            break
    else:
        print("%-26s %d random inputs, no divergence" % (tag, ITERS))

sys.exit(1 if bad else 0)
