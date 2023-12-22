import click
import re
from collections import defaultdict
from aoc2023.utils import parse_file

def holiday_hash(string):
    current_value = 0
    for character in string:
        ascii_val = ord(character)
        current_value += ascii_val
        current_value *= 17
        current_value = current_value % 256
    return current_value

def get_steps(operation):
    m = re.match("([a-z]+)(=[0-9]|-)", operation)
    label = m.group(1)
    operation = m.group(2)
    box = holiday_hash(label)
    if operation[0] == '=':
        lens = operation[1]
        operation = '='
    else:
        lens = None
    return box, label, operation, lens

def find_label_in_box(label, box):
    for i, content in enumerate(box):
        if content[0] == label:
            return i
    return None

def focusing_power(boxes):
    power = 0
    for box_id, contents in boxes.items():
        for i, lens in enumerate(contents):
            power += ((box_id + 1) * (i + 1) * int(lens[1]))
    return power

@click.command()
@click.argument('fi_name')
def main(fi_name):
    inputs = parse_file(fi_name)
    print(f"total hashed value: {sum(map(holiday_hash, inputs[0].split(',')))}")

    boxes = defaultdict(list)
    for step in inputs[0].split(','):        
        box_id, label, operation, lens = get_steps(step)
        current_label_location = find_label_in_box(label, boxes[box_id])
        if operation == '-':
            if current_label_location is not None:
                box_contents = boxes[box_id].copy()
                box_contents.pop(current_label_location)
                boxes[box_id] = box_contents
        elif operation == '=':
            if current_label_location is not None:
                boxes[box_id][current_label_location] = (label, lens)
            else:
                boxes[box_id].append((label, lens))
        else:
            ValueError(f"Operation {operation} not understood")
    print(f"Total focusing power: {focusing_power(boxes)}")

if __name__ == '__main__':
    main()