# Variable byte encoding.
# Each byte holds 7 bits of the number. The first bit of a byte is a
# continuation bit: 1 marks the last byte of a number, 0 means more follow.

def var_byte_encode(numbers):
    codes = []
    for n in numbers:
        if n < 0:
            raise ValueError("Variable byte cannot encode negative numbers, got " + str(n))
        # split the number into 7-bit chunks, most significant first
        chunks = []
        while True:
            chunks.insert(0, n % 128)
            if n < 128:
                break
            n = n // 128
        # set the high bit on the last chunk
        chunks[-1] = chunks[-1] + 128
        byte_strings = []
        for c in chunks:
            byte_strings.append(format(c, "08b"))
        codes.append(" ".join(byte_strings))
    return codes


# Variable byte decoding.
# Read 8 bits at a time. Add the low 7 bits to the number.
# If the high bit is 1, the number is finished.

def var_byte_decode(bits):
    if len(bits) % 8 != 0:
        raise ValueError("Bit string length must be a multiple of 8")
    numbers = []
    n = 0
    for i in range(0, len(bits), 8):
        byte = int(bits[i:i + 8], 2)
        if byte >= 128:
            n = n * 128 + (byte - 128)
            numbers.append(n)
            n = 0
        else:
            n = n * 128 + byte
    return numbers
