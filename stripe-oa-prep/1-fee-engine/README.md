# Problem 1 — Composite Fee Engine

**Theme:** transaction fee calculation, composite-key lookups with wildcard fallback,
integer money math.
**Target time:** 60 min across 4 parts (12 / 15 / 18 / 15).

Run the reference solution with `python code.py <part>`, input on stdin.

---

## Common input grammar (all parts)

One record per line, fields separated by `|`. Records may appear in **any order**;
`RATE`, `FX` and `CAP` are configuration and apply to every charge regardless of
where they sit in the file. `CHARGE` records are processed in file order.
Blank lines may appear anywhere and must be ignored.

```
RATE|<country>|<brand>|<currency>|<bps>|<fixed_minor>
FX|<currency>|<micros>
CAP|<country>|<min_fee>|<max_fee>
CHARGE|<charge_id>|<country>|<brand>|<currency>|<amount_minor>
```

- `country` is an ISO-3166 alpha-2 code, `brand` a lowercase card brand, `currency`
  an ISO-4217 code. All are case-sensitive; match them literally.
- **All money is an integer count of minor units** (cents). There are never decimal
  points in the input. Every currency has 2 decimal places.
- `bps` is basis points: 290 means 2.90%.
- `micros` is how many millionths of one USD one unit of that currency is worth.
  `1080000` means 1 EUR = 1.08 USD. USD is always exactly `1000000`.

**Rounding rule, used everywhere:** whenever a division is required, round the exact
mathematical result **half away from zero** to a whole minor unit — `x.5` always
rounds up to `x+1`, never to even. All quantities in this problem are non-negative
before rounding, so integer `(num * 2 + den) // (den * 2)` is exact.

Record types not listed for a part will not appear in that part's input.

---

## Part 1 — Exact fee lookup

Only `RATE` and `CHARGE` records appear. Guarantees: no `*` appears in any field,
no two `RATE` records share a key, and every charge has exactly one matching rate.

The rate key is the composite `(country, brand, currency)`. For each charge:

```
variable = round_half_up(amount_minor * bps / 10000)
fee      = variable + fixed_minor
net      = amount_minor - fee
```

### Output

One line per `CHARGE`, in input order:

```
<charge_id>|<fee>|<net>
```

---

## Part 2 — Wildcards, overrides, and misses

Now `RATE` records may use `*` in any of the three key fields, and the same key
pattern may appear more than once.

1. A rate matches a charge if each of its three fields is either equal to the
   charge's value or `*`.
2. When several rates match, the **most specific** wins. Specificity is compared
   field by field in the priority order **country, then brand, then currency**: a
   candidate with a literal country beats every candidate with `*` for country, no
   matter what the other two fields hold; ties are then broken on brand, then on
   currency.
3. If two `RATE` records have the **identical** key pattern, the one appearing
   **later in the file wins** — it replaces the earlier one entirely.
4. If no rate matches, the charge is a miss.

### Output

Same as Part 1, except a miss prints:

```
<charge_id>|NO_RATE
```

---

## Part 3 — Multi-currency and fee bounds

`FX` and `CAP` records now appear.

1. Look the rate up on the charge's **original** currency, exactly as in Part 2.
2. Convert the amount to USD cents:
   `usd = round_half_up(amount_minor * micros / 1000000)`. A USD charge converts to
   itself; an `FX|USD|...` record, if present, is ignored.
3. Compute the fee from the **converted** USD amount, using the rule from Part 1.
4. If a `CAP` record exists for the charge's country, clamp the fee into
   `[min_fee, max_fee]`. Either bound may be the literal `-`, meaning unbounded on
   that side. If two `CAP` records name the same country, the later one wins.
   `CAP` bounds are USD cents.
5. `net = usd - fee`.

**Failure precedence:** check the rate first. A charge with no matching rate is
`NO_RATE` even when its currency also has no `FX` record.

### Output

One line per `CHARGE`, in input order:

```
<charge_id>|<usd_amount>|<fee>|<net>
```

Misses print `<charge_id>|NO_RATE`, or `<charge_id>|NO_FX` when the rate matched but
the currency has no `FX` record.

---

## Part 4 — Per-country settlement summary

Same processing rules as Part 3, but the per-charge lines are replaced by an
aggregate report. A charge that produced `NO_RATE` or `NO_FX` contributes to
nothing except the skip counter.

### Output

One line per country that settled at least one charge, sorted by **total fee
descending**, ties broken by **country code ascending (ASCII)**:

```
<country>|<charge_count>|<total_usd_amount>|<total_fee>
```

Then, always, exactly these two lines:

```
TOTAL|<charge_count>|<total_usd_amount>|<total_fee>
SKIPPED|<n>
```

For empty input, Parts 1–3 print nothing at all (zero bytes); Part 4 still prints
`TOTAL|0|0|0` then `SKIPPED|0`.

---

## Sample test cases

### Sample 1 — `tests/sample1.in` (Parts 1 and 2)

```
RATE|US|visa|USD|290|30
RATE|US|amex|USD|350|0
RATE|GB|visa|GBP|140|20
CHARGE|ch_001|US|visa|USD|10000
CHARGE|ch_002|US|amex|USD|2500
CHARGE|ch_003|GB|visa|GBP|999
```

Expected output — identical for Part 1 and Part 2:

```
ch_001|320|9680
ch_002|88|2412
ch_003|34|965
```

`ch_002` is the rounding tripwire: 2500 × 350 / 10000 = **87.5** exactly, which must
round up to 88. `ch_003` is 999 × 140 / 10000 = 13.986 → 14, plus the fixed 20.

### Sample 2 — `tests/sample2.in` (Parts 3 and 4)

```
RATE|*|*|*|350|25
RATE|US|visa|USD|290|30
RATE|DE|*|EUR|175|25
FX|EUR|1080000
FX|GBP|1270000
CAP|DE|100|500
CHARGE|ch_101|US|visa|USD|10000
CHARGE|ch_102|DE|mastercard|EUR|5000
CHARGE|ch_103|GB|visa|GBP|2000
CHARGE|ch_104|JP|jcb|JPY|30000
```

Expected output, Part 3:

```
ch_101|10000|320|9680
ch_102|5400|120|5280
ch_103|2540|114|2426
ch_104|NO_FX
```

Expected output, Part 4:

```
US|1|10000|320
DE|1|5400|120
GB|1|2540|114
TOTAL|3|17940|554
SKIPPED|1
```

---

## When you think you are done

The gotchas — the edge cases the secret tests actually probe — and three hidden
test cases per problem live in [SPOILERS.md](SPOILERS.md). Work all four parts
against the samples first; open it only once you have something you believe is
finished, or once you are properly stuck.
