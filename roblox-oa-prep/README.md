# roblox oa prep

mock material for the Roblox SWE intern online assessment, in its three reported
sections. built to be sat under time, not read.

> **Caveat, stated plainly:** this is modelled on a general understanding of the Roblox
> OA format, not on a firsthand sitting. The section split (DSA → optimisation game →
> written) and the difficulty band are the assumptions everything else rests on. If the
> real assessment differs, the coding problems still stand on their own as practice —
> but the shape may not match.

Note that this directory deliberately breaks the conventions of
[`../stripe-oa-prep/`](../stripe-oa-prep/). That set is implementation-heavy with gated
multi-part problems and strict sectioned output, because that is the Stripe format.
This one is standalone LeetCode-style problems where the difficulty is algorithmic and
the output is a number or a short list. The two directories are inconsistent on purpose.

---

## Part 1 — Coding (60 min for all five)

| # | problem | theme | difficulty |
|---|---|---|---|
| 1 | [Best Build Block](part1-coding/1-build-grid-blocks/) | 2D matrix, prefix sums | Medium |
| 2 | [Longest Play Session](part1-coding/2-longest-session/) | sliding window | Medium |
| 3 | [Match and Collapse](part1-coding/3-match-collapse/) | grid simulation | Medium-Hard |
| 4 | [Tower Builds](part1-coding/4-tower-builds/) | counting DP, modular | Medium |
| 5 | [Username Aliases](part1-coding/5-username-aliases/) | string transform, output ordering | Easy-Medium |

Each problem folder holds:

- `README.md` — statement, constraints, two worked examples. **This is all you read
  while solving.**
- `SOLUTION.md` — approach, complexity, reference solution, and three hidden
  edge-case tests. Open only when you have an answer.
- `code.py` — the reference solution, reading stdin
- `brute.py` — a deliberately naive oracle, written a different way on purpose
- `fuzz_gen.py` — random input generator for differential testing
- `tests/` — the sample and hidden inputs with their expected output

## Part 2 — Optimisation (20 min per puzzle)

| # | puzzle | shape |
|---|---|---|
| 1 | [The Foundry](part2-optimization/1-the-foundry/) | production chain, find the binding constraint |
| 2 | [The Assembly Line](part2-optimization/2-assembly-line/) | two-station scheduling, find the rule |

Pen and paper. Each ships a `solver.py` that exhaustively proves the stated optimum, so
you can check any answer you want to make. `SOLUTION.md` also covers the *thinking
patterns* each puzzle rewards — the two puzzles teach deliberately opposite lessons
about when greedy reasoning works.

## Part 3 — Written (25 min for all six)

[part3-written/](part3-written/) — six short-response questions, then a rubric per
question with a worked weak answer and why it fails. Draft cold before opening
`RUBRICS.md`.

---

## Verification

Everything in Part 1 is checked three ways, and no expected output anywhere was typed
by hand.

```bash
python roblox-oa-prep/fuzz.py      # differential-test each solution vs its naive oracle
python roblox-oa-prep/check.py     # solutions still reproduce every committed .out
python roblox-oa-prep/gen_expected.py   # regenerate the .out files after a change
```

`fuzz.py` is the one that matters. `check.py` only proves the expected outputs are
reproducible — it compares a solution against itself. `fuzz.py` compares each reference
solution against an independently written brute force over thousands of random inputs,
which is what actually catches a wrong sliding-window boundary or an off-by-one in a
tie-break.

Part 2's answers are proved the same way, by exhaustive search:

```bash
python roblox-oa-prep/part2-optimization/1-the-foundry/solver.py
python roblox-oa-prep/part2-optimization/2-assembly-line/solver.py
```

---

## Running a full mock

Set a timer and do it in order, without opening any `SOLUTION.md` or `RUBRICS.md`:

1. **60 min** — all five Part 1 problems. Budget roughly 12 / 10 / 18 / 12 / 8.
2. **20 min** — Foundry.
3. **20 min** — Assembly Line.
4. **25 min** — all six written questions.

That is a little over two hours, which is longer than the real thing; the sections are
sat separately. Doing Part 1 alone under 60 minutes is the highest-value single rep.
