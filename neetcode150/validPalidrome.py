def isPalindrome(self, s: str) -> bool:
    s_comp = s.lower()
    reversed_s = s_comp[::-1]

    for i in range(len(s)):
        if s_comp.alnum():
            if reversed_s[i] != s_comp[i]:
                return False

    return True