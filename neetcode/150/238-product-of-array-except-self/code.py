def productExceptSelf(self, nums: list[int]) -> list[int]:
    # int -> list
    prod = []

    # one for loop
    # if i = counter then skip the product

    for i in range(0,len(nums)):
        product = 1
        for j in range(0, len(nums)):
            if i != j:
                product = product * nums[j]

        prod.append(product)
    return prod
