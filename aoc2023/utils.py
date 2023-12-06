from typing import List

def parse_file(fi_name: str) -> List[str]:
    with open(fi_name, 'r') as fi:
        lines = fi.readlines()
    lines = [l.rstrip('\n') for l in lines]
    return lines