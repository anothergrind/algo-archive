"""Latency Report -- reference solution for all 4 parts.

usage: python code.py <part>   # input on stdin
"""
import sys

REQUIRED = ("method", "path", "status", "duration_ms", "request_id")
IGNORED_LEVELS = ("DEBUG", "TRACE")


def is_id_segment(seg):
    """Stripe-style object id, or an all-digit segment."""
    if not seg:
        return False
    if seg.isdigit():
        return True
    prefix, sep, suffix = seg.partition("_")
    return bool(sep) and 2 <= len(prefix) <= 4 and prefix.isalpha() \
        and prefix.islower() and bool(suffix) and suffix.isalnum()


def normalize(path):
    path = path.split("?", 1)[0]
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    return "/".join("{id}" if is_id_segment(s) else s for s in path.split("/"))


def percentile(sorted_vals, p):
    """Nearest-rank: idx = ceil(p * n / 100) - 1, clamped into range."""
    n = len(sorted_vals)
    idx = -((-p * n) // 100) - 1
    return sorted_vals[min(max(idx, 0), n - 1)]


def parse_line(line, strict):
    """-> (service, endpoint, status, duration, request_id) or None if unusable."""
    tok = line.split()
    if len(tok) < 4:
        return None
    _ts, level, service = tok[0], tok[1], tok[2]
    if strict and level in IGNORED_LEVELS:
        return "FILTERED"
    kv = {}
    for t in tok[3:]:
        k, sep, v = t.partition("=")
        if not sep:
            if strict:
                return None
            continue
        kv.setdefault(k, v)
    if any(k not in kv for k in REQUIRED):
        return None
    status, dur = kv["status"], kv["duration_ms"]
    if strict and (len(status) != 3 or not status.isdigit() or not dur.isdigit()):
        return None
    if not status.isdigit() or not dur.isdigit():
        return None
    return (service, kv["method"] + " " + normalize(kv["path"]),
            int(status), int(dur), kv["request_id"])


def solve(part, lines):
    strict = part >= 3
    endpoints = {}       # endpoint -> [durations, err_count]
    services = {}        # service -> [durations, err_count]
    seen_req = set()
    parsed = skipped = duplicate = 0

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        rec = parse_line(line, strict)
        if rec == "FILTERED":
            continue
        if rec is None:
            skipped += 1
            continue
        service, endpoint, status, dur, rid = rec
        if strict:
            if rid in seen_req:
                duplicate += 1
                continue
            seen_req.add(rid)
        parsed += 1
        e = endpoints.setdefault(endpoint, [[], 0])
        e[0].append(dur)
        s = services.setdefault(service, [[], 0])
        s[0].append(dur)
        if status >= 500:
            e[1] += 1
            s[1] += 1

    for bucket in (endpoints, services):
        for v in bucket.values():
            v[0].sort()

    out = []
    if part == 1:
        for ep in sorted(endpoints, key=lambda e: (-len(endpoints[e][0]), e)):
            out.append("%s|%d" % (ep, len(endpoints[ep][0])))
        return out

    if part in (2, 3):
        def key(e):
            return (-percentile(endpoints[e][0], 99), e)
        for ep in sorted(endpoints, key=key):
            d, err = endpoints[ep]
            if part == 2:
                out.append("%s|%d|%d|%d|%d" % (
                    ep, len(d), percentile(d, 50), percentile(d, 95),
                    percentile(d, 99)))
            else:
                out.append("%s|%d|%d|%d|%d|%d" % (
                    ep, len(d), err, percentile(d, 50), percentile(d, 95),
                    percentile(d, 99)))
        if part == 3:
            out.append("SKIPPED|%d" % skipped)
            out.append("DUPLICATE|%d" % duplicate)
        return out

    out.append("[SERVICE]")
    for sv in sorted(services, key=lambda s: (-len(services[s][0]), s)):
        d, err = services[sv]
        out.append("%s|%d|%d|%d" % (sv, len(d), err, percentile(d, 99)))
    out.append("[SLOWEST]")
    ranked = sorted(endpoints,
                    key=lambda e: (-percentile(endpoints[e][0], 99),
                                   -len(endpoints[e][0]), e))
    for i, ep in enumerate(ranked[:3], 1):
        out.append("%d|%s|%d" % (i, ep, percentile(endpoints[ep][0], 99)))
    out.append("[TOTALS]")
    out.append("LINES|%d|%d|%d" % (parsed, skipped, duplicate))
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
