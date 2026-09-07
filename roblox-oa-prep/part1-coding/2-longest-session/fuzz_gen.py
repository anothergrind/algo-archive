"""Random small play streams for P2, with K spanning 0 .. n+1."""

GAMES = ["ob", "jb", "ad", "bs"]


def gen(rng):
    n = rng.randrange(0, 14)
    K = rng.randrange(0, n + 2)
    lines = ["%d %d" % (n, K)]
    if n:
        # narrow alphabet so long runs and full-distinct stretches both occur
        alpha = GAMES[:rng.randrange(1, len(GAMES) + 1)]
        lines.append(" ".join(rng.choice(alpha) for _ in range(n)))
    else:
        lines.append("")
    return "\n".join(lines)
