import random
from utils.utils import Logger


class BlackjackGame:
    """
    A Blackjack Simulator
    """
    def __init__(self, log_option="Print", auto_reset=True):
        # Initialize Logger
        self.logger = Logger(option=log_option, name="BlackJack Game Simulator")
        self.log = self.logger.log

        self.auto_reset = auto_reset

        self.__map = {"J": 10, "Q": 10, "K": 10, "A": 1}
        self._piles = None
        self.dealer_hand = None
        self.player_hand = None # except first A
        self.player_has_A = False
        self.reset()

    def _draw(self):
        return self._piles.pop()

    def _end(self, player_win=0):
        if player_win == 0:
            self.log("RESULT: Tie")
        elif player_win > 0:
            self.log("RESULT: Player wins")
        else:
            self.log("RESULT: Dealer wins")
        if self.auto_reset:
            self.reset()
        return player_win

    def reset(self):
        self._piles = [str(i) for i in range(2, 11)] * 4 + ["J", "Q", "K", "A"] * 4
        random.shuffle(self._piles)
        self.dealer_hand = []
        self.player_hand = []
        self.player_has_A = False
        self.log("Game Reset")
        # Dealer and player have 2 cards
        self.dealer_hand = [self._draw(), self._draw()]
        self.player_hand = []

        for i in range(2):
            card = self._draw()
            if card == "A" and not self.player_has_A:
                self.player_has_A = True
            else:
                self.player_hand.append(card)

        self.log("Observation:", self.observe())

        if self.count(self.player_hand) == 10 and self.player_has_A:
            self.log("Lucky Player Win! Next round!")
            self.reset()

    def count(self, hand):
        if hasattr(hand, "__iter__"):
            return sum(int(self.__map.get(x, x)) for x in hand)
        elif isinstance(hand, str):
            return int(self.__map.get(hand, hand))
        elif isinstance(hand, int):
            return hand
        else:
            error_message = f"count() got Unexpected input type: {type(hand)}"
            self.log(error_message)
            raise ValueError(error_message)

    def observe(self, end_mode=False):
        if not self.dealer_hand:
            self.log("Game not started")
            return None
        if end_mode:
            return {"dealer": self.dealer_hand, # Only in end mode, we can see dealer's full hand
                    "player": (["A"] + self.player_hand) if self.player_has_A else self.player_hand}
        else:
            return {"dealer": self.dealer_hand[0], "player": (["A"] + self.player_hand) if self.player_has_A else self.player_hand}

    def observe_state(self):
        return [self.dealer_hand[0], self.count(self.player_hand), int(self.player_has_A)]

    def hit(self):
        self.log("Player hits")
        card = self._draw()
        if card == "A" and not self.player_has_A:
            self.player_has_A = True
        else:
            self.player_hand.append(card)
        self.log("Observation:", self.observe())
        count_exclA = self.count(self.player_hand)

        if count_exclA + int(self.player_has_A) * 1 > 21:
            return self._end(player_win=-1)

        elif count_exclA + int(self.player_has_A) * 1 == 21 or count_exclA + int(self.player_has_A) * 11 == 21:
            return self.stand(player_has_21=True)
        else:
            return 0

    def stand(self, player_has_21=False):
        self.log("Player stands. Dealer start action.")
        dealer_count = self.count(self.dealer_hand)
        while dealer_count < 17:
            self.log("Observation:", self.observe(end_mode=True))
            self.dealer_hand.append(self._draw())
            dealer_count = self.count(self.dealer_hand)

        self.log("Final Observation:", self.observe(end_mode=True))

        # Counting player's hand
        if player_has_21:
            player_count = 21
        else:
            player_count_exclA = self.count(self.player_hand)
            # if self.player_has_A:
            #     if player_count_exclA <= 10:
            #         player_count = player_count_exclA + 11
            #     else:
            #         player_count = player_count_exclA + 1
            # else:
            #     player_count = player_count_exclA
            player_count = player_count_exclA if not self.player_has_A else player_count_exclA + (11 if player_count_exclA <= 10 else 1)

        self.log("Final Count:", {"dealer": dealer_count, "player": player_count})

        if player_count > 21: # We are not supposed to see this
            self.log("DEBUG - 'player_count > 21' should be handled in hit()")
            self.log("RESULT: Dealer wins")
            return -1
        else:
            if dealer_count > 21:
                self.log("RESULT: Player wins")
                return self._end(player_win=1)
            else:
                if dealer_count > player_count:
                    return self._end(player_win=-1)
                if player_count > dealer_count:
                    return self._end(player_win=1)
                else:
                    return self._end(player_win=0)


if __name__ == "__main__":
    game = BlackjackGame(log_option='Print')
    action_set = ["hit", "stand", "reset", "observe", "exit"]
    print("Player's Actions:", action_set)

    action = input()
    while action != "exit":
        while action not in action_set:
            print("Invalid Input! Please retry")
            action = input()
        eval(f"game.{action}()")
        action = input()
