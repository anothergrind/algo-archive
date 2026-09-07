"""Regenerate every tests/<name>.p<N>.out from the reference solutions.

usage: python stripe-oa-prep/gen_expected.py [problem-dir ...]
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
dirs = sys.argv[1:] or sorted(
    d for d in glob.glob(os.path.join(ROOT, "*", "")) if os.path.exists(d + "code.py")
)

for d in dirs:
    for src in sorted(glob.glob(os.path.join(d, "tests", "*.in"))):
        base = src[:-3]
        for part in (1, 2, 3, 4):
            with open(src, "rb") as fh:
                r = subprocess.run(
                    [sys.executable, os.path.join(d, "code.py"), str(part)],
                    stdin=fh, capture_output=True,
                )
            dst = "%s.p%d.out" % (base, part)
            if r.returncode != 0:
                body = "<<CRASH>> " + r.stderr.decode().strip().splitlines()[-1]
            else:
                body = r.stdout.decode().replace("\r\n", "\n").strip("\n")
            with open(dst, "w", newline="\n") as fh:
                fh.write(body + "\n" if body else "")
            print("%-40s p%d  %s" % (
                os.path.relpath(dst, ROOT), part,
                body.replace("\n", " / ")[:100] or "<empty>"))
