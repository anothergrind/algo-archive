def twoSum(self, numbers: list[int], target: int) -> list[int]:
    for i in range(0, len(numbers)):
        for j in range(1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [i+1, j+1]
