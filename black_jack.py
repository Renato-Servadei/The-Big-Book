import random, sys

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = 'backside'

def main():
    print('''
    Rules:
    Try to get as close to 21 without going over. 
    Kings, Queens, and Jacks are worth 10 points. 
    Aces are worth 1 or 11 points. 
    Cards 2 through 10 are worth their face value. 
    (H)it to take another card. 
    (S)tand to stop taking cards. 
    On your first play, you can (D)ouble down to increase your bet 
    but must hit exactly one more time before standing. 
    In case of a tie, the bet is returned to the player. 
    The dealer stops hitting at 17.''')

    money = 5000
# Main game loop.
    while True:  
# Check if the player has run out of money:
        if money <= 0:
            print('You\'re broke!')
            print("Good thing you weren't playing with real money.")
            print('Thanks for playing!')
            sys.exit()

#let the player enter the bet for this round.
        print('Money: ', money)
        bet = getBet(money)

# Give the dealer and player two cards from the deck each:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

#Handle player actions
        print('Bet: ', bet)
# Keep looping until player stands or busts.
        while True:
            displayHands(dealerHand, playerHand, False)
            print()
#Check if the player has bust
            if getHandValue(playerHand) > 21:
                break
# Get the player's move, either H, S, or D:
            move = getMove(playerHand, money - bet)

#Handle the player actions
    # Player is doubling down, they can increase their bet:
            if move == 'D':
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}'.format(bet))
                print('Bet: ', bet)
    # Hit/doubling down takes another card.
            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)
#The player has busted
                if getHandValue(playerHand) > 21:
                    continue
# Stand/doubling down stops the player's turn.
            if move in ('S', 'D'):
                break
# Handle the dealer's actions: 
        if getHandValue(playerHand) <= 21: 
# The dealer hits:
            while getHandValue(dealerHand) < 17: 
                print('Dealer hits...') 
                dealerHand.append(deck.pop()) 
                displayHands(playerHand, dealerHand, False) 
# The dealer has busted.
                if getHandValue(dealerHand) > 21: 
                    break 
                input('Press Enter to continue...')
                print('\n\n')
#Show the final hands
        displayHands(playerHand, dealerHand, True) 
        playerValue = getHandValue(playerHand) 
        dealerValue = getHandValue(dealerHand) 
# Handle whether the player won, lost, or tied: 
        if dealerValue > 21: 
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet 
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('It\'s a tie, the bet is returned to you.')
            input('Press Enter to continue...')
            print('\n\n')

#Ask the player how much they want to bet for this round
def getBet(maxBet):
    while True:
        print('How much do you bet? (1 - {} or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet
        
#Return a list of (rank, suit) tuples for all 52 cards
def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
        random.shuffle(deck)
        return deck

#Show the player's and dealer's cards
def displayHands():
    print()

    if showDealerHand:
        print('Dealer: ???', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
#Hide the dealer's first card
        print('Dealer: ???')
        displayCards([BACKSIDE] + dealerHand[:1])
#Show the player's cards
    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)

#Return the value of the cards
def getHandValue(cards):
    value = 0
    numberOfAces = 0
#Add the value for non-ace cards
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)
#Add the value for the Aces
    value += numberOfAces
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10
    return value    

def getMove():
    pass