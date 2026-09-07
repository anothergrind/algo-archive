# Problem 2 — Dispute Radar

**Theme:** streaming charge/dispute processing, per-merchant thresholds, reversals,
mid-stream state change.
**Target time:** 60 min across 4 parts (10 / 15 / 17 / 18).

Run the reference solution with `python code.py <part>`, input on stdin.

---

## Common input grammar (all parts)

One record per line, fields separated by `|`. Blank lines may appear anywhere and
must be ignored.

```
THRESHOLD|<merchant_id>|<max_dispute_bps>
CHARGE|<ts>|<charge_id>|<merchant_id>|<amount_cents>
DISPUTE|<ts>|<charge_id>
REVERSE|<ts>|<charge_id>
```

- `ts` is `YYYY-MM-DDTHH:MM:SSZ`, always UTC and always the same width, so plain
  string comparison orders timestamps correctly. No date library is needed.
- `amount_cents` is a non-negative integer number of cents.
- `THRESHOLD` is configuration, not an event: it applies to the whole run no matter
  where it sits in the file. If a merchant has more than one `THRESHOLD`, the one
  **later in the file** wins. A merchant with no `THRESHOLD` uses the default
  **100 bps**.
- A merchant exists only once it has at least one accepted `CHARGE`.

**Dispute rate**, in basis points, is `floor(disputed_amount * 10000 / gross)`, where
`gross` is the merchant's total accepted charge volume and `disputed_amount` is the
total amount of its charges that are disputed *at the end of the run*. A merchant is
over its limit when its rate is **strictly greater than** its threshold.

---

## Part 1 — Merchant volume

Only `THRESHOLD` and `CHARGE` records appear. Records are guaranteed to be in
non-decreasing timestamp order.

### Output

One line per merchant, sorted by **gross descending**, ties broken by
**merchant_id ascending (ASCII)**:

```
<merchant_id>|<charge_count>|<gross>
```

---

## Part 2 — Disputes and thresholds

`DISPUTE` records now appear. A dispute marks the referenced charge as disputed and
adds its full amount to the merchant's disputed total. Records are still guaranteed
to be in non-decreasing timestamp order.

### Output

One line per merchant, same sort as Part 1:

```
<merchant_id>|<charge_count>|<gross>|<disputed_amount>|<dispute_bps>|<status>
```

`status` is `FLAGGED` when the merchant is over its limit, otherwise `OK`.

---

## Part 3 — Reversals, and time is no longer file order

Two changes:

1. `REVERSE` records appear. A reversal un-disputes the referenced charge: the charge
   stops counting toward the merchant's disputed total.
2. **The file is no longer sorted.** Records must be processed in `ts` order. Records
   sharing a timestamp are processed in the order they appear in the file.

### Output

Identical format to Part 2.

---

## Part 4 — Blocking

Process events in the Part 3 order. Immediately after applying a `DISPUTE`,
re-evaluate the merchant using only the events processed so far. If the merchant has
accepted **at least 3** charges so far *and* its dispute rate is strictly greater
than its threshold, the merchant becomes `BLOCKED` at that instant.

- Blocking is permanent. A later `REVERSE` that drops the rate does not unblock it.
- Every `CHARGE` for a blocked merchant is **rejected**: it does not join
  `charge_count` or `gross`, and its `charge_id` never becomes known, so a later
  `DISPUTE` naming it does nothing.
- A rejected charge still increments that merchant's rejected counter.

### Output

One line per merchant, same sort as Part 1 (gross descending, then merchant_id):

```
<merchant_id>|<charge_count>|<gross>|<disputed_amount>|<dispute_bps>|<status>|<rejected_count>
```

`status` is `BLOCKED` if the merchant was ever blocked; otherwise `FLAGGED` if its
final rate is over its limit; otherwise `OK`.

Then, always, exactly one line:

```
TOTAL|<merchant_count>|<blocked_count>|<rejected_count>
```

For empty input, Parts 1–3 print nothing at all; Part 4 prints `TOTAL|0|0|0`.

---

## Sample test cases

### Sample 1 — `tests/sample1.in` (Parts 1 and 2)

```
THRESHOLD|acct_zeta|150
CHARGE|2024-03-01T09:00:00Z|ch_1|acct_alpha|10000
CHARGE|2024-03-01T09:05:00Z|ch_2|acct_alpha|100
CHARGE|2024-03-01T09:07:00Z|ch_3|acct_alpha|89900
CHARGE|2024-03-01T09:10:00Z|ch_4|acct_zeta|20000
CHARGE|2024-03-01T09:15:00Z|ch_5|acct_zeta|30000
DISPUTE|2024-03-02T11:00:00Z|ch_2
DISPUTE|2024-03-02T11:05:00Z|ch_4
```

Expected output, Part 1:

```
acct_alpha|3|100000
acct_zeta|2|50000
```

Expected output, Part 2:

```
acct_alpha|3|100000|100|10|OK
acct_zeta|2|50000|20000|4000|FLAGGED
```

`acct_alpha` is 100 / 100000 = 10 bps, under the default 100. `acct_zeta` is
20000 / 50000 = 4000 bps, over its own 150.

### Sample 2 — `tests/sample2.in` (Parts 3 and 4)

```
THRESHOLD|acct_beta|500
CHARGE|2024-05-01T09:00:00Z|ch_p|acct_omega|500000
CHARGE|2024-05-01T09:30:00Z|ch_q|acct_omega|10
CHARGE|2024-05-01T10:00:00Z|ch_a|acct_beta|1000
CHARGE|2024-05-01T10:01:00Z|ch_b|acct_beta|1000
CHARGE|2024-05-01T10:02:00Z|ch_c|acct_beta|1000
REVERSE|2024-05-03T08:00:00Z|ch_a
DISPUTE|2024-05-02T08:00:00Z|ch_a
CHARGE|2024-05-04T10:00:00Z|ch_d|acct_beta|1000
DISPUTE|2024-05-05T09:00:00Z|ch_b
CHARGE|2024-05-06T10:00:00Z|ch_e|acct_beta|1000
DISPUTE|2024-05-07T09:00:00Z|ch_q
```

Expected output, Part 3:

```
acct_omega|2|500010|10|0|OK
acct_beta|5|5000|1000|2000|FLAGGED
```

Expected output, Part 4:

```
acct_omega|2|500010|10|0|OK|0
acct_beta|3|3000|1000|3333|BLOCKED|2
TOTAL|2|1|2
```

The `REVERSE` for `ch_a` sits **above** its `DISPUTE` in the file but one day
**after** it in time. Processing in file order leaves `ch_a` disputed and yields
`4000` bps for `acct_beta`; processing in timestamp order gives the correct `2000`.

In Part 4, `acct_beta` is blocked the moment `ch_a` is disputed (3 charges, 3333 bps
against a 500 limit), so `ch_d` and `ch_e` are rejected and never reach `gross`.
`acct_omega` had only 2 charges when its dispute landed, below the minimum of 3, so
it is never blocked.

---

## When you think you are done

The gotchas — the edge cases the secret tests actually probe — and three hidden
test cases per problem live in [SPOILERS.md](SPOILERS.md). Work all four parts
against the samples first; open it only once you have something you believe is
finished, or once you are properly stuck.
