"""Account Lifecycle Machine -- your solution. All four parts live in here.

usage: python mine.py <part>   # the input arrives on stdin

    python mine.py 1 < tests/sample1.in | diff - tests/sample1.p1.out
    python ../check_mine.py 3-account-state-machine 1

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
            '2024-01-01T00:00:00Z,k01,acc_1,OPEN,',
            '2024-01-01T00:01:00Z,k02,acc_1,VERIFY,',
            '2024-01-01T00:02:00Z,k03,acc_2,VERIFY,',
            '2024-01-01T00:03:00Z,k04,acc_2,OPEN,',
            '2024-01-01T00:04:00Z,k05,acc_1,SUSPEND,',
            '2024-01-01T00:05:00Z,k06,acc_1,REINSTATE,',
            '2024-01-01T00:06:00Z,k07,acc_3,OPEN,',
            '2024-01-01T00:07:00Z,k08,acc_3,CLOSE,',
            '2024-01-01T00:08:00Z,k09,acc_3,VERIFY,',
            '2024-01-01T00:09:00Z,k10,acc_1,DEPOSIT,5000',
            '2024-01-01T00:10:00Z,k11,acc_1,WITHDRAW,6000',
            '2024-01-01T00:11:00Z,k12,acc_1,WITHDRAW,1500',
            '2024-01-01T00:12:00Z,k13,acc_2,DEPOSIT,999',
        ]

    Blank lines are kept, so skip them yourself if the format allows them.

    Return a list of strings, one per line of output. Not one big string with
    newlines in it, and do not print -- the bottom of the file joins your list
    with "\n" and prints the result, so anything you print in here lands in the
    middle of your answer and fails the diff. For the input above, part 1 wants
    you to return exactly (this is tests/sample1.p1.out):

        [
            'acc_1,ACTIVE',
            'acc_2,PENDING',
            'acc_3,CLOSED',
        ]
    """
    out = []
    # TODO -- build up `out`, one string per line of output
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
