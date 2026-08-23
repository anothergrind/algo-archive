# I forgot to have the freq_list for every instance
# I forgot to pop out the value from the dictionary after I add it to the list

def topKFrequent(self, nums: list[int], k: int) -> list[int]:
    # create a dictionary, have it match the key with the index, and the value with the number of times we see it
    # pick the biggest number from dictionary, add it to list, continue until k = 0
    num_list = []
    freq_list = {}
    high_key = 0

    for i in nums:
        freq_list[i] = freq_list.get(i, 0) + 1

    while k > 0:
        high_key = max(freq_list, key=freq_list.get)
        num_list.append(high_key)
        freq_list.pop(high_key)
        k = k - 1

    return num_list
