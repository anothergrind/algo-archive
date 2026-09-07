# Problem 4 — Latency Report — spoilers

**Do not open this until you have a solution you believe is finished.**
It names every trap the hidden tests are built from, and then gives you the
hidden tests themselves. Reading it first turns the exercise into transcription.

Back to the problem: [README.md](README.md)

---

## Gotchas — the hidden edge cases

1. **`split(" ")` is wrong.** Log lines pad the level column, so consecutive spaces
   appear. Use whitespace-run splitting.
2. **Values can contain `=`.** `path=/v1/x?expand=y` must split into `path` and
   `/v1/x?expand=y`. Splitting on every `=` mangles it.
3. **Key order is not fixed.** Never index the pairs positionally.
4. **`p50` is nearest-rank, not a mean.** `[10,20,30,40]` gives `20`, not `25`. This
   is the single most common wrong answer here.
5. **`p95` and `p99` collapse to the maximum for small samples.** For `n < 21` they
   are both the largest value; that is correct, not a bug.
6. **Filtered `DEBUG` lines are counted nowhere.** They inflate `SKIPPED` if you drop
   them down the malformed path.
7. **`v1` is not an id.** A "contains a digit" rule fails here; so does a bare
   "contains an underscore" rule on `abcde_1`, `ch_` and `_abc`.
8. **Trailing slash and query string collapse two endpoints into one.** Miss either
   and the counts split.
9. **Duplicate `request_id` is first-wins**, and the duplicate's duration must not
   reach the percentiles.
10. **Both tie-breaks in `[SLOWEST]` matter**, and endpoints tie on p99 constantly
    because small samples all round up to the maximum.
11. **Empty input still prints all three Part 4 headers** and the `LINES` row.

---

## Hidden test cases

### Hidden 1 — empty input, Part 4 (`tests/hidden1_empty.in`)

Input: zero bytes.

```
[SERVICE]
[SLOWEST]
[TOTALS]
LINES|0|0|0
```

### Hidden 2 — percentile ranks and both tie-breaks, Parts 3 and 4 (`tests/hidden2_percentile.in`)

```
2024-07-01T00:00:00.000Z INFO svc_a method=GET path=/a status=200 duration_ms=10 request_id=r1
2024-07-01T00:00:00.000Z INFO svc_a method=GET path=/a status=200 duration_ms=20 request_id=r2
2024-07-01T00:00:00.000Z DEBUG svc_a method=GET path=/a status=200 duration_ms=99999 request_id=r99
2024-07-01T00:00:00.000Z INFO svc_a method=GET path=/a status=200 duration_ms=30 request_id=r3
2024-07-01T00:00:00.000Z INFO svc_a method=GET path=/a status=200 duration_ms=40 request_id=r4
2024-07-01T00:00:00.000Z INFO svc_b method=GET path=/b status=503 duration_ms=40 request_id=r5
2024-07-01T00:00:00.000Z INFO svc_b method=GET path=/b status=200 duration_ms=5 request_id=r6
2024-07-01T00:00:00.000Z INFO svc_c method=GET path=/c status=200 duration_ms=40 request_id=r7
2024-07-01T00:00:00.000Z INFO svc_c method=GET path=/c status=200 duration_ms=1 request_id=r8
2024-07-01T00:00:00.000Z INFO svc_c method=GET path=/c status=200 duration_ms=9999 request_id=r1
```

Expected output, Part 3:

```
GET /a|4|0|20|40|40
GET /b|2|1|5|40|40
GET /c|2|0|1|40|40
SKIPPED|0
DUPLICATE|1
```

Expected output, Part 4:

```
[SERVICE]
svc_a|4|0|40
svc_b|2|1|40
svc_c|2|0|40
[SLOWEST]
1|GET /a|40
2|GET /b|40
3|GET /c|40
[TOTALS]
LINES|8|0|1
```

`GET /a` p50 is `20`; an averaging median gives `25` and fails. All three endpoints
have p99 `40`, so the ranking runs through count descending (`/a` has 4) and then
endpoint ascending (`/b` before `/c`). The `DEBUG` line's 99999 ms and the second
`r1`'s 9999 ms are both traps: if either reaches the percentiles, every p99 changes
and the ranking scrambles. The `DEBUG` line contributes to no counter at all, while
the duplicate lands in `LINES`' third column.

### Hidden 3 — path normalisation traps, Part 1 (`tests/hidden3_paths.in`)

```
2024-08-01T00:00:00.000Z INFO  api method=GET path=/ status=200 duration_ms=1 request_id=n1
2024-08-01T00:00:00.000Z INFO api path=/v1/ duration_ms=1 status=200 method=GET request_id=n2
2024-08-01T00:00:00.000Z INFO api method=GET path=/v1 status=200 duration_ms=1 request_id=n3
2024-08-01T00:00:00.000Z INFO api method=GET path=/v2/items/0 status=200 duration_ms=1 request_id=n4
2024-08-01T00:00:00.000Z INFO api method=GET path=/v2/items/abcde_1 status=200 duration_ms=1 request_id=n5
2024-08-01T00:00:00.000Z INFO api method=GET path=/v2/items/ch_ status=200 duration_ms=1 request_id=n6
2024-08-01T00:00:00.000Z INFO api method=GET path=/v2/items/_abc status=200 duration_ms=1 request_id=n7
2024-08-01T00:00:00.000Z INFO api method=GET path=/v2/items/cus_00 status=200 duration_ms=1 request_id=n8
2024-08-01T00:00:00.000Z INFO api method=GET path=/v2/items/12/refunds?expand=x status=200 duration_ms=1 request_id=n9
```

Expected output, Part 1:

```
GET /v1|2
GET /v2/items/{id}|2
GET /|1
GET /v2/items/_abc|1
GET /v2/items/abcde_1|1
GET /v2/items/ch_|1
GET /v2/items/{id}/refunds|1
```

`/` survives the trailing-slash rule intact, while `/v1/` collapses onto `/v1`.
`0` and `cus_00` are ids; `abcde_1`, `ch_` and `_abc` are not. The five count-1
endpoints exercise ASCII ordering across `_` (95), letters, and `{` (123).

Two silent traps: line 1 has **two** spaces after `INFO`, and line 2 lists its keys
in a different order. Neither changes the answer — but a positional parser or a
`split(" ")` produces garbage on exactly those two lines and nowhere else.
