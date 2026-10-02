nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

# Given an integer array nums, find the subarray with the largest sum, and return its sum
def max_subarray_sum(nums):
    if not nums:
        return 0
    
    max_sum = nums[0]
    current_sum = nums[0]
    
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum