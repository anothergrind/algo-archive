"""Settlement Ledger -- your solution. All four parts live in here.

usage: python mine.py <part>   # the input arrives on stdin

    python mine.py 1 < tests/sample1.in | diff - tests/sample1.p1.out
    python ../check_mine.py 5-settlement-ledger 1

Work part 1 to green before reading part 2 in README.md. Extend `solve` part by
part rather than rewriting it -- that is the whole point of the format.
"""
import sys


def solve(part, lines):
    """Compute the answer for one part. Neither argument is anything you have to
    set up -- the `__main__` block at the bottom of this file builds both and
    hands them to you.

    `part` is an int, 1 to 4: which part of README.md you are implementing. It
    comes straight off the command line, so `python mine.py 3` calls this with
    part == 3. It exists because all four parts share this one function, and
    each part changes both the rules and the output format -- so branch on it:

        if part == 1:
            ...
        elif part == 2:
            ...

    The parts are cumulative (part 3 is part 2 plus one more rule), so in
    practice most of the body ends up shared and only the differences are
    guarded, often as `if part >= 3:`.

    `lines` is the whole of stdin, already read and split into a list of strings
    with the trailing newlines stripped. You never touch stdin yourself. For
    tests/sample1.in it is literally this list:

        [
            'OPEN|acct_a|100000',
            'OPEN|acct_b|0',
            'OPEN|acct_c|5000',
            'XFER|t1|2024-09-02T09:00|acct_a|acct_b|25000',
            'XFER|t2|2024-09-02T10:00|acct_b|acct_c|30000',
            'XFER|t3|2024-09-02T11:00|acct_a|acct_z|1000',
            'XFER|t4|2024-09-02T12:00|acct_c|acct_c|100',
            'XFER|t5|2024-09-02T13:00|acct_a|acct_c|25000',
            'XFER|t1|2024-09-02T14:00|acct_a|acct_c|1',
        ]

    Blank lines are kept, so skip them yourself if the format allows them.

    Return a list of strings, one per line of output. Not one big string with
    newlines in it, and do not print -- the bottom of the file joins your list
    with "\n" and prints the result, so anything you print in here lands in the
    middle of your answer and fails the diff. For the input above, part 1 wants
    you to return exactly (this is tests/sample1.p1.out):

        [
            'acct_a|50000',
            'acct_b|25000',
            'acct_c|30000',
        ]
    """
    out = []
    # TODO -- build up `out`, one string per line of output
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
