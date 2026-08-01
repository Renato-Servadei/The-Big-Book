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