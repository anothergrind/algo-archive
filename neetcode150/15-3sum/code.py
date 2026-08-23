def threeSum(self, nums: list[int]) -> list[list[int]]:
    # base case, if all numbers in the list are > 0 just return a blank array
    addToZero = []

    for i in range(0, len(nums)):
        for j in range(i+1, len(nums)):
            for k in range(j+1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 0:
                    addToZero.append(sorted([nums[i], nums[j], nums[k]]))

    setZero = set(tuple(trip) for trip in addToZero)
    addToZero = [list(trip) for trip in setZero]

    return addToZero
