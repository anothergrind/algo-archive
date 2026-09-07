"""Tiny towers for P4: small N so the exponential oracle terminates."""


def gen(rng):
    N = rng.randrange(0, 13)
    M = rng.randrange(1, 4)
    heights = rng.sample(range(1, 7), M)
    return "%d %d\n%s" % (N, M, " ".join(map(str, heights)))
