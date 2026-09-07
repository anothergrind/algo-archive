"""Regenerate every part1-coding/*/tests/<name>.out from the reference solution.

usage: python roblox-oa-prep/gen_expected.py
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

for d in sorted(glob.glob(os.path.join(ROOT, "part1-coding", "*", ""))):
    if not os.path.exists(d + "code.py"):
        continue
    for src in sorted(glob.glob(os.path.join(d, "tests", "*.in"))):
        with open(src, "rb") as fh:
            r = subprocess.run([sys.executable, d + "code.py"],
                               stdin=fh, capture_output=True)
        if r.returncode != 0:
            body = "<<CRASH>> " + r.stderr.decode().strip().splitlines()[-1]
        else:
            body = r.stdout.decode().replace("\r\n", "\n").strip("\n")
        dst = src[:-3] + ".out"
        with open(dst, "w", newline="\n") as fh:
            fh.write(body + "\n" if body else "")
        print("%-52s %s" % (os.path.relpath(dst, ROOT),
                            body.replace("\n", " / ")[:70] or "<empty>"))
