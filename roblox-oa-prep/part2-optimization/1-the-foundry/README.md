# Puzzle 1 — The Foundry

**Time limit:** 20 minutes. Pen and paper is enough; you should not need to write code.

---

## Scenario

You are laying out a production chain. Ore comes in at one end, plates come out the
other, passing through three machine types in a fixed order:

```
ore --[Crusher]--> gravel --[Smelter]--> ingots --[Presser]--> plates
```

## Machine specifications

| Machine | Consumes | Produces | Power |
|---|---|---|---|
| Crusher | 30 ore / min | 60 gravel / min | 4 MW |
| Smelter | 45 gravel / min | 15 ingots / min | 3 MW |
| Presser | 20 ingots / min | 10 plates / min | 5 MW |

## Rules

1. A machine may run **below** its rated capacity, and its output scales linearly with
   how much input it receives. A crusher fed 15 ore/min emits 30 gravel/min.
2. A machine costs its **full** power draw and a **full** slot even when idle or
   partly loaded. There is no discount for running slow.
3. Intermediate goods are not stockpiled and cannot be sold — anything a stage produces
   that the next stage cannot consume is wasted.
4. Machine counts are whole numbers. You cannot install half a smelter.

## Constraints

- Ore arrives at **90 / min**. You cannot get more.
- You have **12 machine slots** total, in any mix.
- You have **34 MW** of power total.

## Scoring

Maximise **plates per minute**. Report the rate and the machine mix that achieves it.
If several mixes tie, prefer the one using the fewest slots.

---

## Worked example — a smaller foundry

Same machines, but ore arrives at **30 / min**, with **6 slots** and **20 MW**.

Work the chain forward from the constraint that actually binds.

- Ore is capped at 30/min, so **one crusher** absorbs the entire supply — a second
  would sit idle, burning 4 MW and a slot for nothing. That crusher emits
  **60 gravel/min**.
- 60 gravel/min needs `60 / 45 = 1.33` smelters, so **two smelters**. They are not
  fully loaded: together they can take 90 gravel/min but only get 60. At 60 gravel in,
  they emit `60 / 3 = 20 ingots/min`.
- 20 ingots/min needs `20 / 20 = 1` presser exactly. **One presser**, fully loaded,
  emits **10 plates/min**.

Total: 4 slots of 6, and `4 + 6 + 5 = 15` MW of 20. Output **10 plates/min**.

Note what the example teaches: the answer is capped by ore, and the leftover slots and
power are worth nothing. Adding a second presser is legal and free of penalty in the
score — but it produces not one extra plate, because there are no spare ingots to feed
it.

---

## The puzzle

Ore arrives at **90 / min**. You have **12 slots** and **34 MW**.

1. What is the maximum plates per minute?
2. What machine mix achieves it, using the fewest slots?
3. How much of your power budget does that mix actually use — and if there is any left
   over, why can't you spend it?

Work it out before opening [SOLUTION.md](SOLUTION.md). The solution file also contains
an exhaustive solver (`solver.py`) that you can run to check any answer you like.
