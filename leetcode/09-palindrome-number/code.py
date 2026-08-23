class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        regular = str(x)
        reverse = regular[::-1]
        if regular == reverse:
            return True
        else:
            return False