"""P3 Match and Collapse -- your solution.

usage: python mine.py   # the input arrives on stdin

    python mine.py < tests/sample1.in | diff - tests/sample1.out
    python ../../check_mine.py 3-match-collapse
    python ../../fuzz_mine.py 3-match-collapse   # vs brute.py over random inputs
"""
import sys


def solve(lines):
    """Compute the answer. `lines` is not anything you have to set up -- the
    `__main__` block at the bottom of this file builds it and hands it to you.

    `lines` is the whole of stdin, already read and split into a list of strings
    with the trailing newlines stripped. You never touch stdin yourself. For
    tests/sample1.in it is literally this list:

        [
            '5 3',
            'aaa',
            'bcb',
            'bcb',
            'bcb',
            'abc',
        ]

    Blank lines are kept, so skip them yourself if the format allows them.

    Return a list of strings, one per line of output. Not one big string with
    newlines in it, and do not print -- the bottom of the file joins your list
    with "\n" and prints the result, so anything you print in here lands in the
    middle of your answer and fails the diff. Even a one-number answer is a
    one-element list of one string. For the input above (this is
    tests/sample1.out):

        [
            '...',
            '...',
            '...',
            '...',
            'abc',
        ]

    Keep this a plain function taking `lines` and returning a list: fuzz_mine.py
    imports it directly and compares it against brute.py over random inputs.
    """
    out = []
    # TODO -- build up `out`, one string per line of output
    return out


if __name__ == "__main__":
    out = solve(sys.stdin.read().splitlines())
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
