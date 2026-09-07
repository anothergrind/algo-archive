"""Exhaustive verifier for the Foundry puzzle.

Enumerates every legal machine mix and reports the true optimum, so the answer in
SOLUTION.md is proved rather than asserted.

usage: python solver.py [ore] [slots] [power]
"""
import sys

ORE, SLOTS, POWER = 90, 12, 34
if len(sys.argv) > 3:
    ORE, SLOTS, POWER = map(int, sys.argv[1:4])

# (ore in, gravel out), (gravel in, ingot out), (ingot in, plate out)
CRUSH_IN, CRUSH_OUT, CRUSH_MW = 30, 60, 4
SMELT_IN, SMELT_OUT, SMELT_MW = 45, 15, 3
PRESS_IN, PRESS_OUT, PRESS_MW = 20, 10, 5


def plates(c, s, p):
    ore = min(CRUSH_IN * c, ORE)
    gravel = ore * CRUSH_OUT / CRUSH_IN
    gravel_used = min(gravel, SMELT_IN * s)
    ingot = gravel_used * SMELT_OUT / SMELT_IN
    ingot_used = min(ingot, PRESS_IN * p)
    return ingot_used * PRESS_OUT / PRESS_IN


best, winners = -1.0, []
for c in range(SLOTS + 1):
    for s in range(SLOTS + 1 - c):
        for p in range(SLOTS + 1 - c - s):
            if CRUSH_MW * c + SMELT_MW * s + PRESS_MW * p > POWER:
                continue
            out = plates(c, s, p)
            if out > best + 1e-9:
                best, winners = out, [(c, s, p)]
            elif abs(out - best) < 1e-9:
                winners.append((c, s, p))

print("ore=%d slots=%d power=%d" % (ORE, SLOTS, POWER))
print("optimum: %.4f plates/min" % best)
mins = min(winners, key=lambda t: (sum(t),
                                   CRUSH_MW * t[0] + SMELT_MW * t[1] + PRESS_MW * t[2]))
print("configs achieving it: %d" % len(winners))
print("cheapest such config: crushers=%d smelters=%d pressers=%d "
      "(slots %d, power %d MW)"
      % (mins[0], mins[1], mins[2], sum(mins),
         CRUSH_MW * mins[0] + SMELT_MW * mins[1] + PRESS_MW * mins[2]))
for w in sorted(winners)[:12]:
    print("   c=%d s=%d p=%d  slots=%d power=%d"
          % (w[0], w[1], w[2], sum(w),
             CRUSH_MW * w[0] + SMELT_MW * w[1] + PRESS_MW * w[2]))
