"""Random small grids for P1, biased toward ties and all-negative plots."""


def gen(rng):
    R = rng.randrange(1, 7)
    C = rng.randrange(1, 7)
    k = rng.randrange(1, min(R, C) + 1)
    # tiny value range so equal-sum blocks (and the tie-break) come up often
    lo, hi = rng.choice([(-2, 2), (-3, -1), (0, 0), (1, 1), (-1, 1)])
    lines = ["%d %d %d" % (R, C, k)]
    for _ in range(R):
        lines.append(" ".join(str(rng.randint(lo, hi)) for _ in range(C)))
    return "\n".join(lines)
