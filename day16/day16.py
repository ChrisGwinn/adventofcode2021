
from itertools import islice
from collections import namedtuple

Packet = namedtuple("Packet", "version literal operator packets bit_count")

# I'm sure python has libraries for this, but I don't wanna deal with leading 0s
hex_digit_to_bin = {
    '0':'0000',
    '1':'0001',
    '2':'0010',
    '3':'0011',
    '4':'0100',
    '5':'0101',
    '6':'0110',
    '7':'0111',
    '8':'1000',
    '9':'1001',
    'A':'1010',
    'B':'1011',
    'C':'1100',
    'D':'1101',
    'E':'1110',
    'F':'1111'}

def parse_version(biterator):
    return int(''.join(islice(biterator, 3)), 2)
    
def parse_type(biterator):
    return int(''.join(islice(biterator, 3)), 2)

def parse_literal(biterator, max_bits=None):
    bit_count = 0
    bits = ''
    literal = None

    # TODO: respect max_bits?
    while literal == None:
        continuation = next(biterator)
        bit_count += 1
        if continuation == '1':
            bits += ''.join(islice(biterator, 4))
            bit_count += 4
        else:
            bits += ''.join(islice(biterator, 4))
            bit_count += 4
            literal = int(bits, 2)
    return literal, bit_count

def parse_length_type_1(version, operator, biterator):
    subpacket_count = int(''.join(islice(biterator, 11)), 2)
    packets = []
    subpacket_length = 0

    for i in range(subpacket_count):
        # TODO: include max bits?
        subpacket = parse_packet(biterator)
        subpacket_length += subpacket.bit_count
        packets.append(subpacket)
    return Packet(version, None, operator, packets, 11 + 9 + subpacket_length)

def parse_length_type_0(version, operator, biterator):
    length = int(''.join(islice(biterator, 15)), 2)
    packets = []

    remaining_length = length
    # you can never have a packet shorter than 11 bits
    while remaining_length >= 11:
        subpacket = parse_packet(biterator, remaining_length)
        remaining_length -= subpacket.bit_count
        packets.append(subpacket)
    # chew up extra 0s
    if remaining_length > 0:
        islice(biterator, remaining_length)
    return Packet(version, None, operator, packets, 15 + 9 + length)

def parse_packet(biterator, max_bits=None):
    ver = parse_version(biterator)
    operator = parse_type(biterator)
    # literal
    if operator == 4: 
        lit, bit_count = parse_literal(biterator, max_bits=max_bits)
        return Packet(ver, lit, operator, None, bit_count + 6)
    else:
        # fun with recursive parsing
        length_type_id = next(biterator)
        if length_type_id == '0':
            return parse_length_type_0(ver, operator, biterator)
        else:
            return parse_length_type_1(ver, operator, biterator)

def sum_packet_version(packet):
    v = packet.version
    if packet.packets != None:
        for p in packet.packets:
            v += sum_packet_version(p)
    return v

def packet_math(packet):
    if packet.operator == 0:
        # should do this with accumulate and a 2 arg packet_math func
        i = 0
        for p in packet.packets:
            i += packet_math(p)
        return i
    if packet.operator == 1:
        # should do this with accumulate and a 2 arg packet_math func
        i = 1
        for p in packet.packets:
            i *= packet_math(p)
        return i
    if packet.operator == 2:
        return min(map(packet_math, packet.packets))
    if packet.operator == 3:
        return max(map(packet_math, packet.packets))
    if packet.operator == 4:
        return packet.literal
    if packet.operator == 5: #gt
        return 1 if packet_math(packet.packets[0]) > packet_math(packet.packets[1]) else 0
    if packet.operator == 6: #lt
        return 1 if packet_math(packet.packets[0]) < packet_math(packet.packets[1]) else 0
    if packet.operator == 7: #eq
        return 1 if packet_math(packet.packets[0]) == packet_math(packet.packets[1]) else 0


#parsed = parse_packet(iter(''.join([hex_digit_to_bin[x] for x in 'A0016C880162017C3686B18A3D4780'])))
with open('day16/day16-input.txt') as f:
    parsed = parse_packet(iter(''.join([hex_digit_to_bin[x] for x in f.readline()])))

print(f'version sum: {sum_packet_version(parsed)}')
print(f'Packet math results: {packet_math(parsed)}')
