# Reflection: I didn't fully read question, really didn't even understand the anagram before implementing (1)
# I didn't implement it properly (2)
# using dictionaries is apparently the same thing as a hashtable

def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        # two for loops
        # one to keep track of current loop, index of list
        # other to keep track of the string

        res = defaultdict(list)
        n = len(strs)

        for i in range(n):
            key = "".join(sorted(strs[i]))
            res[key].append(strs[i])

        return list(res.values())
