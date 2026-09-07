"""Random small boards for P3: tiny alphabet so runs, cascades and L-shapes abound."""


def gen(rng):
    R = rng.randrange(1, 7)
    C = rng.randrange(1, 7)
    alpha = ["a", "b", "."][:rng.choice([2, 2, 3])]
    lines = ["%d %d" % (R, C)]
    for _ in range(R):
        lines.append("".join(rng.choice(alpha) for _ in range(C)))
    return "\n".join(lines)
