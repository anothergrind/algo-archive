from typing import Any, Dict, List, Optional


class Solution:
    def rank_delay_risks(self, delivery_offsets: List[int]) -> List[int]:
        front = 0
        back = len(delivery_offsets) - 1
        end = len(delivery_offsets) - 1

        route = [0] * len(delivery_offsets)

        while front <= back:
            left = delivery_offsets[front] ** 2
            right = delivery_offsets[back] ** 2
            if left > right:
                route[end] = left
                front = front + 1
            else:
                route[end] = right
                back = back - 1
            end = end - 1

        return route