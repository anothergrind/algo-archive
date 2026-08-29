class Solution(object):
    def fizzBuzz(self, n):
        """
        :type n: int
        :rtype: List[str]
        """

        arr = list(range(1, n + 1))
        for i in range(len(arr)):
            num = i + 1 
            
            if num % 15 == 0:
                arr[i] = "FizzBuzz"
            elif num % 3 == 0:
                arr[i] = "Fizz"
            elif num % 5 == 0:
                arr[i] = "Buzz"
            else:
                arr[i] = str(num)
        return arr