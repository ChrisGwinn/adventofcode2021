#file_to_use = 'day8/day8-sample.txt'
file_to_use = 'day8/day8-input.txt'

digits_to_segments = {
                        0 : (6, 'abcefg'),
                        1 : (2, 'cf'),
                        2 : (5, 'acdeg'),
                        3 : (5, 'acdfg'),
                        4 : (4, 'bcdf'),
                        5 : (5, 'abdfg'),
                        6 : (6, 'abdefg'),
                        7 : (3, 'acf'),
                        8 : (7, 'abcdefg'),
                        9 : (6, 'abcdfg')
}

easy_digit_lengths = (digits_to_segments[1][0], digits_to_segments[4][0], digits_to_segments[7][0], digits_to_segments[8][0])

def sort_letters(a):
    return ''.join(sorted(a))

def letters_to_bitmask(s):
    mask = 0x0
    for c in s:
        mask = mask | (0x1 << (ord(c) - ord('a')))
    return mask

def solve_puzzle(signals, output_values):
    inputs_to_decode = signals.copy()
    input_to_digit = [None for i in range(10)]

    # wow, this is some ugly garbage

    # The first pass because it's easy for me to think about it this way
    for input in signals:
        length = len(input)
        if length == digits_to_segments[1][0]:
            input_to_digit[1] = input
            inputs_to_decode.remove(input)
        elif length == digits_to_segments[4][0]:
            input_to_digit[4] = input
            inputs_to_decode.remove(input)
        elif length == digits_to_segments[7][0]:
            input_to_digit[7] = input
            inputs_to_decode.remove(input)
        elif length == digits_to_segments[8][0]:
            input_to_digit[8] = input
            inputs_to_decode.remove(input)
    
    # You can pick 3 out because it is a superset of 1 and 2 & 5 aren't
    for s in filter(lambda x: len(x) == 5, inputs_to_decode):
        bm = letters_to_bitmask(s)
        if bm | letters_to_bitmask(input_to_digit[1]) == bm:
            input_to_digit[3] = s
            break
    inputs_to_decode.remove(input_to_digit[3])

    # You can get 6 because it isn't a superset of 1
    for s in filter(lambda x: len(x) == 6, inputs_to_decode):
        bm = letters_to_bitmask(s)
        if bm | letters_to_bitmask(input_to_digit[1]) != bm:
            input_to_digit[6] = s
            break
    inputs_to_decode.remove(input_to_digit[6])

    # You can get 5 because 6 is a superset of it and not 2
    for s in filter(lambda x: len(x) == 5, inputs_to_decode):
        bm = letters_to_bitmask(s)
        if bm | letters_to_bitmask(input_to_digit[6]) == letters_to_bitmask(input_to_digit[6]):
            input_to_digit[5] = s
            break
    inputs_to_decode.remove(input_to_digit[5])

    # Now you know 2 because no other ones are left with length 5
    input_to_digit[2] = next(filter(lambda x: len(x) == 5, inputs_to_decode), None)
    inputs_to_decode.remove(input_to_digit[2])

    # Now you can distinguish 0 from 9 because 0 isn't a superset of 3 and 9 is
    bm = letters_to_bitmask(inputs_to_decode[0])
    if bm | letters_to_bitmask(input_to_digit[3]) == bm:
        input_to_digit[9] = inputs_to_decode[0]
        input_to_digit[0] = inputs_to_decode[1]
    else:
        input_to_digit[0] = inputs_to_decode[0]
        input_to_digit[9] = inputs_to_decode[1]

    return  (input_to_digit.index(output_values[0]) * 1000) \
            + (input_to_digit.index(output_values[1]) * 100) \
            + (input_to_digit.index(output_values[2]) * 10) \
            + input_to_digit.index(output_values[3])


with open(file_to_use) as f:
    sum_easy_digits = 0
    sum_output_values = 0
    for line in f:
        s, ov = line.rstrip().split(' | ')
        # Thanks, dmartin for the idea that sorting the letters might make this easier
        signals = list(map(sort_letters, s.split()))
        output_values = list(map(sort_letters, ov.split()))

        # 8-1 is easy, but I have no idea how to lay groundwork for 8-2
        sum_easy_digits += sum(1 for _ in (filter(lambda x: len(x) in easy_digit_lengths, output_values )))

        # 8-2. Yikes. Let's go to a function
        sum_output_values += solve_puzzle(signals, output_values)
        
    print(f'8-1 {sum_easy_digits}')
    print(f'8-2 {sum_output_values}')
