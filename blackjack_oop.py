import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        suits = ['♥', '♦', '♠', '♣']
        for suit in suits:
            for rank in range(2, 11):
                self.cards.append(Card(str(rank), suit))
            for rank in ('J', 'Q', 'K', 'A'):
                self.cards.append(Card(rank, suit))
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        value = 0
        aces = 0

        for card in self.cards:
            if card.rank == 'A':
                aces += 1
            elif card.rank in ('K', 'Q', 'J'):
                value += 10
            else:
                value += int(card.rank)

        value += aces
        for _ in range(aces):
            if value + 10 <= 21:
                value += 10

        return value