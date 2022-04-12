from douzero.env.utils import MIN_SINGLE_CARDS, MIN_PAIRS, MIN_TRIPLES, select
import collections
import itertools

class MovesGener(object):
    """
    This is for generating the possible combinations
    """
    def __init__(self, cards_list):
        self.cards_list = cards_list
        self.cards_dict = collections.defaultdict(int)

        for i in self.cards_list:
            self.cards_dict[i] += 1

        self.single_card_moves = []
        self.gen_type_1_single()
        self.pair_moves = []
        self.gen_type_2_pair()
        self.triple_cards_moves = []
        self.gen_type_3_triple()
        self.bomb_moves = []
        self.gen_type_4_bomb()
        self.final_bomb_moves = []
        self.gen_type_5_king_bomb()

    def _gen_serial_moves(self, cards, min_serial, repeat=1, repeat_num=0):
        if repeat_num < min_serial:  # at least repeat_num is min_serial
            repeat_num = 0

        single_cards = sorted(list(set(cards)))
        seq_records = []
        moves = []

        start = i = 0
        longest = 1
        while i < len(single_cards):
            if i + 1 < len(single_cards) and single_cards[i + 1] - single_cards[i] == 1:
                longest += 1
                i += 1
            else:
                seq_records.append((start, longest))
                i += 1
                start = i
                longest = 1

        for seq in seq_records:
            if seq[1] < min_serial:
                continue
            start, longest = seq[0], seq[1]
            longest_list = single_cards[start: start + longest]

            if repeat_num == 0:  # No limitation on how many sequences
                steps = min_serial
                while steps <= longest:
                    index = 0
                    while steps + index <= longest:
                        target_moves = sorted(longest_list[index: index + steps] * repeat)
                        moves.append(target_moves)
                        index += 1
                    steps += 1

            else:  # repeat_num > 0
                if longest < repeat_num:
                    continue
                index = 0
                while index + repeat_num <= longest:
                    target_moves = sorted(longest_list[index: index + repeat_num] * repeat)
                    moves.append(target_moves)
                    index += 1

        return moves

    def gen_type_1_single(self):
        self.single_card_moves = [[i] for i in set(self.cards_list)]
        return self.single_card_moves

    def gen_type_2_pair(self):
        self.pair_moves = [[k, k] for k, v in self.cards_dict.items() if v >= 2]
        return self.pair_moves

    def gen_type_3_triple(self):
        self.triple_cards_moves = [
            [k, k, k] for k, v in self.cards_dict.items() if v >= 3
        ]

        return self.triple_cards_moves

    def gen_type_4_bomb(self):
        self.bomb_moves = [[k, k, k, k] for k, v in self.cards_dict.items() if v == 4]
        return self.bomb_moves

    def gen_type_5_king_bomb(self):
        self.final_bomb_moves = []
        if 20 in self.cards_list and 30 in self.cards_list:
            self.final_bomb_moves.append([20, 30])
        return self.final_bomb_moves

    def gen_type_6_3_1(self):
        return [
            t + i
            for t, i in itertools.product(
                self.single_card_moves, self.triple_cards_moves
            )
            if t[0] != i[0]
        ]

    def gen_type_7_3_2(self):
        return [
            t + i
            for t, i in itertools.product(self.pair_moves, self.triple_cards_moves)
            if t[0] != i[0]
        ]

    def gen_type_8_serial_single(self, repeat_num=0):
        return self._gen_serial_moves(self.cards_list, MIN_SINGLE_CARDS, repeat=1, repeat_num=repeat_num)

    def gen_type_9_serial_pair(self, repeat_num=0):
        single_pairs = [k for k, v in self.cards_dict.items() if v >= 2]
        return self._gen_serial_moves(single_pairs, MIN_PAIRS, repeat=2, repeat_num=repeat_num)

    def gen_type_10_serial_triple(self, repeat_num=0):
        single_triples = [k for k, v in self.cards_dict.items() if v >= 3]
        return self._gen_serial_moves(single_triples, MIN_TRIPLES, repeat=3, repeat_num=repeat_num)

    def gen_type_11_serial_3_1(self, repeat_num=0):
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_1_moves = []

        for s3 in serial_3_moves:  # s3 is like [3,3,3,4,4,4]
            s3_set = set(s3)
            new_cards = [i for i in self.cards_list if i not in s3_set]

            # Get any s3_len items from cards
            subcards = select(new_cards, len(s3_set))

            serial_3_1_moves.extend(s3 + i for i in subcards)
        return [k for k, _ in itertools.groupby(serial_3_1_moves)]

    def gen_type_12_serial_3_2(self, repeat_num=0):
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_2_moves = []
        pair_set = sorted([k for k, v in self.cards_dict.items() if v >= 2])

        for s3 in serial_3_moves:
            s3_set = set(s3)
            pair_candidates = [i for i in pair_set if i not in s3_set]

            # Get any s3_len items from cards
            subcards = select(pair_candidates, len(s3_set))
            serial_3_2_moves.extend(sorted(s3 + i * 2) for i in subcards)
        return serial_3_2_moves

    def gen_type_13_4_2(self):
        four_cards = [k for k, v in self.cards_dict.items() if v == 4]
        result = []
        for fc in four_cards:
            cards_list = [k for k in self.cards_list if k != fc]
            subcards = select(cards_list, 2)
            result.extend([fc]*4 + i for i in subcards)
        return [k for k, _ in itertools.groupby(result)]

    def gen_type_14_4_22(self):
        four_cards = [k for k, v in self.cards_dict.items() if v == 4]
        result = []
        for fc in four_cards:
            cards_list = [k for k, v in self.cards_dict.items() if k != fc and v>=2]
            subcards = select(cards_list, 2)
            result.extend([fc] * 4 + [i[0], i[0], i[1], i[1]] for i in subcards)
        return result

    # generate all possible moves from given cards
    def gen_moves(self):
        moves = []
        moves.extend(self.gen_type_1_single())
        moves.extend(self.gen_type_2_pair())
        moves.extend(self.gen_type_3_triple())
        moves.extend(self.gen_type_4_bomb())
        moves.extend(self.gen_type_5_king_bomb())
        moves.extend(self.gen_type_6_3_1())
        moves.extend(self.gen_type_7_3_2())
        moves.extend(self.gen_type_8_serial_single())
        moves.extend(self.gen_type_9_serial_pair())
        moves.extend(self.gen_type_10_serial_triple())
        moves.extend(self.gen_type_11_serial_3_1())
        moves.extend(self.gen_type_12_serial_3_2())
        moves.extend(self.gen_type_13_4_2())
        moves.extend(self.gen_type_14_4_22())
        return moves
