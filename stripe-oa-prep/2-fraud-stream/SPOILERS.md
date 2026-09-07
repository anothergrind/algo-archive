# Problem 2 — Dispute Radar — spoilers

**Do not open this until you have a solution you believe is finished.**
It names every trap the hidden tests are built from, and then gives you the
hidden tests themselves. Reading it first turns the exercise into transcription.

Back to the problem: [README.md](README.md)

---

## Gotchas — the hidden edge cases

1. **Disputes referencing an unknown `charge_id`.** Not mentioned anywhere in the
   statement. They must be silently ignored, and must not create a phantom merchant.
2. **A charge disputed twice.** The second `DISPUTE` on an already-disputed charge
   must not double-count the amount.
3. **Division by zero.** A merchant whose every charge is `0` has `gross == 0`. Its
   dispute rate is `0` and its status is `OK` — do not crash and do not flag it.
4. **Duplicate `charge_id`.** The first accepted charge with an id wins; a later
   record reusing that id is ignored entirely, including its amount and its merchant.
5. **Reversing something that was never disputed** (or was already reversed) is a
   no-op, not an error, and must not drive `disputed_amount` negative.
6. **Strictly greater, not greater-or-equal.** A rate exactly equal to the threshold
   is `OK`. Off-by-one here fails silently on most inputs.
7. **The sort tie-break is load-bearing.** Two merchants can end with identical gross;
   without the `merchant_id` tie-break the output order is undefined.
8. **`THRESHOLD` can appear after the charges it governs**, and can appear twice for
   the same merchant. Do not process it as a positional event.
9. **In Part 4 the block check runs after each dispute, not once at the end.** A
   merchant whose *final* rate is under the limit can still be blocked mid-stream by a
   dispute that was later reversed.
10. **Same-timestamp events are separated only by file order.** Part 3's sort must be
    stable; a `DISPUTE` and its `REVERSE` can share a timestamp to the second.
11. **Empty input** must not crash; Part 4 still prints its `TOTAL` line.

---

## Hidden test cases

### Hidden 1 — empty input, Part 4 (`tests/hidden1_empty.in`)

Input: zero bytes.

```
TOTAL|0|0|0
```

### Hidden 2 — bad references, duplicates, zero gross, same-timestamp order, Parts 2 and 3 (`tests/hidden2_refs.in`)

```
THRESHOLD|m_dup|999
THRESHOLD|m_dup|0

CHARGE|2024-01-01T00:00:00Z|ch_1|m_zero|0
CHARGE|2024-01-01T00:00:01Z|ch_2|m_zero|0
DISPUTE|2024-01-01T00:00:02Z|ch_1
CHARGE|2024-01-01T00:00:03Z|ch_3|m_dup|1000
CHARGE|2024-01-01T00:00:04Z|ch_3|m_dup|9999999
DISPUTE|2024-01-01T00:00:05Z|ch_3
DISPUTE|2024-01-01T00:00:06Z|ch_3
DISPUTE|2024-01-01T00:00:07Z|ch_nope
REVERSE|2024-01-01T00:00:08Z|ch_2
CHARGE|2024-01-01T00:00:09Z|ch_4|m_tie|1000
CHARGE|2024-01-01T00:00:09Z|ch_5|m_tie|1000
DISPUTE|2024-01-01T00:00:10Z|ch_4
REVERSE|2024-01-01T00:00:10Z|ch_4
```

Expected output, Part 2:

```
m_tie|2|2000|1000|5000|FLAGGED
m_dup|1|1000|1000|10000|FLAGGED
m_zero|2|0|0|0|OK
```

Expected output, Part 3:

```
m_tie|2|2000|0|0|OK
m_dup|1|1000|1000|10000|FLAGGED
m_zero|2|0|0|0|OK
```

`m_dup`'s second `ch_3` is discarded, so its gross is 1000 and not 10000999. The
second `DISPUTE|ch_3` does not double the disputed amount. `ch_nope` is unknown.
`m_zero` divides by zero unless guarded. The `THRESHOLD|m_dup|0` overrides the 999.

`m_tie` is the same-timestamp test. Its `DISPUTE` and `REVERSE` are stamped
`00:00:10` to the second, and only the file order separates them. Part 3 must sort
**stably**, keep the dispute ahead of the reversal, and end at `0` disputed. Any sort
that reorders equal keys — or a dict keyed on the timestamp — flips them, the
reversal becomes a no-op against a charge that is not yet disputed, and `m_tie`
reports `1000|5000|FLAGGED` instead. Part 2 has no reversals, so it legitimately
reports exactly that.

### Hidden 3 — exact threshold, gross tie, rejection after block, Part 4 (`tests/hidden3_boundary.in`)

```
THRESHOLD|m_b|3333
DISPUTE|2024-02-01T00:00:09Z|c7
CHARGE|2024-02-01T00:00:00Z|c1|m_a|1000
CHARGE|2024-02-01T00:00:04Z|c4|m_b|1000
DISPUTE|2024-02-01T00:00:03Z|c1
CHARGE|2024-02-01T00:00:01Z|c2|m_a|1000
THRESHOLD|m_a|3332
CHARGE|2024-02-01T00:00:05Z|c5|m_b|1000
CHARGE|2024-02-01T00:00:02Z|c3|m_a|1000
DISPUTE|2024-02-01T00:00:07Z|c4
CHARGE|2024-02-01T00:00:06Z|c6|m_b|1000
CHARGE|2024-02-01T00:00:08Z|c7|m_a|500000
```

Expected output, Part 4:

```
m_a|3|3000|1000|3333|BLOCKED|1
m_b|3|3000|1000|3333|OK|0
TOTAL|2|1|1
```

Both merchants land on exactly 3333 bps. `m_a`'s limit is 3332, so it blocks; `m_b`'s
is 3333, so it does not. `m_a`'s 500000 charge is rejected, which keeps the two gross
totals tied at 3000 and forces the `merchant_id` tie-break. The very first line of
the file disputes `c7`, a charge that will be rejected nine seconds later and
therefore never exists.
