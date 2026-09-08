"""Settlement Ledger -- your solution. All four parts live in here.

usage: python mine.py <part>   # input on stdin

    python mine.py 1 < tests/sample1.in | diff - tests/sample1.p1.out
    python ../check_mine.py 5-settlement-ledger 1

Work part 1 to green before reading part 2 in README.md. Extend `solve`
part by part rather than rewriting it -- that is the whole point of the format.
"""
import sys


def solve(part, lines):
    """Return the output lines (no trailing newlines) for the given part."""
    out = []
    # TODO
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
