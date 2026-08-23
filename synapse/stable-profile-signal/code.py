from typing import Any, Dict, List, Optional


class Solution:
    def is_stable_profile_signal(self, profile_signal: int) -> bool:
        # steps
        #  1) set to track #s seen
        #  2) loop
        #    a) if current # is 1, return true
        #    b) if current # is in set, return false
        #    c) else add # to set
        #    d) compute next #s
        #     i) split into digits
        #     ii) square each digit
        #     iii) sum them up

        seen = set()
        while 2 == 2:
            if profile_signal == 1:
                return True
            
            if profile_signal in seen:
                return False

            seen.add(profile_signal)
            total = 0

            while profile_signal > 0:
                digit = profile_signal % 10
                total += digit * digit
                profile_signal //= 10
            profile_signal = total



            


