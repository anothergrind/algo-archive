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


# earlier attempt, kept for reference -- doesn't work
def mySolution(self, nums: list[int]) -> int:
    if len(nums) == 0:
        return 0

    counter = 0
    remove_dups = set(nums)
    backList = list(remove_dups)

    for i in range(0, len(backList)):
        for j in range(0, len(backList)):
            if backList[i] + 1 == backList[j]:
                counter = counter + 1

    return counter
