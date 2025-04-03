from player import Player, PlayerAction
from game import PokerGame, GamePhase
from card import Card, Rank, Suit, Deck
from hand_evaluator import HandRank, HandResult, HandEvaluator
import random
from collections import defaultdict

state = "normal"
class MyPlayer(Player):

    def __init__(self, name, stack):
        super().__init__(name, stack)

    def action(self, game_state: list[int], action_history: list):
        global state

        if game_state[4] != 0 and game_state[5] == 0 and game_state[6] == 0:
            comm_cards = [0, 0, 0]
            for i, j in enumerate(game_state[2:5]):
                m, n = MyPlayer.get_rank_suit(j)
                comm_cards[i] = Card(rank=Rank(m), suit=Suit(n))
            
            my_result = HandEvaluator.evaluate_hand(self.hole_cards, comm_cards)
            if my_result.hand_rank.value >= 4:
                state = "aggressive"

        if game_state[5] != 0 and game_state[6] == 0:
            comm_cards = [0, 0, 0, 0]
            for i, j in enumerate(game_state[2:6]):
                m, n = MyPlayer.get_rank_suit(j)
                comm_cards[i] = Card(rank=Rank(m), suit=Suit(n))
            
            my_result = HandEvaluator.evaluate_hand(self.hole_cards, comm_cards)

            if my_result.hand_rank.value >= 4:
                state = "aggressive"

            if my_result.hand_rank.value < 2:
                return PlayerAction.FOLD, 0
            elif my_result.hand_rank.value == 2:
                num = random.random()
                if num < 0.6:
                    return PlayerAction.FOLD, 0
                
            elif my_result.hand_rank.value == 3:
                if my_result.hand_value[0] >= 7:
                    pass
                else:
                    num = random.random()
                    if num < 0.7:
                        return PlayerAction.FOLD, 0
                    else:
                        return PlayerAction.CALL, (game_state[8] - self.bet_amount)

        if action_history:
            last_phase = action_history[-1][0]
            raise_counts = defaultdict(int)

            for phase, player, action, _ in action_history:
                if phase == last_phase and action == 'raise':
                    raise_counts[player] += 1

            players_with_raises_gt3 = [player for player, count in raise_counts.items() if count >= 2]
            if len(players_with_raises_gt3) >= 2:
                return PlayerAction.CALL, (game_state[8] - self.bet_amount)

        current_raise = game_state[8]
        if state == "normal":
            if self.stack > (current_raise + 40):
                return PlayerAction.RAISE, current_raise + 40
            return PlayerAction.ALL_IN, self.stack
        elif state == "aggressive":
            if self.stack > (current_raise + 60):
                return PlayerAction.RAISE, current_raise + 60
            return PlayerAction.ALL_IN, self.stack


    def estimate_win_rate(self, nb_simulations, game_state):
        win_count = sum([self.montecarlo_simulator(game_state) for _ in range(nb_simulations)])
        return win_count / nb_simulations
    
    def montecarlo_simulator(self, game_state):
        deck = range(1, 53)
        cards = game_state[:8]
        cards = [element for element in cards if element != 0]
        deck = list(set(deck) - set(cards))
        
        comm_cards_int = game_state[2:7]
        comm_cards = [0, 0, 0, 0, 0]
        for i, j in enumerate(comm_cards_int):
            if j == 0:
                card = random.choice(deck)
                m, n = MyPlayer.get_rank_suit(card)
                comm_cards[i] = Card(rank=Rank(m), suit=Suit(n))
                deck.remove(card)
            else:
                m, n = MyPlayer.get_rank_suit(comm_cards[i])
                comm_cards[i] = Card(rank=Rank(m), suit=Suit(n))

        opp_holes = []
        for i in range(game_state[11] - 1):
            card1 = random.choice(deck)
            deck.remove(card1)
            card2 = random.choice(deck)
            deck.remove(card2)

            k, j = MyPlayer.get_rank_suit(card1)
            card1 = Card(rank=Rank(k), suit=Suit(j))

            k, j = MyPlayer.get_rank_suit(card2)
            card2 = Card(rank=Rank(k), suit=Suit(j))

            opp_holes.append([card1, card2])

        opp_results = [HandEvaluator.evaluate_hand(i, comm_cards) for i in opp_holes]
        my_result = HandEvaluator.evaluate_hand(self.hole_cards, comm_cards)
        
        opp_results.sort(key=lambda x: (x.hand_rank.value, x.hand_value), reverse=True)
        if my_result.hand_rank.value > opp_results[0].hand_rank.value:
            return 1
        elif my_result.hand_rank.value == opp_results[0].hand_rank.value:
            if my_result.hand_value >= opp_results[0].hand_value:
                return 1
            else:
                return 0
        else:
            return 0 

    @staticmethod
    def get_rank_suit(card_idx):
        suit = (card_idx - 1) // 13
        rank = card_idx + 1 - (suit * 13)
        return rank, suit
