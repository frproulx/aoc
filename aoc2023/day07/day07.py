import argparse
from collections import defaultdict
from itertools import combinations_with_replacement
from aoc2023.utils import parse_file

CARD_ORDER = '23456789TJQKA'
CARD_SCORES = dict(zip(CARD_ORDER, range(len(CARD_ORDER))))
CARD_ORDER_JOKERS = 'J23456789TQKA'
CARD_SCORES_JOKERS = dict(zip(CARD_ORDER_JOKERS, range(len(CARD_ORDER_JOKERS))))

class Hand():
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = int(bid)

        self.card_count = count_cards(cards)
        self.score = None
        self.score = score_hand(self.card_count)
        self.joker_score = None
        self.joker_score = self.jokerize_score()

    def __repr__(self) -> str:
        return f'{self.cards} (score: {self.score})'

    def jokerize_score(self):
        number_of_jokers = self.card_count['J']

        if (number_of_jokers == 0):
            return self.score
        elif number_of_jokers >= 4:
            # Either of these coerce to 5 of a kind
            return 7
        else:
            return test_joker_candidates(self.cards, n_jokers=number_of_jokers)

def count_cards(cards):
    card_count = defaultdict(int)
    for card in cards:
        card_count[card] += 1
    return card_count

def score_hand(card_count):
    """Create ranking level"""
    if max(card_count.values()) == 5:
        # 5 of a kind
        return 7
    elif max(card_count.values()) == 4:
        # 4 of a kind
        return 6
    elif (2 in card_count.values()) and (3 in card_count.values()):
        # full house
        return 5
    elif (3 in card_count.values()):
        # 3 of a kind
        return 4
    elif sum([ct == 2 for ct in card_count.values()]) == 2:
        # 2 pair
        return 3
    elif max(card_count.values()) == 2:
        return 2
    else:
        return 1

def test_joker_candidates(cards: str, n_jokers: int):
    """ Test all permutations"""
    scores = []
    card_count = count_cards(cards)
    base_cards = cards.replace('J', '')
    symbols = ''.join([c for c in card_count.keys() if c != 'J'])
    symbol_candidates = combinations_with_replacement(symbols, n_jokers)
    for c in symbol_candidates:
        candidate_hand = base_cards + ''.join(c)
        scores.append(score_hand(count_cards(candidate_hand)))
    return max(scores)


def compare_cards(cards1: str, cards2: str, jokers_wild=False) -> bool:
    for i in range(len(cards1)):
        if jokers_wild:
            sc1 = CARD_SCORES_JOKERS[cards1[i]]
            sc2 = CARD_SCORES_JOKERS[cards2[i]]
        else:
            sc1 = CARD_SCORES[cards1[i]]
            sc2 = CARD_SCORES[cards2[i]]
        if sc1 == sc2:
            continue
        elif sc1 > sc2:
            return True
        else:
            return False
    raise Exception(f"Hands are identical! {cards1} {cards2}")

def compare_hands(hand1, hand2, jokers_wild=False):
    """Returns True if hand1 bigger than hand 2"""
    if jokers_wild:
        score1, score2 = hand1.joker_score, hand2.joker_score
    else:
        score1, score2 = hand1.score, hand2.score

    if score1 > score2:
        return True
    elif score1 < score2:
        return False
    else:
        return compare_cards(hand1.cards, hand2.cards, jokers_wild=jokers_wild)

def sort_hands(hands, jokers_wild=False):
    for i in range(len(hands)):
        swapped = False
        for j in range(0, len(hands) - i - 1):
            if compare_hands(hands[j], hands[j+1], jokers_wild=jokers_wild):
                hands[j], hands[j+1] = hands[j+1], hands[j]
                swapped = True
        if swapped == False:
            break
    return hands

def score_hands(hands):
    total_score = 0
    for i, hand in enumerate(hands):
        total_score += hand.bid * (i+1)
    return total_score

def main(fi_name):
    input = parse_file(fi_name)
    hands = [Hand(*row.split(' ')) for row in input]
    sorted_hands = sort_hands(hands, jokers_wild=False)
    print(f"Part 1 score: {score_hands(sorted_hands)}")

    joker_sort_hands = sort_hands(hands, jokers_wild=True)
    print(f"Part 2 score: {score_hands(joker_sort_hands)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fi_name')
    args = parser.parse_args()
    main(fi_name=args.fi_name)