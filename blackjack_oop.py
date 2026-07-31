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

class Game:
    def __init__(self):
        self.money = 5000

    def start(self):
        while True:
            if self.money <= 0:
                print("You're broke!")
                break

            print(f"Money: {self.money}")
            bet = self.get_bet()

            deck = Deck()

            player = Hand()
            dealer = Hand()

            player.add_card(deck.draw())
            player.add_card(deck.draw())

            dealer.add_card(deck.draw())
            dealer.add_card(deck.draw())

            self.player_turn(player, dealer, deck, bet)
            self.dealer_turn(dealer, deck)

            self.resolve_round(player, dealer, bet)

    def player_turn(self, player, dealer, deck, bet):
        while True:
            print("Player:", player.value())

            if player.value() > 21:
                break

            move = input("(H)it or (S)tand: ").upper()

            if move == 'H':
                card = deck.draw()
                print(f"You drew {card}")
                player.add_card(card)
            elif move == 'S':
                break
            
    def dealer_turn(self, dealer, deck):
        while dealer.value() < 17:
            print("Dealer hits...")
            dealer.add_card(deck.draw())

    def resolve_round(self, player, dealer, bet):
        player_val = player.value()
        dealer_val = dealer.value()

        print(f"Player: {player_val} | Dealer: {dealer_val}")

        if dealer_val > 21 or player_val > dealer_val:
            print("You win!")
            self.money += bet
        elif player_val < dealer_val:
            print("You lose!")
            self.money -= bet
        else:
            print("Tie!")

if __name__ == "__main__":
    game = Game()
    game.start()