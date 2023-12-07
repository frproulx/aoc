import argparse
from collections import defaultdict
from aoc2023.utils import parse_file

CARD_ORDER = '23456789TJQKA'
CARD_SCORES = dict(zip(CARD_ORDER, range(len(CARD_ORDER))))

class Hand():
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = int(bid)

        self.score = None
        self.score_hand()

    def __repr__(self) -> str:
        return f'{self.cards} (score: {self.score})'

    def score_hand(self):
        """Create ranking level"""
        card_count = defaultdict(int)
        for card in self.cards:
            card_count[card] += 1
        if max(card_count.values()) == 5:
            # 5 of a kind
            self.score = 7
        elif max(card_count.values()) == 4:
            # 4 of a kind
            self.score = 6
        elif (2 in card_count.values()) and (3 in card_count.values()):
            # full house
            self.score = 5
        elif (3 in card_count.values()):
            # 3 of a kind
            self.score = 4
        elif sum([ct == 2 for ct in card_count.values()]) == 2:
            # 2 pair
            self.score = 3
        elif max(card_count.values()) == 2:
            self.score = 2
        else:
            self.score = 1

def compare_cards(cards1: str, cards2: str) -> bool:
    for i in range(len(cards1)):
        sc1 = CARD_SCORES[cards1[i]]
        sc2 = CARD_SCORES[cards2[i]]
        if sc1 == sc2:
            continue
        elif sc1 > sc2:
            return True
        else:
            return False
    raise Exception(f"Hands are identical! {cards1} {cards2}")

def compare_hands(hand1, hand2):
    """Returns True if hand1 bigger than hand 2"""
    if hand1.score > hand2.score:
        return True
    elif hand1.score < hand2.score:
        return False
    else:
        return compare_cards(hand1.cards, hand2.cards)

def sort_hands(hands):
    for i in range(len(hands)):
        swapped = False
        for j in range(0, len(hands) - i - 1):
            if compare_hands(hands[j], hands[j+1]):
                hands[j], hands[j+1] = hands[j+1], hands[j]
                swapped = True
        if swapped == False:
            break
    return hands

def score_hands_part1(hands):
    total_score = 0
    for i, hand in enumerate(hands):
        total_score += hand.bid * (i+1)
    return total_score

def main(fi_name):
    input = parse_file(fi_name)
    hands = [Hand(*row.split(' ')) for row in input]
    sorted_hands = sort_hands(hands)
    print(f"Part 1 score: {score_hands_part1(sorted_hands)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)