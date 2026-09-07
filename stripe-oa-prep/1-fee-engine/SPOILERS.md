# Problem 1 — Composite Fee Engine — spoilers

**Do not open this until you have a solution you believe is finished.**
It names every trap the hidden tests are built from, and then gives you the
hidden tests themselves. Reading it first turns the exercise into transcription.

Back to the problem: [README.md](README.md)

---

## Gotchas — the hidden edge cases

Not stated where a first read would catch them, and what the secret tests are built
from:

1. **Banker's rounding.** Python's built-in `round()` turns `87.5` into `88` but
   `88.5` into `88`. Any float-based or `round()`-based fee is wrong on exact halves.
2. **Duplicate composite keys.** The same `(country, brand, currency)` pattern can be
   declared twice; the later declaration replaces the earlier. A solution that keeps
   a list of rules and takes the *first* match silently uses the stale rate.
3. **Zero-amount charges.** `amount = 0` still incurs the fixed fee, so `fee` exceeds
   the amount and `net` goes negative. Do not special-case or skip them.
4. **A minimum-fee floor can exceed the charge.** In Part 3 a `CAP` floor applied to a
   tiny charge yields a **negative net**. Print it as-is; do not clamp to zero.
5. **`NO_RATE` beats `NO_FX`.** A charge missing both must print `NO_RATE`.
6. **`FX|USD|...` is a decoy.** If present it must be ignored, not used as a rate.
7. **Amounts exceed 32 bits.** `amount * bps` overflows `int32` and crowds `int64`;
   free in Python, fatal in Java/C++ with `int`.
8. **Empty input** — and input holding configuration but no charges — must not crash;
   Part 4 still prints its two trailing lines.
9. **Blank lines** appear mid-file.
10. **Part 4's sort needs the tie-break.** Two countries with equal total fees must be
    ordered by country code; sorting on fee alone is non-deterministic.

---

## Hidden test cases

### Hidden 1 — empty input, Part 4 (`tests/hidden1_empty.in`)

Input: zero bytes.

```
TOTAL|0|0|0
SKIPPED|0
```

### Hidden 2 — duplicates, wildcards, zero and huge amounts, Part 2 (`tests/hidden2_dupes.in`)

```
RATE|US|visa|USD|290|30

RATE|US|visa|USD|100|0
RATE|US|*|USD|500|99
RATE|*|visa|USD|10|1
RATE|MX|visa|USD|0|7
RATE|NZ|visa|USD|0|7

CHARGE|ch_a|US|visa|USD|0
CHARGE|ch_b|US|visa|USD|99999999999
CHARGE|ch_c|US|amex|USD|1000
CHARGE|ch_d|CA|visa|USD|1000
CHARGE|ch_e|CA|amex|USD|1000
CHARGE|ch_f|NZ|visa|USD|1000
CHARGE|ch_g|MX|visa|USD|1000
```

Expected output, Part 2:

```
ch_a|0|0
ch_b|1000000000|98999999999
ch_c|149|851
ch_d|2|998
ch_e|NO_RATE
ch_f|7|993
ch_g|7|993
```

`ch_b` is 99999999999 × 100 / 10000 = 999999999.99 → 1000000000, using the **second**
`US|visa|USD` rate. The same input at Part 4:

```
US|3|100000000999|1000000149
MX|1|1000|7
NZ|1|1000|7
CA|1|1000|2
TOTAL|6|100000003999|1000000165
SKIPPED|1
```

`MX` and `NZ` both total exactly 7 in fees, so they are ordered against each other by
country code — and both sit *above* `CA`, which has a smaller total. Sorting on
country alone, or on fee alone, fails here.

### Hidden 3 — caps, FX decoys, failure precedence, Part 3 (`tests/hidden3_caps.in`)

```
RATE|FR|visa|EUR|200|0
RATE|FR|amex|EUR|200|0
FX|USD|9999999
FX|EUR|1080000
CAP|FR|150|-
CAP|FR|150|300
CAP|US|-|50
RATE|US|visa|USD|290|30
CHARGE|ch_x|FR|visa|EUR|100
CHARGE|ch_y|FR|amex|EUR|900000
CHARGE|ch_z|US|visa|USD|10000
CHARGE|ch_w|FR|visa|GBP|500
CHARGE|ch_v|IT|visa|EUR|500
```

Expected output, Part 3:

```
ch_x|108|150|-42
ch_y|972000|300|971700
ch_z|10000|50|9950
ch_w|NO_RATE
ch_v|NO_RATE
```

`ch_x` hits the 150 floor and nets negative. `ch_y`'s raw fee of 19440 is cut to the
300 ceiling from the *second* `CAP|FR`. `ch_z`'s raw fee of 320 is cut to 50.
`ch_w` has neither a rate nor an FX for GBP and must report `NO_RATE`.
The `FX|USD|9999999` line must have no effect.
