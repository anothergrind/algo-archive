"""Verify every reference solution still reproduces its committed expected output.

usage: python stripe-oa-prep/check.py
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
fails = 0
total = 0

for d in sorted(glob.glob(os.path.join(ROOT, "*", ""))):
    if not os.path.exists(d + "code.py"):
        continue
    for src in sorted(glob.glob(os.path.join(d, "tests", "*.in"))):
        for part in (1, 2, 3, 4):
            dst = "%s.p%d.out" % (src[:-3], part)
            if not os.path.exists(dst):
                continue
            with open(src, "rb") as fh:
                r = subprocess.run([sys.executable, d + "code.py", str(part)],
                                   stdin=fh, capture_output=True)
            got = r.stdout.decode().replace("\r\n", "\n").strip("\n")
            if r.returncode != 0:
                got = "<<CRASH>> " + r.stderr.decode().strip().splitlines()[-1]
            want = open(dst).read().strip("\n")
            total += 1
            if got != want:
                fails += 1
                print("FAIL %s part %d" % (os.path.relpath(dst, ROOT), part))
                print("  want: %r" % want)
                print("  got : %r" % got)

print("%d/%d cases match" % (total - fails, total))
sys.exit(1 if fails else 0)
