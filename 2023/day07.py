from day import Day
from collections import defaultdict
from functools import cmp_to_key

class Day07(Day):

    def __init__(self):
        super().__init__()

    def parse_input(self):
        self.hands = self.input.process_data_as_zip_rows(0)
        return

    def part1(self):
        def get_hand_type(hand):
            types = defaultdict(int)
            shared_lbls = 0
            for card in hand:
                if card in types and types[card] < 2:
                    shared_lbls += 1
                types[card] += 1
            match len(types):
                case 1: return 7
                case 2: return 6 if shared_lbls == 1 else 5
                case 3: return 4 if shared_lbls == 1 else 3
                case 4: return 2
                case 5: return 1
                case _: return 0
        def card_ord(card1, card2):
            custom_order = ['T', 'J', 'Q', 'K', 'A']
            def custom_sort_key(char1, char2):
                return custom_order.index(char1) - custom_order.index(char2)

            match card1.isdigit(), card2.isdigit():
                case True , True: return int(card1) - int(card2)
                case False, True: return 1
                case True , False: return -1
                case False, False:
                    return custom_sort_key(card1, card2)

        def cards_ord(hand1, hand2):
            cards = list(zip(hand1, hand2))
            for card1, card2 in cards:
                if card1 != card2:
                    return card_ord(card1, card2)
                else:
                    continue
            return 1

        def hand_ord(hand1, hand2):
            type1 = get_hand_type(hand1)
            type2 = get_hand_type(hand2)
            if type1 != type2:
                return type1 - type2
            else:
                return cards_ord(hand1, hand2)

        sorted_tuples = sorted(self.hands, key=cmp_to_key(lambda x, y: hand_ord(x[0], y[0])))
        res = 0
        for i , (_ , bid) in enumerate(sorted_tuples):
            res += (i+1) * int(bid)

        return res

    def part2(self):
        def get_hand_type(hand):
            types = defaultdict(int)
            shared_lbls = 0
            for card in hand:
                if card in types and types[card] < 2:
                    shared_lbls += 1
                types[card] += 1
            if 'J' not in types:
                match len(types):
                    case 1: return 7
                    case 2: return 6 if shared_lbls == 1 else 5
                    case 3: return 4 if shared_lbls == 1 else 3
                    case 4: return 2
                    case 5: return 1
                    case _: return 0
            else:
                match types['J']:
                    case 5: return 7
                    case 4: return 7
                    case 3:
                        if shared_lbls == 2:
                            return 7
                        else:
                            return 6
                    case 2:
                        match shared_lbls:
                            case 1: return 4
                            case 2:
                                if len(types) == 2:
                                    return 7
                                else:
                                    return 6
                    case 1:
                        match shared_lbls:
                            case 0: return 2
                            case 1:
                                match len(types):
                                    case 2:
                                        return 7
                                    case 3:
                                        return 6
                                    case 4:
                                        return 4
                            case 2: return 5

        def card_ord(card1, card2):
            custom_order = ['T', 'Q', 'K', 'A']
            def custom_sort_key(card):
                if card.isdigit():
                    return int(card)
                elif card == 'J':
                    return 1
                return 10 + custom_order.index(card)

            return custom_sort_key(card1) - custom_sort_key(card2)

        def cards_ord(hand1, hand2):
            cards = list(zip(hand1, hand2))
            for card1, card2 in cards:
                if card1 != card2:
                    return card_ord(card1, card2)
                else:
                    continue
            return 0

        def hand_ord(hand1, hand2):
            type1 = get_hand_type(hand1)
            type2 = get_hand_type(hand2)
            if type1 != type2:
                return type1 - type2
            else:
                return cards_ord(hand1, hand2)

        sorted_tuples = sorted(self.hands, key=cmp_to_key(lambda x, y: hand_ord(x[0], y[0])))
        res = 0
        for i , (_ , bid) in enumerate(sorted_tuples):
            res += (i+1) * int(bid)

        return res