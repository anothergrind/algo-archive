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
