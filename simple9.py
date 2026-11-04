# Simple-9 encoding.
# Each 32-bit word = 4 selector bits + 28 data bits.
# The selector says how the 28 data bits are split:
#   selector: (how many numbers, bits per number)
LAYOUTS = [
    (28, 1),
    (14, 2),
    (9, 3),
    (7, 4),
    (5, 5),
    (4, 7),
    (3, 9),
    (2, 14),
    (1, 28),
]

def fits(group, bits):
    for n in group:
        if n < 0 or n >= 2 ** bits:
            return False
    return True

def simple9_encode(numbers):
    words = []
    i = 0
    while i < len(numbers):
        chosen = None
        # first try to find a layout that is completely filled
        for selector in range(len(LAYOUTS)):
            count, bits = LAYOUTS[selector]
            group = numbers[i:i + count]
            if len(group) == count and fits(group, bits):
                chosen = selector
                break
        # near the end of the list there may not be enough numbers left
        # to fill a word, so take the first layout the rest fits into
        if chosen is None:
            for selector in range(len(LAYOUTS)):
                count, bits = LAYOUTS[selector]
                group = numbers[i:i + count]
                if fits(group, bits):
                    chosen = selector
                    break
        if chosen is None:
            raise ValueError("Number too large for Simple-9 (max 2^28 - 1): " + str(numbers[i]))

        count, bits = LAYOUTS[chosen]
        group = numbers[i:i + count]
        word = format(chosen, "04b")
        for n in group:
            word += format(n, "0" + str(bits) + "b")
        word += "0" * (32 - len(word))   # pad unused bits with zeros
        words.append(word)
        i += len(group)
    return words


# Simple-9 decoding.
# Read 32 bits at a time. The first 4 bits are the selector, which says
# how many numbers there are and how many bits each one uses.

def simple9_decode(bits):
    if len(bits) % 32 != 0:
        raise ValueError("Bit string length must be a multiple of 32")
    numbers = []
    for i in range(0, len(bits), 32):
        word = bits[i:i + 32]
        selector = int(word[:4], 2)
        if selector >= len(LAYOUTS):
            raise ValueError("Unknown selector: " + word[:4])
        count, size = LAYOUTS[selector]
        group = []
        for j in range(count):
            start = 4 + j * size
            group.append(int(word[start:start + size], 2))
        # the last word may be padded with zeros, so remove them
        if i + 32 == len(bits):
            while len(group) > 0 and group[-1] == 0:
                group.pop()
        numbers.extend(group)
    return numbers
