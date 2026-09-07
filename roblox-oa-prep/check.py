"""Verify every reference solution still reproduces its committed expected output.

usage: python roblox-oa-prep/check.py
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
fails = total = 0

for d in sorted(glob.glob(os.path.join(ROOT, "part1-coding", "*", ""))):
    if not os.path.exists(d + "code.py"):
        continue
    for src in sorted(glob.glob(os.path.join(d, "tests", "*.in"))):
        dst = src[:-3] + ".out"
        if not os.path.exists(dst):
            continue
        with open(src, "rb") as fh:
            r = subprocess.run([sys.executable, d + "code.py"],
                               stdin=fh, capture_output=True)
        got = r.stdout.decode().replace("\r\n", "\n").strip("\n")
        if r.returncode != 0:
            got = "<<CRASH>> " + r.stderr.decode().strip().splitlines()[-1]
        want = open(dst).read().strip("\n")
        total += 1
        if got != want:
            fails += 1
            print("FAIL %s\n  want: %r\n  got : %r"
                  % (os.path.relpath(dst, ROOT), want, got))

print("%d/%d cases match" % (total - fails, total))
sys.exit(1 if fails else 0)
