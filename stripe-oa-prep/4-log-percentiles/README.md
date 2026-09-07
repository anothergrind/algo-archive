# Problem 4 — Latency Report

**Theme:** raw log parsing, path normalisation, nearest-rank percentiles, error
filtering, sectioned report output.
**Target time:** 60 min across 4 parts (15 / 15 / 15 / 15).

Run the reference solution with `python code.py <part>`, input on stdin.

---

## Common input grammar (all parts)

One log line per record. Fields are separated by **runs of whitespace** (a line may
contain more than one space between fields):

```
<timestamp> <level> <service> <key>=<value> <key>=<value> ...
```

- The first three tokens are always the timestamp, the log level and the service
  name, in that order.
- Every remaining token is a `key=value` pair. **The pairs may appear in any order.**
  Split each on its *first* `=` only — values can contain `=`.
- The keys used are `method`, `path`, `status`, `duration_ms` and `request_id`.
  Additional unknown keys may appear and are ignored. If a key appears more than once
  on the same line, the **first** occurrence wins.
- `duration_ms` is a whole number of milliseconds.
- Blank lines may appear anywhere and must be ignored.

### Endpoint normalisation

An **endpoint** is the string `"<method> <normalised_path>"` — method, one space,
path.

To normalise a path:

1. Drop everything from the first `?` onward.
2. Drop one trailing `/`, unless the path is exactly `/`.
3. Split on `/` and replace each **id segment** with the literal `{id}`.

A segment is an id segment when it is either:

- entirely digits (`0`, `12`, `2024`), or
- a Stripe-style object id: a lowercase alphabetic prefix of **2 to 4** letters, then
  an underscore, then a non-empty alphanumeric suffix (`ch_1A2b3C`, `cus_42`).

Everything else is left alone — including `v1`, `abcde_1` (prefix too long), `ch_`
(empty suffix) and `_abc` (empty prefix).

### Percentiles

Use **nearest-rank** on the endpoint's durations sorted ascending, 0-indexed:

```
idx = ceil(p * n / 100) - 1        # clamp into [0, n-1]
p_value = sorted_durations[idx]
```

So `p50` of a single-sample endpoint is that sample, and `p50` of
`[10, 20, 30, 40]` is `20` — not the average of the two middle values.

---

## Part 1 — Request counts per endpoint

Every line is well-formed — four or more tokens, every pair splittable, all five keys
present, `status` three digits and `duration_ms` all digits — and every `request_id`
is unique. There is nothing to skip and nothing to deduplicate at Parts 1 and 2.

### Output

One line per endpoint, sorted by **count descending**, ties broken by
**endpoint ascending (ASCII)**:

```
<endpoint>|<count>
```

---

## Part 2 — Latency percentiles

Same guarantees as Part 1.

### Output

One line per endpoint, sorted by **p99 descending**, ties broken by **endpoint
ascending (ASCII)**:

```
<endpoint>|<count>|<p50>|<p95>|<p99>
```

---

## Part 3 — Dirty logs

The input is now real. Apply these rules in order, per line:

1. **Level filter.** A line whose level is `DEBUG` or `TRACE` is dropped entirely.
   It is *not* counted as parsed and *not* counted as skipped — it never happened.
2. **Malformed.** A line is malformed, and counted as skipped, if any of:
   - it has fewer than 4 whitespace-separated tokens;
   - a token after the first three contains no `=`;
   - any of the five keys is missing;
   - `status` is not exactly three digits;
   - `duration_ms` is not all digits.
3. **Duplicate.** If the line's `request_id` has already been accepted, the line is
   dropped and counted as a duplicate. First occurrence wins.

An **error** is a request whose `status` is 500 or greater.

### Output

One line per endpoint, sorted by **p99 descending**, ties broken by endpoint
ascending:

```
<endpoint>|<count>|<error_count>|<p50>|<p95>|<p99>
```

Then, always, exactly these two lines:

```
SKIPPED|<malformed_line_count>
DUPLICATE|<duplicate_line_count>
```

---

## Part 4 — Service report

Same parsing and filtering as Part 3. The output becomes three labelled sections.
**All three headers are always printed, even when the section beneath is empty.**

```
[SERVICE]
<service>|<count>|<error_count>|<p99>
...
[SLOWEST]
<rank>|<endpoint>|<p99>
...
[TOTALS]
LINES|<parsed>|<skipped>|<duplicate>
```

- Service rows: one per service that had at least one parsed line, sorted by **count
  descending**, ties broken by **service name ascending**. `p99` is computed over
  that service's merged durations across all its endpoints.
- Slowest rows: the **top 3** endpoints by **p99 descending**, ties broken by **count
  descending**, then **endpoint ascending**. `rank` is `1`, `2`, `3`; print fewer
  rows if there are fewer endpoints.
- Empty input produces exactly four lines: the three headers and `LINES|0|0|0`.
  Parts 1–3 print nothing at all for empty input except Part 3's two trailing
  counters, which are always present.

---

## Sample test cases

### Sample 1 — `tests/sample1.in` (Parts 1 and 2)

```
2024-06-01T10:00:00.100Z INFO api method=GET path=/v1/charges/ch_1A2b3C status=200 duration_ms=12 request_id=req_001
2024-06-01T10:00:00.200Z INFO api method=GET path=/v1/charges/ch_9zZ status=200 duration_ms=40 request_id=req_002
2024-06-01T10:00:00.300Z INFO api method=GET path=/v1/charges/ch_x status=404 duration_ms=7 request_id=req_003
2024-06-01T10:00:00.400Z INFO api method=POST path=/v1/charges status=200 duration_ms=250 request_id=req_004
2024-06-01T10:00:00.500Z INFO api method=POST path=/v1/charges status=500 duration_ms=900 request_id=req_005
2024-06-01T10:00:00.600Z INFO api method=GET path=/v1/customers/cus_42/sources/12 status=200 duration_ms=33 request_id=req_006
```

Expected output, Part 1:

```
GET /v1/charges/{id}|3
POST /v1/charges|2
GET /v1/customers/{id}/sources/{id}|1
```

Expected output, Part 2:

```
POST /v1/charges|2|250|900|900
GET /v1/charges/{id}|3|12|40|40
GET /v1/customers/{id}/sources/{id}|1|33|33|33
```

`v1` is not an id segment even though it contains a digit. `ch_x` is an id even
though its suffix is a single character. `12` is an id because it is all digits.

### Sample 2 — `tests/sample2.in` (Parts 3 and 4)

```
2024-06-02T08:00:00.000Z INFO  api duration_ms=15 method=GET request_id=req_101 path=/v1/balance status=200
2024-06-02T08:00:01.000Z DEBUG api method=GET path=/v1/balance status=200 duration_ms=999 request_id=req_102
2024-06-02T08:00:02.000Z INFO api method=GET path=/v1/balance/ status=200 duration_ms=25 request_id=req_103
2024-06-02T08:00:03.000Z INFO api method=GET path=/v1/balance?limit=10 status=200 duration_ms=35 request_id=req_104
2024-06-02T08:00:04.000Z INFO api method=GET path=/v1/balance status=200 duration_ms=45 request_id=req_101
2024-06-02T08:00:05.000Z WARN worker method=POST path=/v1/payouts status=502 duration_ms=1200 request_id=req_105
2024-06-02T08:00:06.000Z ERROR worker method=POST path=/v1/payouts status=500 duration_ms=800 request_id=req_106
2024-06-02T08:00:07.000Z INFO worker method=POST path=/v1/payouts status=200 duration_ms=100 request_id=req_107
2024-06-02T08:00:08.000Z INFO api method=GET path=/v1/balance status=20X duration_ms=5 request_id=req_108
2024-06-02T08:00:09.000Z INFO api method=GET status=200 duration_ms=5 request_id=req_109
2024-06-02T08:00:10.000Z garbage
```

Expected output, Part 3:

```
POST /v1/payouts|3|2|800|1200|1200
GET /v1/balance|3|0|25|35|35
SKIPPED|3
DUPLICATE|1
```

Expected output, Part 4:

```
[SERVICE]
api|3|0|35
worker|3|2|1200
[SLOWEST]
1|POST /v1/payouts|1200
2|GET /v1/balance|35
[TOTALS]
LINES|6|3|1
```

The first line has two spaces after `INFO` and its keys are shuffled. `/v1/balance/`
and `/v1/balance?limit=10` both normalise onto `/v1/balance`. The `DEBUG` line's
999 ms never enters any percentile and is not counted anywhere. The three skipped
lines are the `20X` status, the line with no `path`, and `garbage`.

---

## When you think you are done

The gotchas — the edge cases the secret tests actually probe — and three hidden
test cases per problem live in [SPOILERS.md](SPOILERS.md). Work all four parts
against the samples first; open it only once you have something you believe is
finished, or once you are properly stuck.
