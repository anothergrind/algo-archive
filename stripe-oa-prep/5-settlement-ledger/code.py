"""Settlement Ledger -- reference solution for all 4 parts.

usage: python code.py <part>   # input on stdin
"""
import sys
from datetime import date, timedelta

CUTOFF = "17:00"
DEFAULT_DAILY_LIMIT = 500000


def to_date(s):
    return date(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def is_business(d):
    return d.weekday() < 5


def next_business(d):
    d += timedelta(days=1)
    while not is_business(d):
        d += timedelta(days=1)
    return d


def settlement_date(ts):
    """ts is 'YYYY-MM-DDTHH:MM'. Debit is instant; this is when the credit lands."""
    d, t = to_date(ts), ts[11:16]
    submit = d if (is_business(d) and t < CUTOFF) else next_business(d)
    return next_business(submit)


def parse(lines):
    opening, limits, txns = {}, {}, []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        f = line.split("|")
        if f[0] == "OPEN":
            opening.setdefault(f[1], int(f[2]))       # first OPEN wins
        elif f[0] == "LIMIT":
            limits[f[1]] = int(f[2])                  # last LIMIT wins
        elif f[0] == "XFER":
            txns.append((f[1], f[2], f[3], f[4], int(f[5])))
    return opening, limits, txns


def solve(part, lines):
    opening, limits, txns = parse(lines)
    settled = dict(opening)                # available balance
    pending = {a: [] for a in opening}     # account -> [(sdate, amount)]
    credited = {}                          # (sdate_str, account) -> amount
    daily = {}                             # (date_str, account) -> outbound
    seen_txn = set()
    rejected = []
    applied = 0

    def mature(acct, upto):
        keep = []
        for sdate, amt in pending[acct]:
            if sdate <= upto:
                settled[acct] += amt
            else:
                keep.append((sdate, amt))
        pending[acct] = keep

    for tid, ts, src, dst, amt in txns:
        if tid in seen_txn:
            rejected.append((tid, "DUPLICATE_TXN"))
            continue
        seen_txn.add(tid)

        if src not in opening or dst not in opening:
            rejected.append((tid, "UNKNOWN_ACCOUNT"))
            continue
        if src == dst:
            rejected.append((tid, "SAME_ACCOUNT"))
            continue

        day = ts[0:10]
        if part >= 3:
            mature(src, to_date(day))

        if part >= 4:
            cap = limits.get(src, DEFAULT_DAILY_LIMIT)
            if daily.get((day, src), 0) + amt > cap:
                rejected.append((tid, "LIMIT_EXCEEDED"))
                continue

        if amt > settled[src]:
            rejected.append((tid, "INSUFFICIENT_FUNDS"))
            continue

        settled[src] -= amt
        applied += 1
        if part >= 4:
            daily[(day, src)] = daily.get((day, src), 0) + amt

        if part < 3:
            settled[dst] += amt
        else:
            sdate = settlement_date(ts)
            pending[dst].append((sdate, amt))
            key = (sdate.isoformat(), dst)
            credited[key] = credited.get(key, 0) + amt

    for acct in opening:                   # everything eventually settles
        for _sdate, amt in pending[acct]:
            settled[acct] += amt
        pending[acct] = []

    out = []
    if part == 1:
        for acct in sorted(settled):
            out.append("%s|%d" % (acct, settled[acct]))
        return out

    out.append("#BALANCES")
    for acct in sorted(settled):
        out.append("%s|%d" % (acct, settled[acct]))
    out.append("#REJECTED")
    for tid, reason in rejected:
        out.append("%s|%s" % (tid, reason))
    if part >= 3:
        out.append("#SETTLEMENTS")
        for key in sorted(credited):
            out.append("%s|%s|%d" % (key[0], key[1], credited[key]))
    if part >= 4:
        out.append("#DAILY")
        for key in sorted(daily):
            out.append("%s|%s|%d" % (key[0], key[1], daily[key]))
    out.append("#TOTALS")
    out.append("TOTAL|%d|%d" % (applied, len(rejected)))
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
