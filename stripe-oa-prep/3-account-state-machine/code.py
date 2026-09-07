"""Account Lifecycle Machine -- reference solution for all 4 parts.

usage: python code.py <part>   # input on stdin
"""
import sys

LIFECYCLE = {
    "OPEN": (None, "PENDING"),
    "VERIFY": ("PENDING", "ACTIVE"),
    "SUSPEND": ("ACTIVE", "SUSPENDED"),
    "REINSTATE": ("SUSPENDED", "ACTIVE"),
}
MONEY = ("DEPOSIT", "WITHDRAW")
KNOWN = set(LIFECYCLE) | set(MONEY) | {"CLOSE"}


def is_uint(s):
    return s.isdigit()


def dollars(cents):
    return "%d.%02d" % (cents // 100, cents % 100)


def solve(part, lines):
    state = {}        # account_id -> state
    balance = {}      # account_id -> cents
    last_ts = {}      # account_id -> ts of last APPLIED command
    seen_keys = set()
    rejects = {}
    applied = 0

    def reject(code):
        rejects[code] = rejects.get(code, 0) + 1

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        f = line.split(",")

        if len(f) != 5:
            reject("MALFORMED")
            continue
        ts, key, acct, cmd, arg = f

        if cmd not in KNOWN:
            reject("BAD_COMMAND")
            continue
        if cmd in MONEY and not is_uint(arg):
            reject("MALFORMED")
            continue

        if part >= 3:
            if key in seen_keys:
                reject("DUPLICATE_KEY")
                continue
            seen_keys.add(key)

        cur = state.get(acct)

        if cmd != "OPEN" and cur is None:
            reject("UNKNOWN_ACCOUNT")
            continue

        if part >= 3 and cur is not None and ts < last_ts.get(acct, ""):
            reject("STALE_TIMESTAMP")
            continue

        if cmd == "OPEN":
            if cur is not None:
                reject("INVALID_TRANSITION")
                continue
            state[acct] = "PENDING"
            balance[acct] = 0

        elif cmd in LIFECYCLE:
            need, nxt = LIFECYCLE[cmd]
            if cur != need:
                reject("INVALID_TRANSITION")
                continue
            state[acct] = nxt

        elif cmd == "CLOSE":
            if cur == "CLOSED":
                reject("INVALID_TRANSITION")
                continue
            if part >= 3 and balance[acct] != 0:
                reject("NONZERO_BALANCE")
                continue
            state[acct] = "CLOSED"

        else:                                   # DEPOSIT / WITHDRAW
            if cur != "ACTIVE":
                reject("INVALID_TRANSITION")
                continue
            amt = int(arg)
            if cmd == "WITHDRAW":
                if amt > balance[acct]:
                    reject("INSUFFICIENT_FUNDS")
                    continue
                balance[acct] -= amt
            else:
                balance[acct] += amt

        applied += 1
        last_ts[acct] = ts

    out = []
    for acct in sorted(state):
        if part == 1:
            out.append("%s,%s" % (acct, state[acct]))
        elif part < 4:
            out.append("%s,%s,%d" % (acct, state[acct], balance[acct]))
        else:
            out.append("%s,%s,%s" % (acct, state[acct], dollars(balance[acct])))

    if part == 4:
        out.append("--")
        for code in sorted(rejects, key=lambda c: (-rejects[c], c)):
            out.append("%s,%d" % (code, rejects[code]))
        out.append("--")
        out.append("TOTAL,%d,%d" % (applied, sum(rejects.values())))
    return out


if __name__ == "__main__":
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("\n".join(solve(part, sys.stdin.read().splitlines())))
