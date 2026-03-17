# hash set solution
# solves in O(n) time

def longestConsecutive(self, nums: list[int]) -> int:
    numSet = set(nums)
    longest = 0

    for num in numSet:
        if (num - 1) not in numSet:
            length = 1
            while (num + length) in numSet:
                length += 1
            longest = max(length, longest)
    return longest