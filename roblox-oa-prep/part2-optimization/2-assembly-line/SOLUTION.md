# Puzzle 2 — The Assembly Line — solution

**Only open this after you have committed to an answer.** Back to the puzzle:
[README.md](README.md)

---

## Answer

1. **Minimum makespan: 31 minutes.**
2. **`E, C, A, F, D, B`** achieves it. (47 of the 720 orderings tie at 31; the worst is
   42. Any sequence reaching 31 is a correct answer to question 2.)
3. The rule is **Johnson's rule**:

   > Split the orders into those whose paint time is **less than** their package time
   > and those where it is not. Run the first group in **increasing paint time**, then
   > the second group in **decreasing package time**.

Proved by exhaustive search — run `python solver.py`.

---

## Reasoning

### Why sequencing matters at all

The total work is fixed: 29 minutes of painting and 27 of packaging no matter what you
choose. The only thing your sequence controls is **idle time on the packaging station**
— the gap before it starts, plus any gap where it has finished an order and the next
one is still in the paint booth.

So minimising the makespan is exactly minimising packaging idle time. That reframing is
the whole puzzle.

### What the rule is doing

Two competing pressures:

- **At the start**, packaging is idle until the first order finishes painting. So you
  want a *short paint time* first, to open the second station as early as possible.
- **At the end**, painting has finished and packaging still has its last order to run.
  So you want a *short package time* last, to keep the tail cheap.

Johnson's rule serves both. Orders where paint < package are "front-loaded" — they open
the pipeline cheaply and give packaging plenty to chew on — so they go first, shortest
paint first. Orders where package ≤ paint are "back-loaded" — they keep painting busy
while packaging drains — so they go last, and among them you want the smallest package
time at the very end, hence decreasing package time.

### Applying it here

| Order | Paint | Package | Group |
|---|---|---|---|
| E | 2 | 7 | paint < package |
| C | 3 | 5 | paint < package |
| A | 4 | 6 | paint < package |
| F | 5 | 4 | paint ≥ package |
| D | 8 | 3 | paint ≥ package |
| B | 7 | 2 | paint ≥ package |

First group by increasing paint: `E(2), C(3), A(4)`.
Second group by decreasing package: `F(4), D(3), B(2)`.
Sequence: **`E, C, A, F, D, B`**.

Timeline:

| Order | Paint done | Package starts | Package done |
|---|---|---|---|
| E | 2 | 2 | 9 |
| C | 5 | 9 | 14 |
| A | 9 | 14 | 20 |
| F | 14 | 20 | 24 |
| D | 22 | 24 | 27 |
| B | 29 | 29 | 31 |

Packaging idles only for the first 2 minutes and again for 2 minutes before B. Painting
finishes at 29 and the last package takes 2 more — **31**.

### Why the obvious greedies fail

- **Shortest total time first** (sort on paint + package): 32 to 35 depending on how
  you break ties. It ignores which station the time sits on, which is the only thing
  that matters.
- **Shortest paint first** across the board (`E, C, A, F, B, D`): 32. Close, because it
  gets the front right — but it ends on D's 3-minute package instead of B's 2-minute
  one, so the tail costs a minute more.
- **Longest paint first** (`D, B, F, A, C, E`): 42, the worst ordering there is.

Being one minute off is the characteristic failure here: the front-loading half of the
rule is intuitive and most people find it; the back-loading half, sorting *descending*
on the *other* station, is the part that gets missed.

One caution: on this particular instance, "longest package time first" also happens to
reach 31. That is a coincidence of these six jobs, not a rule — it fails in general.
Matching the optimum on one instance is not evidence that a criterion is correct, which
is exactly why question 3 asked for a rule that works for any number of orders.

---

## The thinking patterns this rewards

**Reframe the objective into the quantity you actually control.** "Minimise makespan"
is hard to reason about directly. "Minimise idle time on the downstream station" is
almost mechanical. Roblox's factory game rewards this constantly — throughput problems
usually turn into *starvation* problems once you look at the right station.

**Look for the exchange argument.** The reason Johnson's rule is provably optimal is
that if any adjacent pair violates it, swapping them never increases the makespan.
You do not need to reconstruct the proof under time pressure, but the *instinct* — "can
I improve this by swapping two neighbours?" — is what turns a guess into a rule, and it
is also a fast way to check your own answer.

**Greedy is right here, but only the correct greedy.** This is the opposite lesson to
Puzzle 1. There, greedy local improvement actively misled you and you needed global
constraint analysis. Here a greedy ordering is provably optimal — but three plausible
greedy criteria give 32–35 and only one gives 31. The skill is not "be greedy" or
"don't be greedy"; it is recognising which structure you are in.

**Asymmetry is a signal.** When two stations have different time profiles per job, the
optimal policy is almost never symmetric. A rule that sorts both groups the same
direction should feel suspicious.

**Bound your answer before you trust it.** Painting totals 29 minutes and the shortest
package time is 2, so no schedule can finish before 31. Once you compute 31 you are
*done* — you have matched the lower bound and do not need to search further. Finding a
cheap lower bound is often faster than proving your construction optimal, and it is the
single most useful habit for timed optimisation questions.
