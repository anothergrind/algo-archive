# stripe oa prep

five practice problems shaped like the Stripe SWE intern online assessment:
one problem per folder, split into 4 connected parts, ~60 minutes each.

these are implementation problems, not algorithm problems. nothing here needs a data
structure fancier than a dict. the difficulty is entirely in parsing structured text,
holding state correctly across a stream of records, and matching the output format
byte for byte.

| folder | theme | what breaks people |
| --- | --- | --- |
| [`1-fee-engine/`](1-fee-engine/) | composite-key fee lookup, integer money math | half-up rounding, wildcard specificity, duplicate keys |
| [`2-fraud-stream/`](2-fraud-stream/) | charges, disputes, reversals, per-merchant thresholds | file order vs timestamp order, dangling references, divide by zero |
| [`3-account-state-machine/`](3-account-state-machine/) | lifecycle transitions, idempotency, rejection summary | rejected commands leaking state, cents→dollars formatting |
| [`4-log-percentiles/`](4-log-percentiles/) | raw log parsing, path normalisation, latency percentiles | nearest-rank vs average median, whitespace runs, `=` inside values |
| [`5-settlement-ledger/`](5-settlement-ledger/) | T+1 settlement, business days, cutoff, ACH daily limits | 17:00 boundary, weekend stacking, unsettled funds |

problem 5 is the closest to the "financial account ledger over time" format.

## how to use these

each folder has:

- `README.md` — the problem exactly as it would appear on HackerRank: the four parts,
  input and output specs, and two worked samples
- `SPOILERS.md` — the **gotchas** section naming every trap the secret tests probe,
  plus three hidden test cases with expected output
- `mine.py` — **an empty stub for your own solution**, wired to the same stdin
  and `<part>` argument convention as the reference
- `code.py` — a working reference solution for all four parts
- `tests/*.in` — the raw inputs
- `tests/*.p<N>.out` — expected output for part `N` of that input

**Do not open `SPOILERS.md` until you think you are finished.** It names the traps and
then hands you the hidden tests, so reading it early turns the exercise into
transcription. `README.md` is ordered so you can stop at the part you are on: work
part 1 to a green run before reading part 2. That gating is the whole point of the
format — it means your part 1 code has to be shaped so part 2 can extend it rather
than replace it.

Write your attempt in `mine.py`. It runs the same way the reference does:

```bash
cd stripe-oa-prep/1-fee-engine
python mine.py 1 < tests/sample1.in
python mine.py 2 < tests/sample1.in | diff - tests/sample1.p2.out
```

`check_mine.py` runs `mine.py` against every committed expectation. **Pass the part
you are on** — with no part filter it reports all four, and the parts you have not
written yet read as a wall of failures:

```bash
python stripe-oa-prep/check_mine.py fee 1   # problem substring, then part
python stripe-oa-prep/check_mine.py         # every problem, every part
```

It prints the full diff for a failing `sample*` case, since those samples are worked
in `README.md` anyway, but only the case *name* for a failing `hidden*` one — enough
to tell you which edge case broke without handing you what `SPOILERS.md` is gating.
Add `--show` when you want it to give up the answer.

Note that a `tests/<name>.p<N>.out` file exists for every input at every part, but
only the pairings named in each README are meaningful — later parts add record types
and guarantees that earlier parts are promised never to see, so running an early part
against a late part's input can legitimately crash. `check_mine.py` skips the
pairings whose expectation is one of those crashes, but scores every other one — so a
`FAIL` on a pairing your part's README does not name is not automatically your bug.

## maintenance

`check.py` re-runs every *reference* solution against every committed expectation
(`check_mine.py`, above, is the one for your own work):

```bash
python stripe-oa-prep/check.py
```

`gen_expected.py` regenerates the `.out` files after changing a `code.py` or a
`.in` file. Every expected output in every README was produced by running the
reference solution — none of it was written by hand.

```bash
python stripe-oa-prep/gen_expected.py
```
