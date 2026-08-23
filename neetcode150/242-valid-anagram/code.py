# Mistakes I made: I was iterating via range instead of accessing the string directly

def isAnagram(self, s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    # strat is to iterate through both strings, and making sure at the end
    # the tally's are the same with a dictionary, but how to do that?
    s_dict = {}
    t_dict = {}

    for char in s:
        if char in s_dict:
            s_dict[char] = s_dict[char] + 1
        else:
            s_dict[char] = 1

    for char in t:
        if char in t_dict:
            t_dict[char] = t_dict[char] + 1
        else:
            t_dict[char] = 1

        if s_dict == t_dict:
            return True

    return False
