# Problem 5 — Settlement Ledger

**Theme:** balance ledger, transfer validation, T+1 settlement with business-day and
cutoff-time rules, per-day ACH funding limits.
**Target time:** 60 min across 4 parts (10 / 12 / 22 / 16).

This is the closest of the five to a real "financial account ledger over time" OA.

Run the reference solution with `python code.py <part>`, input on stdin.

---

## Common input grammar (all parts)

One record per line, fields separated by `|`. Blank lines may appear anywhere and
must be ignored.

```
OPEN|<account_id>|<opening_balance_cents>
LIMIT|<account_id>|<daily_limit_cents>
XFER|<txn_id>|<ts>|<from_account>|<to_account>|<amount_cents>
```

- `OPEN` and `LIMIT` are configuration and apply to the whole run wherever they sit
  in the file. A second `OPEN` for an account is ignored — **the first `OPEN` wins**,
  an account cannot be reopened. A second `LIMIT` replaces the first — **the last
  `LIMIT` wins**.
- `ts` is `YYYY-MM-DDTHH:MM` — no seconds, no timezone suffix.
- `XFER` records are processed in **file order**. From Part 3 onward they are
  guaranteed to be in non-decreasing timestamp order.
- All amounts are non-negative integers in cents.

### Rejection reasons

A transfer gets exactly one reason, the first that applies:

| # | Reason | Condition |
|---|---|---|
| 1 | `DUPLICATE_TXN` | `txn_id` already seen, applied or not |
| 2 | `UNKNOWN_ACCOUNT` | `from` or `to` was never opened |
| 3 | `SAME_ACCOUNT` | `from` equals `to` |
| 4 | `LIMIT_EXCEEDED` | Part 4 only, see below |
| 5 | `INSUFFICIENT_FUNDS` | amount exceeds the sender's available balance |

A rejected transfer changes nothing: no balance moves, no settlement is scheduled,
and no daily allowance is consumed.

---

## Part 1 — Immediate ledger

Transfers settle instantly: debit the sender, credit the receiver in the same step.
Reject per the table above (`LIMIT_EXCEEDED` cannot occur).

### Output

One line per opened account, sorted by **account_id ascending (ASCII)**:

```
<account_id>|<balance_cents>
```

---

## Part 2 — Rejection log

Same processing as Part 1, sectioned output. Section headers are always printed even
when the section below them is empty.

```
#BALANCES
<account_id>|<balance_cents>
...
#REJECTED
<txn_id>|<reason>
...
#TOTALS
TOTAL|<applied_count>|<rejected_count>
```

Rejections are listed in **input order**, not sorted.

---

## Part 3 — Delayed settlement

The debit is still immediate, but the **credit lands on a settlement date**.

Cutoff is **17:00**. Weekends (Saturday and Sunday) are not business days. Public
holidays are not modelled — every weekday is a business day.

For a transfer at timestamp `ts` on calendar date `d` at time `t`:

```
submit_day = d                       if d is a business day and t < 17:00
             next business day > d   otherwise

settlement_date = next business day > submit_day
```

So a Friday 09:00 transfer settles Monday; a Friday 17:00 transfer settles Tuesday;
and a Saturday transfer, at any time, also settles Tuesday.

**Available balance.** The `INSUFFICIENT_FUNDS` check uses what the sender can
actually spend at that moment: its opening balance, minus every transfer it has
already sent, plus only those incoming credits whose settlement date is **on or
before the transfer's calendar date**. Money that has not settled yet cannot be
spent.

**Final balances** in `#BALANCES` are reported after every scheduled credit has
settled, including credits whose settlement date is past the end of the stream.

### Output

```
#BALANCES
<account_id>|<balance_cents>
...
#REJECTED
<txn_id>|<reason>
...
#SETTLEMENTS
<YYYY-MM-DD>|<account_id>|<credited_cents>
...
#TOTALS
TOTAL|<applied_count>|<rejected_count>
```

`#SETTLEMENTS` has one line per `(settlement_date, receiving account)` pair that has
at least one credit, with the amounts summed, sorted by **date ascending** then
**account_id ascending**.

---

## Part 4 — ACH funding limits

Each account has a daily outbound limit: the total it may **send** across all
transfers stamped with the same calendar date. `LIMIT` sets it per account; an
account with no `LIMIT` record uses the default **500000** cents.

The limit is keyed on the transfer's own calendar date — the date in `ts`, not the
settlement date — and a Saturday is its own day like any other. A transfer that
would take the sender's total for that date **above** the limit is rejected with
`LIMIT_EXCEEDED` and consumes none of the allowance. Exactly hitting the limit is
allowed.

### Output

As Part 3, with a fourth section inserted before `#TOTALS`:

```
#DAILY
<YYYY-MM-DD>|<account_id>|<outbound_cents>
```

One line per `(date, sending account)` pair with at least one **applied** transfer,
sorted by **date ascending** then **account_id ascending**.

Empty input produces exactly six lines: the five headers and `TOTAL|0|0`. Part 1
prints nothing at all for empty input.

---

## Sample test cases

### Sample 1 — `tests/sample1.in` (Parts 1 and 2)

```
OPEN|acct_a|100000
OPEN|acct_b|0
OPEN|acct_c|5000
XFER|t1|2024-09-02T09:00|acct_a|acct_b|25000
XFER|t2|2024-09-02T10:00|acct_b|acct_c|30000
XFER|t3|2024-09-02T11:00|acct_a|acct_z|1000
XFER|t4|2024-09-02T12:00|acct_c|acct_c|100
XFER|t5|2024-09-02T13:00|acct_a|acct_c|25000
XFER|t1|2024-09-02T14:00|acct_a|acct_c|1
```

Expected output, Part 1:

```
acct_a|50000
acct_b|25000
acct_c|30000
```

Expected output, Part 2:

```
#BALANCES
acct_a|50000
acct_b|25000
acct_c|30000
#REJECTED
t2|INSUFFICIENT_FUNDS
t3|UNKNOWN_ACCOUNT
t4|SAME_ACCOUNT
t1|DUPLICATE_TXN
#TOTALS
TOTAL|2|4
```

### Sample 2 — `tests/sample2.in` (Parts 3 and 4)

2024-09-06 is a Friday; 09-07 and 09-08 are the weekend; 09-09 is Monday.

```
OPEN|acct_a|1000000
OPEN|acct_b|0
LIMIT|acct_a|300000
XFER|t1|2024-09-06T09:00|acct_a|acct_b|100000
XFER|t2|2024-09-06T17:00|acct_a|acct_b|100000
XFER|t3|2024-09-06T18:00|acct_a|acct_b|150000
XFER|t4|2024-09-07T11:00|acct_a|acct_b|100000
XFER|t5|2024-09-10T09:00|acct_b|acct_a|150000
```

Expected output, Part 3:

```
#BALANCES
acct_a|700000
acct_b|300000
#REJECTED
#SETTLEMENTS
2024-09-09|acct_b|100000
2024-09-10|acct_b|350000
2024-09-11|acct_a|150000
#TOTALS
TOTAL|5|0
```

Expected output, Part 4:

```
#BALANCES
acct_a|850000
acct_b|150000
#REJECTED
t3|LIMIT_EXCEEDED
#SETTLEMENTS
2024-09-09|acct_b|100000
2024-09-10|acct_b|200000
2024-09-11|acct_a|150000
#DAILY
2024-09-06|acct_a|200000
2024-09-07|acct_a|100000
2024-09-10|acct_b|150000
#TOTALS
TOTAL|4|1
```

`t1` beats the Friday cutoff and settles Monday. `t2` lands exactly on 17:00 and `t3`
after it, so both submit Monday and settle Tuesday; `t4` is a Saturday and does the
same. `t5` on Tuesday can spend 300000 because those three credits have settled by
then. In Part 4, `t3` would have pushed `acct_a`'s Friday outbound to 350000 against
its 300000 limit, so it never happens at all — which is why the Part 3 and Part 4
balances differ.

---

## When you think you are done

The gotchas — the edge cases the secret tests actually probe — and three hidden
test cases per problem live in [SPOILERS.md](SPOILERS.md). Work all four parts
against the samples first; open it only once you have something you believe is
finished, or once you are properly stuck.
