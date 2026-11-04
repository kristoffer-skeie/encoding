# Elias gamma encoding.
# For a number n >= 1:
#   offset = binary of n with the leading 1 removed
#   length = length of offset, written in unary (3 -> 1110)
# Code = length followed by offset.
# Example: 9 = 1001 -> offset 001, length 3 -> 1110 001

def elias_gamma_encode(numbers):
    codes = []
    for n in numbers:
        if n < 1:
            raise ValueError("Elias gamma can only encode numbers >= 1, got " + str(n))
        binary = bin(n)[2:]        # e.g. 9 -> "1001"
        offset = binary[1:]        # remove leading 1 -> "001"
        length = "1" * len(offset) + "0"   # unary -> "1110"
        codes.append(length + offset)
    return codes


# Elias gamma decoding.
# Count the 1s until the first 0 to get the offset length,
# then read that many bits as the offset and put the leading 1 back.
# Example: 1110001 -> length 3, offset 001 -> 1001 = 9

def elias_gamma_decode(bits):
    numbers = []
    i = 0
    while i < len(bits):
        length = 0
        while bits[i] == "1":
            length += 1
            i += 1
        i += 1                      # skip the 0 that ends the unary part
        offset = bits[i:i + length]
        if len(offset) < length:
            raise ValueError("Bit string ended in the middle of a code")
        numbers.append(int("1" + offset, 2))
        i += length
    return numbers
