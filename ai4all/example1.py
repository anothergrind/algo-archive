x = [1, 2, 3, 4]
y = 5

# brute force way, O(n^2)
def find_target(x , y):
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            if x[i] + x[j] == y:
                return (x[i], x[j])
    return None 

# divide and conquer way, O(n log n)
def find_minimum(x):
    if not x:
        return None
    
    # divide the list into two halves
    mid = len(x) / 2
    left_half = x[:mid]
    right_half = x[mid:]
    
    # check for base case, which is when there is one element per sub array
    if len(left_half) == 1 and len(right_half) == 1:
        return min(left_half[0], right_half[0])
    
    # recursively find the minimum in each half
    min_left = find_minimum(left_half)
    min_right = find_minimum(right_half)
    
    # return the overall minimum
    return min(min_left, min_right)

# divide and conquer way, O(n log n)
def find_maximum(x):
    if not x:
        return None
    
    # divide the list into two halves
    mid = len(x) / 2
    left_half = x[:mid]
    right_half = x[mid:]
    
    # check for base case, which is when there is one element per sub array
    if len(left_half) == 1 and len(right_half) == 1:
        return max(left_half[0], right_half[0])
    
    # recursively find the maximum in each half
    max_left = find_maximum(left_half)
    max_right = find_maximum(right_half)
    
    # return the overall maximum
    return max(max_left, max_right)

