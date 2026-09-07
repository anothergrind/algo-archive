"""Composite Fee Engine -- reference solution for all 4 parts.

usage: python code.py <part>   # input on stdin
"""
import sys

USD_MICROS = 1_000_000


def half_up_div(num, den):
    """round_half_up(num / den) for num >= 0, den > 0, integers only."""
    return (num * 2 + den) // (den * 2)


def parse(lines):
    rates = {}   # (country, brand, currency) -> (bps, fixed); last line wins
    fx = {}      # currency -> micros
    caps = {}    # country -> (min_fee or None, max_fee or None); last line wins
    charges = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        f = line.split("|")
        kind = f[0]
        if kind == "RATE":
            rates[(f[1], f[2], f[3])] = (int(f[4]), int(f[5]))
        elif kind == "FX":
            if f[1] != "USD":
                fx[f[1]] = int(f[2])
        elif kind == "CAP":
            lo = None if f[2] == "-" else int(f[2])
            hi = None if f[3] == "-" else int(f[3])
            caps[f[1]] = (lo, hi)
        elif kind == "CHARGE":
            charges.append((f[1], f[2], f[3], f[4], int(f[5])))
    return rates, fx, caps, charges


def lookup_exact(rates, country, brand, currency):
    return rates.get((country, brand, currency))


def lookup_wildcard(rates, country, brand, currency):
    """Most specific match wins; specificity compared field-by-field,
    country > brand > currency."""
    best_score, best_val = None, None
    for (c, b, cur), val in rates.items():
        if c != country and c != "*":
            continue
        if b != brand and b != "*":
            continue
        if cur != currency and cur != "*":
            continue
        score = (c != "*", b != "*", cur != "*")
        if best_score is None or score > best_score:
            best_score, best_val = score, val
    return best_val


def to_usd(fx, currency, amount):
    if currency == "USD":
        return amount
    if currency not in fx:
        return None
    return half_up_div(amount * fx[currency], USD_MICROS)


def fee_for(amount_usd, bps, fixed):
    return half_up_div(amount_usd * bps, 10_000) + fixed


def clamp(fee, caps, country):
    lo, hi = caps.get(country, (None, None))
    if lo is not None and fee < lo:
        fee = lo
    if hi is not None and fee > hi:
        fee = hi
    return fee


def solve(part, lines):
    rates, fx, caps, charges = parse(lines)
    out = []
    agg = {}          # country -> [count, total_usd, total_fee]
    skipped = 0
    tot = [0, 0, 0]

    for cid, country, brand, currency, amount in charges:
        if part == 1:
            bps, fixed = lookup_exact(rates, country, brand, currency)
            fee = fee_for(amount, bps, fixed)
            out.append("%s|%d|%d" % (cid, fee, amount - fee))
            continue

        rate = lookup_wildcard(rates, country, brand, currency)
        if rate is None:
            skipped += 1
            if part < 4:
                out.append("%s|NO_RATE" % cid)
            continue

        if part == 2:
            fee = fee_for(amount, rate[0], rate[1])
            out.append("%s|%d|%d" % (cid, fee, amount - fee))
            continue

        usd = to_usd(fx, currency, amount)
        if usd is None:
            skipped += 1
            if part < 4:
                out.append("%s|NO_FX" % cid)
            continue

        fee = clamp(fee_for(usd, rate[0], rate[1]), caps, country)

        if part == 3:
            out.append("%s|%d|%d|%d" % (cid, usd, fee, usd - fee))
        else:
            row = agg.setdefault(country, [0, 0, 0])
            row[0] += 1
            row[1] += usd
            row[2] += fee
            tot[0] += 1
            tot[1] += usd
            tot[2] += fee

    if part == 4:
        for country in sorted(agg, key=lambda c: (-agg[c][2], c)):
            n, a, f = agg[country]
            out.append("%s|%d|%d|%d" % (country, n, a, f))
        out.append("TOTAL|%d|%d|%d" % (tot[0], tot[1], tot[2]))
        out.append("SKIPPED|%d" % skipped)
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
