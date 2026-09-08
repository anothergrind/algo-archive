"""P1 Best Build Block -- your solution.

usage: python mine.py   # input on stdin

    python mine.py < tests/sample1.in | diff - tests/sample1.out
    python ../../check_mine.py 1-build-grid-blocks
    python ../../fuzz_mine.py 1-build-grid-blocks   # vs brute.py over random inputs

Keep `solve(lines)` pure and returning a list of strings -- fuzz_mine.py
imports it directly and compares it against brute.py.
"""
import sys


def solve(lines):
    """Return the output lines (no trailing newlines)."""
    out = []
    # TODO
    return out


if __name__ == "__main__":
    out = solve(sys.stdin.read().splitlines())
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
