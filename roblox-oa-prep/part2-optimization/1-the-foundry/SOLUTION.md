# Puzzle 1 — The Foundry — solution

**Only open this after you have committed to an answer.** Back to the puzzle:
[README.md](README.md)

---

## Answer

1. **20 plates per minute.**
2. **2 crushers, 3 smelters, 2 pressers** — 7 slots.
3. That mix draws `8 + 9 + 10 = 27` MW of your 34. The remaining 7 MW is unspendable:
   no machine you could add with it increases output.

Proved by exhaustive search over every legal mix — run `python solver.py`.

---

## Reasoning

### First, find the unconstrained ceiling

Ignore power for a moment. Ore at 90/min supports 3 crushers, which emit 180
gravel/min. That supports 4 smelters (`180 / 45 = 4` exactly), emitting 60 ingots/min.
That supports 3 pressers (`60 / 20 = 3` exactly), emitting **30 plates/min**.

So `3, 4, 3` — 10 slots — would give 30 plates/min. Its power draw is
`12 + 12 + 15 = 39` MW. You have 34. **Power is the binding constraint, not ore and
not slots.**

### Then, find what 34 MW can actually reach

Work backwards from the output. To press `X` plates/min you need `2X` ingots/min, hence
`X/5` pressers rounded up; to make `2X` ingots you need `6X` gravel/min, hence
`2X/15` smelters rounded up; to make `6X` gravel you need `3X` ore/min, hence `X/10`
crushers rounded up.

Test 25 plates/min: that needs `⌈2.5⌉ = 3` pressers (15 MW), `⌈3.33⌉ = 4` smelters
(12 MW) and `⌈2.5⌉ = 3` crushers (12 MW) — **39 MW**. Over budget.

Test 20 plates/min: `2` pressers (10 MW), 40 ingots/min needs `⌈2.67⌉ = 3` smelters
(9 MW), 120 gravel/min needs `2` crushers (8 MW) — **27 MW**. Inside budget.

Nothing between 20 and 25 is reachable either, because the presser is the coarse step:
2 pressers cap you at 20 plates/min and the third one costs 5 MW you can only afford by
giving up a crusher or a smelter, which starves it. That is why the answer is exactly
20 and the search confirms it.

### Why the spare 7 MW is worthless

With 27 MW spent you can afford one more smelter (3 MW) or one more crusher (4 MW), or
both. Neither helps:

- A third crusher would draw the full 90 ore/min instead of 60, emitting 180
  gravel/min — but your 3 smelters can only swallow 135, so 45 gravel/min is simply
  wasted. Ingot output rises from 40/min to 45/min, and your 2 pressers still cannot
  take more than 40. Plates: unchanged.
- A fourth smelter raises ingot capacity to 60/min, but 2 pressers cap consumption at
  40/min regardless. Plates: unchanged.

The chain is **presser-limited**, and a third presser is unaffordable without cutting
upstream. Adding capacity anywhere except the bottleneck buys nothing. The solver
confirms six different mixes all reach exactly 20 plates/min, ranging from 27 MW to
34 MW — spending more power does not move the number.

---

## The thinking patterns this rewards

**Find the binding constraint before optimising anything.** Three constraints were
given — ore, slots, power. Ore permits 30 plates/min, slots permit far more, power
permits 20. Only one of them is real. Most of the puzzle is realising which, and the
trap is that ore is the one the scenario draws your eye to.

**Work backwards from the output, not forwards from the input.** Forward reasoning —
"I have 90 ore, so 3 crushers" — commits 12 MW before you know whether you can afford
the pressers that would justify it. Backward reasoning from a target plate rate tells
you the whole bill of materials at once and lets you binary-search the target.

**Balance ratios, then round up, then check the bill.** Continuous ratios give the
shape of the answer; integer machine counts and the round-up are where the budget is
actually consumed. Doing the rounding at the end, once, is much less error-prone than
carrying integers through every stage.

**Resist saturating a budget just because it is there.** The instinct to spend all
34 MW is exactly wrong here — this is the local-versus-global trap. A greedy
"add the cheapest machine that increases any stage's capacity" walks straight into
adding crushers and smelters that push more material into a presser that cannot take
it. Throughput is set by the narrowest stage; everything else is decoration.

**Corollary worth internalising for the real game:** when you are stuck, ask what one
extra unit of each resource would buy you. Here, one extra MW buys nothing until you
have five of them (a whole presser) *and* the upstream capacity to feed it — which is
the definition of a bottleneck that has to be relieved in a block, not incrementally.
