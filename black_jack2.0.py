import random
import sys

# =======================
# Card
# =======================
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# =======================
# Deck
# =======================
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


# =======================
# Hand
# =======================
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

    def display(self, hide_first=False):
        if hide_first:
            print("Dealer: [Hidden],", self.cards[1])
        else:
            print("Dealer:", ", ".join(str(c) for c in self.cards), f"({self.value()})")


# =======================
# Game
# =======================
class Game:
    def __init__(self):
        self.money = 5000

    def start(self):
        print("""
Rules:
Try to get as close to 21 without going over.
Face cards are worth 10. Aces are 1 or 11.
(H)it, (S)tand.
Dealer hits until 17.
""")

        while True:
            if self.money <= 0:
                print("You're broke!")
                break

            print(f"\nMoney: {self.money}")
            bet = self.get_bet()

            deck = Deck()
            player = Hand()
            dealer = Hand()

            # Initial deal
            for _ in range(2):
                player.add_card(deck.draw())
                dealer.add_card(deck.draw())

            # Player turn
            if not self.player_turn(player, dealer, deck):
                self.resolve_round(player, dealer, bet)
                continue

            # Dealer turn
            self.dealer_turn(dealer, deck)

            # Final result
            self.resolve_round(player, dealer, bet)

    # -----------------------
    # Player turn
    # -----------------------
    def player_turn(self, player, dealer, deck):
        while True:
            print("\nDealer shows:", dealer.cards[1])
            print("Player:", ", ".join(str(c) for c in player.cards), f"({player.value()})")

            if player.value() > 21:
                return False  # bust

            move = input("(H)it or (S)tand: ").upper()

            if move == 'H':
                card = deck.draw()
                print(f"You drew {card}")
                player.add_card(card)
            elif move == 'S':
                return True

    # -----------------------
    # Dealer turn
    # -----------------------
    def dealer_turn(self, dealer, deck):
        print("\nDealer's turn:")
        while dealer.value() < 17:
            card = deck.draw()
            print(f"Dealer draws {card}")
            dealer.add_card(card)

        print("Dealer stands with", dealer.value())

    # -----------------------
    # Resolve round
    # -----------------------
    def resolve_round(self, player, dealer, bet):
        player_val = player.value()
        dealer_val = dealer.value()

        print("\nFinal Hands:")
        print("Player:", ", ".join(str(c) for c in player.cards), f"({player_val})")
        print("Dealer:", ", ".join(str(c) for c in dealer.cards), f"({dealer_val})")

        # ✔ Lógica correcta
        if player_val > 21:
            print("You busted! You lose.")
            self.money -= bet

        elif dealer_val > 21:
            print("Dealer busts! You win!")
            self.money += bet

        elif player_val > dealer_val:
            print("You win!")
            self.money += bet

        elif player_val < dealer_val:
            print("You lose!")
            self.money -= bet

        else:
            print("It's a tie!")

    # -----------------------
    # Bet
    # -----------------------
    def get_bet(self):
        while True:
            bet = input(f"Bet amount (1 - {self.money} or QUIT): ").upper()

            if bet == "QUIT":
                print("Thanks for playing!")
                sys.exit()

            if not bet.isdecimal():
                print("Enter a valid number.")
                continue

            bet = int(bet)

            if 1 <= bet <= self.money:
                return bet


# =======================
# Entry point
# =======================
if __name__ == "__main__":
    game = Game()
    game.start()