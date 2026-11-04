# Gap encoding - keep the first number, then store the difference
# between each number and the one before it.
# Example: [3, 7, 11, 23] -> [3, 4, 4, 12]

def gap_encode(numbers):
    numbers = sorted(numbers)
    gaps = []
    previous = 0
    for n in numbers:
        gaps.append(n - previous)
        previous = n
    return gaps

# Gap decoding: add each gap to the previous number.
# Example: [3, 4, 4, 12] -> [3, 7, 11, 23]

def gap_decode(gaps):
    numbers = []
    previous = 0
    for g in gaps:
        previous = previous + g
        numbers.append(previous)
    return numbers
