import argparse
from aoc2023.utils import parse_file

def parse_card(card):
    winning_numbers, my_numbers = card.split(':')[1].split('|')
    winning_numbers = winning_numbers.strip().replace('  ', ' ').split(' ')
    my_numbers = my_numbers.strip().replace('  ', ' ').split(' ')
    return winning_numbers, my_numbers

def score_card(winning_numbers, my_numbers):
    card_score = 0
    for c in my_numbers:
        if c in winning_numbers:
            if card_score == 0:
                card_score = 1
            else:
                card_score *= 2
    return card_score

def count_card_values(winning_numbers, my_numbers):
    card_win_count = 0
    for c in my_numbers:
        if c in winning_numbers:
            card_win_count += 1
    return card_win_count

def copy_cards(card_values):
    card_copies = [1] * len(card_values)
    for i, card in enumerate(card_values):
        for i_diff in range(1, card+1):
            card_copies[i + i_diff] += card_copies[i]
    return card_copies

def main(fi_name):
    cards = parse_file(fi_name)
    total_score = 0
    for card in cards:
        total_score += score_card(*parse_card(card))
    print(f"Part 1 total score: {total_score}")

    card_values = [count_card_values(*parse_card(card)) for card in cards]
    card_copies = copy_cards(card_values)
    print(f"Part 2 total cards: {sum(card_copies)}")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)