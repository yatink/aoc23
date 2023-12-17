import functools
import math
import operator


def parse_input(inpt):
    lines = inpt.split('\n')
    times = [int(x) for x in lines[0].split(" ")[1:] if x]
    distances = [int(x) for x in lines[1].split(" ")[1:] if x]
    return list(zip(times, distances))


def calculate_number_of_ways(distance, time):
    common = math.sqrt(time**2 - 4*distance)
    pos = (time + common) / 2
    neg = (time - common) / 2

    offset = 0
    if math.ceil(float(pos) - float(int(pos))) == 0:
        offset -= 1
    if math.ceil(float(neg) - float(int(neg))) == 0:
        offset -= 1
        
    return int(math.floor(pos)) - int(math.ceil(neg)) + 1 + offset


def part1(inpt):
    times_distances = parse_input(inpt)
    ways = []
    for t, d in times_distances:
        ways.append(calculate_number_of_ways(d, t))
    return functools.reduce(operator.mul, ways)

def part2(inpt):
    times_distances = parse_input(inpt)
    single_time = int(''.join([str(x[0]) for x in times_distances]))
    single_distance = int(''.join([str(x[1]) for x in times_distances]))
    return calculate_number_of_ways(single_distance, single_time)


if __name__ == '__main__':
    test_inpt = """Time:      7  15   30
Distance:  9  40  200"""

    real_inpt = """Time:        44     82     69     81
Distance:   202   1076   1138   1458"""
    
    print(part1(real_inpt))
    print(part2(real_inpt))
