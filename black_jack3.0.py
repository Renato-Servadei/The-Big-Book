import random

class Deck:
    def __init__(self, cards=None):
        # Permite inyectar cartas (clave para testing)
        if cards is not None:
            self.cards = cards
        else:
            self.cards = self._build_standard_deck()
            self.shuffle()

    def _build_standard_deck(self):
        suits = ['♥', '♦', '♠', '♣']
        cards = []

        for suit in suits:
            for rank in range(2, 11):
                cards.append(Card(str(rank), suit))
            for rank in ('J', 'Q', 'K', 'A'):
                cards.append(Card(rank, suit))

        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop()
    
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

class ConsoleUI:
    def show_player(self, player):
        print("Player:", player.hand.value())

    def show_dealer(self, dealer, hide=False):
        if hide:
            print("Dealer: [hidden]")
        else:
            print("Dealer:", dealer.hand.value())

    def ask_move(self):
        return input("(H)it or (S)tand: ").upper()

    def ask_bet(self, money):
        return int(input(f"Bet (1-{money}): "))

def main():
    deck = Deck()
    player = Player(5000)
    dealer = Player(0)
    ui = ConsoleUI()
    service = GameService(deck)

    bet = ui.ask_bet(player.money)
    player.bet(bet)

    service.initial_deal(player, dealer)

    # Turno jugador
    while not BlackjackRules.is_bust(player.hand):
        ui.show_player(player)
        move = ui.ask_move()

        if move == 'H':
            service.player_hit(player)
        else:
            break

    # Turno dealer
    service.dealer_play(dealer)

    # Resultado
    result = BlackjackRules.compare(player.hand, dealer.hand)
    print("Result:", result)