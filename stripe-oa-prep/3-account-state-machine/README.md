# Problem 3 — Account Lifecycle Machine

**Theme:** chronological command stream, state-transition validation, idempotency,
aggregated rejection summary with strict section formatting.
**Target time:** 60 min across 4 parts (12 / 13 / 20 / 15).

Run the reference solution with `python code.py <part>`, input on stdin.

---

## Common input grammar (all parts)

One command per line, **exactly five comma-separated fields**:

```
<ts>,<idempotency_key>,<account_id>,<command>,<arg>
```

- `ts` is `YYYY-MM-DDTHH:MM:SSZ`, fixed width, so string comparison orders it.
- `arg` is empty for lifecycle commands — the line ends with a trailing comma.
  A non-empty `arg` on a lifecycle command is ignored, not an error.
- `arg` is an amount in **cents** for `DEPOSIT` and `WITHDRAW`.
- Commands are applied strictly in **file order**. The file is the arrival order.
- Blank lines may appear anywhere and must be ignored.

### States

```
(none) --OPEN--> PENDING --VERIFY--> ACTIVE --SUSPEND--> SUSPENDED
                                       ^                     |
                                       +-----REINSTATE-------+

CLOSE:  PENDING | ACTIVE | SUSPENDED --> CLOSED     (CLOSED is terminal)
```

`DEPOSIT` and `WITHDRAW` are legal **only** in `ACTIVE`.

A command that is not legal is **rejected**: it changes nothing at all — not the
state, not the balance, and not the account's last-applied timestamp.

---

## Part 1 — Lifecycle only

Only `OPEN`, `VERIFY`, `SUSPEND`, `REINSTATE` and `CLOSE` appear. Every
`idempotency_key` is unique and timestamps are non-decreasing. Reject anything that
is not a legal transition, and any command other than `OPEN` naming an account that
does not exist.

### Output

One line per account that was ever opened, sorted by **account_id ascending (ASCII)**:

```
<account_id>,<state>
```

---

## Part 2 — Balances

`DEPOSIT` and `WITHDRAW` now appear, legal only in `ACTIVE`. A `WITHDRAW` for more
than the current balance is rejected; the balance is untouched. Keys are still
unique and timestamps still non-decreasing.

### Output

```
<account_id>,<state>,<balance_cents>
```

---

## Part 3 — Idempotency, stale commands, and a close rule

Three rules are added.

1. **Idempotency.** `idempotency_key` is unique across the *whole run*, not per
   account. If a key has already been seen — even on a different account, even with
   different fields — the command is rejected as a duplicate and nothing happens.
   A key is consumed by any command that reaches the idempotency check, whether or
   not that command is subsequently applied.
2. **Staleness.** The stream can arrive out of order. A command whose `ts` is
   **strictly earlier** than the timestamp of the last *applied* command for that
   account is rejected. Rejected commands never advance that timestamp.
3. **Close requires a zero balance.** `CLOSE` on an account with a non-zero balance
   is rejected.

Also validate the line itself: a line whose field count is not exactly 5 is
malformed, as is a `DEPOSIT` or `WITHDRAW` whose `arg` is not a string of digits
(`-100` and `3.50` are both malformed). An unrecognised command name is a bad
command.

**Rejection precedence** — a command gets exactly one reason, the first that applies
in this order:

| # | Reason code | Condition |
|---|---|---|
| 1 | `MALFORMED` | field count ≠ 5, or a money `arg` that is not all digits |
| 2 | `BAD_COMMAND` | command name not in the seven known commands |
| 3 | `DUPLICATE_KEY` | `idempotency_key` already seen |
| 4 | `UNKNOWN_ACCOUNT` | command other than `OPEN` on an account never opened |
| 5 | `STALE_TIMESTAMP` | `ts` < the account's last applied `ts` |
| 6 | `INVALID_TRANSITION` | illegal for the current state, including `OPEN` on an existing account and any command on a `CLOSED` account |
| 7 | `NONZERO_BALANCE` | `CLOSE` with a non-zero balance |
| 8 | `INSUFFICIENT_FUNDS` | `WITHDRAW` exceeding the balance |

### Output

Same format as Part 2.

---

## Part 4 — Summary report

Same processing as Part 3. The output becomes a three-section report separated by
lines containing exactly two hyphens, `--`.

**Section 1** — one line per account, sorted by account_id ascending. Balances are
now printed **in dollars with exactly two decimal places**, e.g. `5` cents prints as
`0.05` and `3500` prints as `35.00`.

```
<account_id>,<state>,<balance_dollars>
```

**Section 2** — one line per rejection reason that occurred at least once, sorted by
**count descending**, ties broken by **reason code ascending (ASCII)**:

```
<reason_code>,<count>
```

**Section 3** — always exactly one line:

```
TOTAL,<applied_count>,<rejected_count>
```

Both `--` separators are always printed, even when a section is empty. Empty input
therefore produces exactly three lines: `--`, `--`, `TOTAL,0,0`. Parts 1–3 print
nothing at all for empty input.

---

## Sample test cases

### Sample 1 — `tests/sample1.in` (Parts 1 and 2)

```
2024-01-01T00:00:00Z,k01,acc_1,OPEN,
2024-01-01T00:01:00Z,k02,acc_1,VERIFY,
2024-01-01T00:02:00Z,k03,acc_2,VERIFY,
2024-01-01T00:03:00Z,k04,acc_2,OPEN,
2024-01-01T00:04:00Z,k05,acc_1,SUSPEND,
2024-01-01T00:05:00Z,k06,acc_1,REINSTATE,
2024-01-01T00:06:00Z,k07,acc_3,OPEN,
2024-01-01T00:07:00Z,k08,acc_3,CLOSE,
2024-01-01T00:08:00Z,k09,acc_3,VERIFY,
2024-01-01T00:09:00Z,k10,acc_1,DEPOSIT,5000
2024-01-01T00:10:00Z,k11,acc_1,WITHDRAW,6000
2024-01-01T00:11:00Z,k12,acc_1,WITHDRAW,1500
2024-01-01T00:12:00Z,k13,acc_2,DEPOSIT,999
```

Expected output, Part 1:

```
acc_1,ACTIVE
acc_2,PENDING
acc_3,CLOSED
```

Expected output, Part 2:

```
acc_1,ACTIVE,3500
acc_2,PENDING,0
acc_3,CLOSED,0
```

`acc_2` is verified before it exists (ignored), then opened. `acc_3` is verified
after being closed (ignored). `acc_1` deposits 5000, is refused a 6000 withdrawal,
then withdraws 1500.

For reference, the same input at Part 4:

```
acc_1,ACTIVE,35.00
acc_2,PENDING,0.00
acc_3,CLOSED,0.00
--
INVALID_TRANSITION,2
INSUFFICIENT_FUNDS,1
UNKNOWN_ACCOUNT,1
--
TOTAL,9,4
```

### Sample 2 — `tests/sample2.in` (Parts 3 and 4)

```
2024-02-01T10:00:00Z,a1,acc_x,OPEN,
2024-02-01T10:01:00Z,a2,acc_x,VERIFY,
2024-02-01T10:02:00Z,a3,acc_x,DEPOSIT,10000
2024-02-01T10:03:00Z,a3,acc_x,DEPOSIT,10000
2024-02-01T09:59:00Z,a4,acc_x,WITHDRAW,100
2024-02-01T10:04:00Z,a5,acc_x,CLOSE,
2024-02-01T10:05:00Z,a6,acc_x,WITHDRAW,10000
2024-02-01T10:06:00Z,a7,acc_x,CLOSE,
2024-02-01T10:07:00Z,a8,acc_y,FREEZE,
2024-02-01T10:08:00Z,a9,acc_y
2024-02-01T10:09:00Z,a10,acc_z,OPEN,
2024-02-01T10:10:00Z,a11,acc_z,DEPOSIT,7
2024-02-01T10:11:00Z,a12,acc_z,SUSPEND,
```

Expected output, Part 3:

```
acc_x,CLOSED,0
acc_z,PENDING,0
```

Expected output, Part 4:

```
acc_x,CLOSED,0.00
acc_z,PENDING,0.00
--
INVALID_TRANSITION,2
BAD_COMMAND,1
DUPLICATE_KEY,1
MALFORMED,1
NONZERO_BALANCE,1
STALE_TIMESTAMP,1
--
TOTAL,6,7
```

`a3` is reused, so the second deposit is a duplicate. `a4` is dated a minute before
the account was opened. `a5` tries to close with 10000 on the books. `acc_y` never
exists: `FREEZE` is a bad command and the next line has only three fields, so no
`UNKNOWN_ACCOUNT` is ever raised for it and it never appears in section 1.

---

## When you think you are done

The gotchas — the edge cases the secret tests actually probe — and three hidden
test cases per problem live in [SPOILERS.md](SPOILERS.md). Work all four parts
against the samples first; open it only once you have something you believe is
finished, or once you are properly stuck.
