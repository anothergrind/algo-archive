# Problem 3 — Account Lifecycle Machine — spoilers

**Do not open this until you have a solution you believe is finished.**
It names every trap the hidden tests are built from, and then gives you the
hidden tests themselves. Reading it first turns the exercise into transcription.

Back to the problem: [README.md](README.md)

---

## Gotchas — the hidden edge cases

1. **Rejected commands must not advance the account's last-applied timestamp.** If
   you stamp `last_ts` before validating, one malformed line poisons every later
   command as `STALE_TIMESTAMP`.
2. **Idempotency keys are global, not per account.** The same key on a different
   account is still a duplicate.
3. **Trailing empty field.** `...,OPEN,` splits into five fields, the last empty.
   `str.split(",")` is right; anything that drops trailing empties reports every
   lifecycle line as `MALFORMED`.
4. **Cent-to-dollar formatting.** `5` cents is `0.05`, not `0.5`; `100` is `1.00`,
   not `1.0`. Divide by 100 in floats and `0.05` eventually prints as `0.049999`.
5. **`WITHDRAW` of exactly the balance succeeds**; only *more than* the balance is
   `INSUFFICIENT_FUNDS`. A `>=` here is wrong.
6. **`DEPOSIT,0` is valid** and counts as applied. `DEPOSIT,-100` is `MALFORMED`,
   because the amount must be digits only.
7. **Precedence between `BAD_COMMAND` and `UNKNOWN_ACCOUNT`.** An unknown command on
   an account that was never opened is `BAD_COMMAND`, and the account must not be
   conjured into existence by it.
8. **Both `--` lines print even when the reject section is empty**, so a clean run
   ends with two adjacent separators.
9. **An account that is only ever the target of rejected commands never appears** in
   section 1.
10. **Section 2's tie-break is load-bearing** — several reasons commonly land on the
    same count.

---

## Hidden test cases

### Hidden 1 — empty input, Part 4 (`tests/hidden1_empty.in`)

Input: zero bytes.

```
--
--
TOTAL,0,0
```

### Hidden 2 — formatting, malformed amounts, global keys, Part 4 (`tests/hidden2_format.in`)

```
2024-03-01T00:00:00Z,z1,acc_a,OPEN,IGNORED
2024-03-01T00:00:01Z,z2,acc_a,VERIFY,
2024-03-01T00:00:02Z,z3,acc_a,DEPOSIT,5
2024-03-01T00:00:03Z,z4,acc_a,DEPOSIT,0
2024-03-01T00:00:04Z,z5,acc_a,DEPOSIT,-100
2024-03-01T00:00:05Z,z6,acc_a,WITHDRAW,3.50
2024-03-01T00:00:00Z,z7,acc_a,DEPOSIT,100000
2024-03-01T00:00:06Z,z3,acc_b,OPEN,
2024-03-01T00:00:07Z,z8,acc_b,OPEN,
2024-03-01T00:00:08Z,z9,acc_ghost,FREEZE,
```

Expected output, Part 4:

```
acc_a,ACTIVE,0.05
acc_b,PENDING,0.00
--
MALFORMED,2
BAD_COMMAND,1
DUPLICATE_KEY,1
STALE_TIMESTAMP,1
--
TOTAL,5,5
```

`z1` carries a stray `arg` and must still be applied. `z5` and `z6` are malformed and
leave `last_ts` at `00:00:03`, so `z7` at `00:00:00` is stale — if the malformed
lines had advanced the clock the reason would be wrong. `z3` is reused on a different
account. The final balance of 5 cents must print as `0.05`. `z9` is a bad command, so
`acc_ghost` is never created and never appears in section 1 — resolving it as
`UNKNOWN_ACCOUNT` instead gets both the reason and the account list wrong.

### Hidden 3 — full transition cycle, exact withdrawal, Parts 3 and 4 (`tests/hidden3_cycle.in`)

```
2024-04-01T00:00:00Z,q1,acc_m,OPEN,
2024-04-01T00:00:01Z,q2,acc_m,OPEN,
2024-04-01T00:00:02Z,q3,acc_m,VERIFY,
2024-04-01T00:00:03Z,q4,acc_m,DEPOSIT,250000
2024-04-01T00:00:04Z,q5,acc_m,SUSPEND,
2024-04-01T00:00:05Z,q6,acc_m,WITHDRAW,1
2024-04-01T00:00:06Z,q7,acc_m,CLOSE,
2024-04-01T00:00:07Z,q8,acc_m,REINSTATE,
2024-04-01T00:00:08Z,q9,acc_m,WITHDRAW,250000
2024-04-01T00:00:09Z,q10,acc_m,WITHDRAW,1
2024-04-01T00:00:10Z,q11,acc_m,CLOSE,
2024-04-01T00:00:11Z,q12,acc_m,CLOSE,
```

Expected output, Part 3:

```
acc_m,CLOSED,0
```

Expected output, Part 4:

```
acc_m,CLOSED,0.00
--
INVALID_TRANSITION,3
INSUFFICIENT_FUNDS,1
NONZERO_BALANCE,1
--
TOTAL,7,5
```

`q9` withdraws the balance exactly and must succeed; `q10` then fails against a zero
balance. `q7` is blocked by the close rule, `q12` by `CLOSED` being terminal.
