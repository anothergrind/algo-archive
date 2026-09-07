# Problem 5 — Settlement Ledger — spoilers

**Do not open this until you have a solution you believe is finished.**
It names every trap the hidden tests are built from, and then gives you the
hidden tests themselves. Reading it first turns the exercise into transcription.

Back to the problem: [README.md](README.md)

---

## Gotchas — the hidden edge cases

1. **The cutoff is `>=`, not `>`.** A transfer at exactly 17:00 is *after* the
   cutoff. Comparing `t <= "17:00"` shifts one whole business day.
2. **A weekend transfer submits on Monday and settles Tuesday** — two rules stack.
   Treating "weekend" as merely "roll the settlement date forward" gives Monday.
3. **Unsettled credits cannot be spent.** An account that received money yesterday
   evening may still be `INSUFFICIENT_FUNDS` today.
4. **`OPEN` is first-wins but `LIMIT` is last-wins.** They are deliberately opposite.
5. **A duplicate `txn_id` is rejected even if the original was itself rejected** — the
   id is consumed by any transfer that reaches the duplicate check.
6. **Zero-amount transfers are valid.** They apply, they produce a `#SETTLEMENTS` row
   of `0`, and they produce a `#DAILY` row of `0`. Do not filter them out.
7. **`LIMIT_EXCEEDED` outranks `INSUFFICIENT_FUNDS`**, so a broke account over its
   limit reports the limit.
8. **A rejected transfer consumes no daily allowance.** Deducting first and rolling
   back is where this usually breaks.
9. **Settlement dates cross month and year boundaries**, and the sort on those dates
   is by ISO string, so it must be zero-padded.
10. **All section headers print even when empty**, including `#REJECTED` on a clean
    run, which puts two headers on consecutive lines.
11. **Every opened account appears in `#BALANCES`**, even one that never moved money.

---

## Hidden test cases

### Hidden 1 — empty input, Part 4 (`tests/hidden1_empty.in`)

Input: zero bytes.

```
#BALANCES
#REJECTED
#SETTLEMENTS
#DAILY
#TOTALS
TOTAL|0|0
```

### Hidden 2 — config precedence, zero amounts, unsettled funds, Part 4 (`tests/hidden2_config.in`)

2024-09-02 is a Monday.

```
OPEN|w|100000
OPEN|w|999999999
OPEN|x|0
LIMIT|w|100
LIMIT|w|1000
XFER|d1|2024-09-02T09:00|w|x|1000
XFER|d2|2024-09-02T09:01|w|x|1
XFER|d3|2024-09-02T09:02|x|w|0
XFER|d4|2024-09-02T09:03|x|w|500
XFER|d5|2024-09-03T09:00|x|w|500
XFER|d2|2024-09-03T09:01|w|x|1
XFER|d6|2024-09-03T09:02|x|w|999999
```

Expected output, Part 4:

```
#BALANCES
w|99500
x|500
#REJECTED
d2|LIMIT_EXCEEDED
d4|INSUFFICIENT_FUNDS
d2|DUPLICATE_TXN
d6|LIMIT_EXCEEDED
#SETTLEMENTS
2024-09-03|w|0
2024-09-03|x|1000
2024-09-04|w|500
#DAILY
2024-09-02|w|1000
2024-09-02|x|0
2024-09-03|x|500
#TOTALS
TOTAL|3|4
```

`w` opens at 100000, not 999999999, and its limit is 1000, not 100. `d1` hits the
limit exactly and is allowed; `d2`, for one cent, is not. `d3` moves zero and still
produces a `0` row in both `#SETTLEMENTS` and `#DAILY`. `d4` fails because `x`'s 1000
does not settle until 09-03, and the very same transfer succeeds as `d5` a day later.

The last two lines are the precedence tests. `d2` is reused — and is a duplicate even
though the original `d2` was itself rejected, so the same id appears twice in
`#REJECTED` with two different reasons. `d6` sends 999999 from an account holding 500;
because its default 500000 limit is checked first, the answer is `LIMIT_EXCEEDED`,
not `INSUFFICIENT_FUNDS`. Note also that `w`'s `#DAILY` row for 09-02 reads `1000`,
not `1001` — the rejected `d2` consumed none of the allowance.

### Hidden 3 — cutoff, weekends, year boundary, Part 3 (`tests/hidden3_calendar.in`)

2024-12-27 is a Friday; 12-28 and 12-29 are the weekend; 12-30 Monday, 12-31 Tuesday,
2025-01-01 Wednesday, 01-02 Thursday.

```
OPEN|src|10000000
OPEN|dst|0
OPEN|idle|42
XFER|b1|2024-12-27T16:59|src|dst|100
XFER|b2|2024-12-27T17:00|src|dst|200
XFER|b3|2024-12-28T08:00|src|dst|300
XFER|b4|2024-12-29T23:59|src|dst|400
XFER|b5|2024-12-31T18:00|src|dst|500
XFER|b6|2025-01-01T09:00|src|dst|600
```

Expected output, Part 3:

```
#BALANCES
dst|2100
idle|42
src|9997900
#REJECTED
#SETTLEMENTS
2024-12-30|dst|100
2024-12-31|dst|900
2025-01-02|dst|1100
#TOTALS
TOTAL|6|0
```

One minute separates `b1` (settles 12-30) from `b2` (settles 12-31). `b3` and `b4`
are weekend submissions and join `b2`. `b5` is after Tuesday's cutoff, so it submits
on New Year's Day — a weekday, and therefore a business day here — and settles
01-02, alongside `b6` which was submitted that same Wednesday morning. `#REJECTED` is
empty but its header still prints, and `idle` — opened but never touched — still owes
a `#BALANCES` row.
