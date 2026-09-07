"""Exhaustive verifier for the Assembly Line puzzle (2-station permutation flow shop).

Brute-forces every ordering to find the true minimum makespan, then checks that
Johnson's rule reproduces it.

usage: python solver.py
"""
from itertools import permutations

# name -> (paint minutes, package minutes)
JOBS = {
    "A": (4, 6),
    "B": (7, 2),
    "C": (3, 5),
    "D": (8, 3),
    "E": (2, 7),
    "F": (5, 4),
}
EXAMPLE = {"A": (3, 4), "B": (5, 2), "C": (1, 6)}


def makespan(seq, jobs):
    paint_free = pack_free = 0
    for name in seq:
        a, b = jobs[name]
        paint_free += a                       # one order at a time on paint
        pack_free = max(pack_free, paint_free) + b   # package waits for paint
    return pack_free


def johnson(jobs):
    head = sorted([n for n in jobs if jobs[n][0] < jobs[n][1]],
                  key=lambda n: jobs[n][0])
    tail = sorted([n for n in jobs if jobs[n][0] >= jobs[n][1]],
                  key=lambda n: -jobs[n][1])
    return head + tail


def report(label, jobs):
    best = min(makespan(p, jobs) for p in permutations(jobs))
    optimal = sorted(p for p in permutations(jobs) if makespan(p, jobs) == best)
    j = johnson(jobs)
    print("%s: %d orderings, best makespan = %d min" % (label, len(optimal), best))
    print("  johnson's rule gives %s -> %d min  %s"
          % ("".join(j), makespan(j, jobs),
             "OPTIMAL" if makespan(j, jobs) == best else "*** NOT OPTIMAL ***"))
    print("  worst possible ordering: %d min"
          % max(makespan(p, jobs) for p in permutations(jobs)))
    print("  all optimal orderings: %s"
          % ", ".join("".join(p) for p in optimal[:8]))


report("worked example", EXAMPLE)
print()
report("the puzzle", JOBS)
