class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def value(self):
        value, aces = 0, 0

        for c in self.cards:
            if c.rank == 'A':
                aces += 1
            elif c.rank in ('K', 'Q', 'J'):
                value += 10
            else:
                value += int(c.rank)

        value += aces
        for _ in range(aces):
            if value + 10 <= 21:
                value += 10

        return value

class Player:
    def __init__(self, money):
        self.money = money
        self.hand = Hand()

    def bet(self, amount):
        if amount > self.money:
            raise ValueError("Not enough money")
        self.money -= amount
        return amount

class BlackjackRules:
    @staticmethod
    def is_bust(hand):
        return hand.value() > 21

    @staticmethod
    def dealer_should_hit(hand):
        return hand.value() < 17

    @staticmethod
    def compare(player_hand, dealer_hand):
        p = player_hand.value()
        d = dealer_hand.value()

        if p > 21:
            return "player_bust"
        if d > 21:
            return "dealer_bust"
        if p > d:
            return "player_win"
        if p < d:
            return "dealer_win"
        return "tie"

class GameService:
    def __init__(self, deck):
        self.deck = deck

    def initial_deal(self, player, dealer):
        for _ in range(2):
            player.hand.add(self.deck.draw())
            dealer.hand.add(self.deck.draw())

    def player_hit(self, player):
        player.hand.add(self.deck.draw())

    def dealer_play(self, dealer):
        while BlackjackRules.dealer_should_hit(dealer.hand):
            dealer.hand.add(self.deck.draw())