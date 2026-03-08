# Design an algorithm to encode a list of strings to a string. 
# The encoded string is then sent over the network and is decoded back to the original list of strings.

# Machine 1 (sender) has the function:
# string encode(vector<string> strs) {
#     // ... your code
#     return encoded_string;
# }

# Machine 2 (receiver) has the function:
# vector<string> decode(string s) {
#     //... your code
#     return strs;
# }

# So Machine 1 does:
# string encoded_string = encode(strs);

# and Machine 2 does:
# vector<string> strs2 = decode(encoded_string);

# strs2 in Machine 2 should be the same as strs in Machine 1.


# Example 1:
#   Input: dummy_input = ["Hello","World"]
#   Output: ["Hello","World"]

# Explanation:
# Machine 1:
# Codec encoder = new Codec();
# String msg = encoder.encode(strs);
# Machine 1 ---msg---> Machine 2

# Machine 2:
# Codec decoder = new Codec();
# String[] strs = decoder.decode(msg);

# Example 2:
# Input: dummy_input = [""]
# Output: [""]


# Constraints:
#     0 <= strs.length < 100
#     0 <= strs[i].length < 200
#     strs[i] contains any possible characters out of 256 valid ASCII characters.


# encode: take all list and concatenate it into a string
def encode(self, strs: list[str]) -> str:
    encoded_str = ""
    for i in range(len(strs)):
        encoded_str = encoded_str + " " + strs[i]

    return encoded_str


# decode: take string and break it up into smaller parts
# i don't think i can use static value to split the string by, but i'll start with that
def decode(self, s: str) -> list[str]:
    s = s.strip()
    if not s:
        return [""]
        
    decoded_str = []
    current = ""
    for char in s:
        if char == " ":
            if current:  # Skip extra spaces
                decoded_str.append(current)
            current = ""
        else:
            current += char
    if current:
        decoded_str.append(current)
    return decoded_str

        
