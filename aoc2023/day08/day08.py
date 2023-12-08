import argparse
import re
from math import lcm
from aoc2023.utils import parse_file


def count_turns_to_zzz(turns, dungeon_map):
    turn_count = 0
    room = 'AAA'
    while room != 'ZZZ':
        for direction in turns:
            turn_count += 1
            if direction == 'L':
                room = dungeon_map[room][0]
            elif direction == 'R':
                room = dungeon_map[room][1]
            if room == 'ZZZ':
                break
    return turn_count

def ghost_walk(turns, dungeon_map):
    rooms = [room for room in dungeon_map.keys() if room.endswith('A')]
    print(rooms)
    ghost_times = []
    for i in range(len(rooms)):
        room = rooms[i]
        turn_count = 0
        while not room.endswith('Z'):
            for direction in turns:
                turn_count += 1
                if direction == 'L':
                    room = dungeon_map[room][0]
                elif direction == 'R':
                    room = dungeon_map[room][1]
                if room.endswith('Z'):
                    break
        ghost_times.append(turn_count)
    return ghost_times


def main(fi_name):
    input = parse_file(fi_name)
    map_ = {}
    for line in input:
        if re.fullmatch('[LR][^A-KM-QS-Z]+', line):
            turns = line
            continue
        line_match = re.search('([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)', line)
        if not line_match:
            continue
        # print(line_match.group(1))
        map_[line_match.group(1)] = (line_match.group(2), line_match.group(3))
    if not fi_name.split('/')[-1].endswith('test3.txt'):
        turns_to_zzz = count_turns_to_zzz(turns, map_)
        print(f"{turns_to_zzz} turns to ZZZ")
    ghost_turns = ghost_walk(turns, map_)
    print(f"Ghosts take {lcm(*ghost_turns)} turns")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)