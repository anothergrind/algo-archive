"""Dispute Radar -- reference solution for all 4 parts.

usage: python code.py <part>   # input on stdin
"""
import sys

DEFAULT_THRESHOLD_BPS = 100
MIN_CHARGES_TO_BLOCK = 3


def parse(lines):
    thresholds = {}   # merchant -> bps; last record wins
    events = []       # (ts, seq, kind, fields)
    seq = 0
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        f = line.split("|")
        if f[0] == "THRESHOLD":
            thresholds[f[1]] = int(f[2])
        elif f[0] in ("CHARGE", "DISPUTE", "REVERSE"):
            events.append((f[1], seq, f[0], f))
            seq += 1
    return thresholds, events


class Merchant(object):
    def __init__(self):
        self.count = 0
        self.gross = 0
        self.disputed = 0
        self.rejected = 0
        self.blocked = False

    def bps(self):
        if self.gross <= 0:
            return 0
        return (self.disputed * 10000) // self.gross


def solve(part, lines):
    thresholds, events = parse(lines)
    if part >= 3:
        events.sort(key=lambda e: (e[0], e[1]))

    merchants = {}                      # merchant_id -> Merchant
    charge_merchant = {}                # charge_id -> merchant_id (accepted only)
    charge_amount = {}
    disputed_now = set()

    def m_of(mid):
        return merchants.setdefault(mid, Merchant())

    def threshold(mid):
        return thresholds.get(mid, DEFAULT_THRESHOLD_BPS)

    for ts, _seq, kind, f in events:
        if kind == "CHARGE":
            _, _ts, cid, mid, amt = f
            if cid in charge_merchant:          # duplicate charge id: ignore
                continue
            m = m_of(mid)
            if part >= 4 and m.blocked:
                m.rejected += 1
                continue
            charge_merchant[cid] = mid
            charge_amount[cid] = int(amt)
            m.count += 1
            m.gross += int(amt)

        elif kind == "DISPUTE":
            cid = f[2]
            if cid not in charge_merchant or cid in disputed_now:
                continue                        # unknown or already disputed
            disputed_now.add(cid)
            m = merchants[charge_merchant[cid]]
            m.disputed += charge_amount[cid]
            if part >= 4 and not m.blocked:
                if (m.count >= MIN_CHARGES_TO_BLOCK
                        and m.bps() > threshold(charge_merchant[cid])):
                    m.blocked = True

        elif kind == "REVERSE" and part >= 3:
            cid = f[2]
            if cid not in disputed_now:
                continue                        # nothing to reverse
            disputed_now.discard(cid)
            merchants[charge_merchant[cid]].disputed -= charge_amount[cid]

    order = sorted(merchants, key=lambda mid: (-merchants[mid].gross, mid))
    out = []
    for mid in order:
        m = merchants[mid]
        if part == 1:
            out.append("%s|%d|%d" % (mid, m.count, m.gross))
            continue
        over = m.bps() > threshold(mid)
        if part < 4:
            status = "FLAGGED" if over else "OK"
            out.append("%s|%d|%d|%d|%d|%s"
                       % (mid, m.count, m.gross, m.disputed, m.bps(), status))
        else:
            status = "BLOCKED" if m.blocked else ("FLAGGED" if over else "OK")
            out.append("%s|%d|%d|%d|%d|%s|%d"
                       % (mid, m.count, m.gross, m.disputed, m.bps(), status,
                          m.rejected))
    if part == 4:
        out.append("TOTAL|%d|%d|%d" % (
            len(merchants),
            sum(1 for m in merchants.values() if m.blocked),
            sum(m.rejected for m in merchants.values())))
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
