# Puzzle 2 — The Assembly Line

**Time limit:** 20 minutes. Pen and paper is enough.

---

## Scenario

Six custom orders have come in. Every order must be **painted** first, then
**packaged** — always in that order, never the reverse.

There is exactly **one** painting station and exactly **one** packaging station. Each
station handles one order at a time, start to finish, no pausing.

You choose the sequence in which orders enter the painting station. Orders then reach
the packaging station **in that same sequence** — the line does not let orders overtake
each other.

## Rules

1. Painting an order takes its listed paint time; packaging takes its listed package
   time.
2. An order can only start packaging once **it has finished painting** *and* **the
   packaging station is free**.
3. The painting station never waits: as soon as it finishes an order it starts the next
   one in your sequence.
4. Both stations start idle at minute 0.

## Scoring

Minimise the **makespan** — the clock time at which the *last* order finishes
packaging.

---

## Worked example — three orders

| Order | Paint | Package |
|---|---|---|
| A | 3 | 4 |
| B | 5 | 2 |
| C | 1 | 6 |

Try the sequence **B, A, C**:

- Paint finishes B at 5, A at 8, C at 9.
- Package B: starts at 5 (paint done), runs 2 → done at **7**.
- Package A: paint done at 8, station free at 7, so starts at 8, runs 4 → done at
  **12**.
- Package C: paint done at 9, station free at 12, so starts at 12, runs 6 → done at
  **18**.

Makespan **18** — and this is the *worst* of the six orderings.

Now try **C, A, B**:

- Paint finishes C at 1, A at 4, B at 9.
- Package C: starts at 1, runs 6 → done at **7**.
- Package A: paint done at 4, station free at 7, starts at 7, runs 4 → done at **11**.
- Package B: paint done at 9, station free at 11, starts at 11, runs 2 → done at
  **13**.

Makespan **13**, and no ordering beats it.

The difference between 13 and 18 is pure sequencing — the same total work either way.
What changed is how long the packaging station sat idle at the start, and how much work
was left for it after painting finished. `C, A, B` gets a short paint job out of the
way first so packaging starts at minute 1 instead of minute 5, and it leaves the
shortest package job for last so the tail is cheap.

---

## The puzzle

| Order | Paint | Package |
|---|---|---|
| A | 4 | 6 |
| B | 7 | 2 |
| C | 3 | 5 |
| D | 8 | 3 |
| E | 2 | 7 |
| F | 5 | 4 |

1. What is the minimum possible makespan?
2. Give a sequence that achieves it.
3. What is the **rule** you used to build that sequence? State it in one sentence, in a
   form that would work for any number of orders — not just these six.

Question 3 is the one that matters. There are 720 orderings here; there are 3.6 million
for ten orders. A method that only works by trying them all is not the answer.

Work it out before opening [SOLUTION.md](SOLUTION.md). The solution file ships
`solver.py`, which brute-forces every ordering, so you can check any claim you make.
