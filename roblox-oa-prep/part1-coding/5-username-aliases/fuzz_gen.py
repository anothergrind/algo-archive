"""Random small username lists for P5: separators, digits, case, duplicates."""

CHARS = "aAbB._-019"


def gen(rng):
    n = rng.randrange(0, 10)
    lines = [str(n)]
    pool = []
    for _ in range(max(n, 1)):
        L = rng.randrange(1, 6)
        name = "".join(rng.choice(CHARS) for _ in range(L))
        if not any(c.isalnum() for c in name):      # guaranteed by constraints
            name += "a"
        pool.append(name)
    for _ in range(n):
        lines.append(rng.choice(pool))              # repeats -> exact duplicates
    return "\n".join(lines)
