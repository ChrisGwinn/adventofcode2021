# Only need to calculate gamma, since epsilon just flips all the bits
# We can't just repeatedly xor, because there can be strings of 0s
# We _can_ take a running sum and average, since we'll know from the average which is more common
num_bits = 12
bit_pos_sum = [0] * num_bits
lines_read = 0
with open('day3-input.txt') as f:
    lines = f.readlines()
    for line in lines:
        read_bits_array = [int(a) for a in line.rstrip('\n')]
        for i in range(num_bits):
            bit_pos_sum[i] += read_bits_array[i]
        lines_read += 1
gamma = 0
epsilon = 0
for i in list(map(lambda x: (1 if x > lines_read/2 else 0), bit_pos_sum)):
    if bit_pos_sum[i] == lines_read/2:
        print('aha')
    gamma = (gamma << 1) + i
    epsilon = (epsilon << 1) + (1 if i == 0 else 0)

print (epsilon * gamma)


def find_o2(lines):
    lines_to_consider = lines
    for i in range(num_bits):
        one_lines = list(filter(lambda x: x[i] == '1', lines_to_consider))
        zero_lines = list(filter(lambda x: x[i] == '0', lines_to_consider))

        if len(zero_lines) > len(one_lines):
            if len(zero_lines) == 1:
                return int(zero_lines[0].rstrip('n'), 2)
            lines_to_consider = zero_lines
        else:
            if len(one_lines) == 1:
                return int(one_lines[0].rstrip('n'), 2)
            lines_to_consider = one_lines

def find_co2(lines):
    lines_to_consider = lines
    for i in range(num_bits):
        one_lines = list(filter(lambda x: x[i] == '1', lines_to_consider))
        zero_lines = list(filter(lambda x: x[i] == '0', lines_to_consider))

        if len(one_lines) < len(zero_lines):
            if len(one_lines) == 1:
                    return int(one_lines[0].rstrip('n'), 2)
            lines_to_consider = one_lines
        else:
            if len(zero_lines) == 1:
                    return int(zero_lines[0].rstrip('n'), 2)
            lines_to_consider = zero_lines
""" 

def find_line_code_from_bits(lines, bits):
    # find all the lines that match the first bit
    # if there's one, return the line
    # if there's more than one, move to the next bit
    lines_to_consider = lines
    bits_as_string = format(bits, '012b')
    for i in range(num_bits):
        lines_to_consider = list(filter(lambda x: x[i] == bits_as_string[i], lines_to_consider))
        print(len(lines_to_consider))
        if len(lines_to_consider) == 1:
            return int(lines_to_consider[0].rstrip('n'), 2)

oxygen_gen_rating = find_line_code_from_bits(lines, gamma)
co2_scrubber_rating = find_line_code_from_bits(lines, epsilon)
 """

oxygen_gen_rating = find_o2(lines)
co2_scrubber_rating = find_co2(lines)
print(oxygen_gen_rating * co2_scrubber_rating)