import random
from collections import namedtuple
from helpers import *

PlayerHand = namedtuple('player_hand', 'name hand')
Card = namedtuple('card', 'rank suit')

suits = ['♠', '♦', '♥', '♣']
ranks = list(range(2, 11)) + ['J', 'Q', 'K', 'A']

deck = [Card(rank, suit) for suit in suits for rank in ranks]

del suits
del ranks

num_players = 0
while num_players < 1:
    num_players = int(input("How many players? "))  # should put in a try to handle poorly formatted responses
    if num_players < 1:
        print("The dealer can't play itself.")

decks_in_shoe = 7   # commonly played with 6 to 8 decks in a shoe

players = []
for i in range(num_players):
    while True:
        player_name = str(input("Input Player {}'s name: ".format(i+1)))
        if player_name == "Dealer":
            print("Player name cannot be 'Dealer' please try again")
        else:
            break
    players.append(PlayerHand(player_name, []))

# add dealer to the end of the player list (because the last card should be dealt to them)
players.append(PlayerHand("Dealer", []))
num_players += 1


while True:

    # shuffle a new shoe
    deck_shoe = []
    for _ in range(decks_in_shoe):
        deck_shoe.extend(random.sample(deck, 52))
    random.shuffle(deck_shoe)   # shuffles the entire shoe again so as to not have only shuffled decks stacked.
    print("\n<<<Shuffling Decks>>>\n", end='')
    index = 0

    # If there aren't enough cards to play a hand its time to shuffle the deck.
    while len(deck_shoe) > num_players*4:

        for _ in range(2):  # give each player 2 cards
            for player in range(num_players):     # give each player their cards in round robin fashion
                players[player].hand.append(deck_shoe.pop())

        # print table dealer card covered
        print_table(players)

        for player in players:
            if "Dealer" == player.name:
                while True:   # emulated do while loop
                    if hand_sum(player.hand) <= 16:
                        player.hand.append(deck_shoe.pop())
                    print_table(players, dealer_cover=False, print_sums=True)
                    if hand_sum(player.hand) >= 17:  # do while condition
                        break
            while not is_bust(player.hand) and "Dealer" != player.name:
                player_action = input("{}'s Turn: h = hit, s = stand, d = double down > ".format(player.name))
                if 's' == player_action:
                    break
                if 'h' == player_action or 'd' == player_action:
                    player.hand.append(deck_shoe.pop())
                print_table(players)

        print(Fore.YELLOW, "\nHand Complete   >   ", end='')

        dealer_sum = 0
        dealer_bust = False
        players_who_won = []

        for player in reversed(players):
            if "Dealer" == player.name:
                dealer_sum = hand_sum(player.hand)

                if is_bust(player.hand):   # doing in reverse order so Dealer should be first
                    dealer_bust = True
                else:
                    dealer_bust = False

            else:
                # this logic calls a push a win but I don't care.
                if not is_bust(player.hand) and (hand_sum(player.hand) >= dealer_sum or dealer_bust):
                    players_who_won.append(player.name)

        if players_who_won:
            num_winners = len(players_who_won)
            if num_winners == 1:
                print(players_who_won[0], end='')
            else:
                for name in players_who_won:
                    if 1 == num_winners:
                        print("and " + name, end='')
                    else:
                        print(name + ", ", end='')  # ends up putting a comma for only 2 winners but meh that's fine...
                        num_winners -= 1
            print(" won")
        else:
            print("Dealer won!")
        print(Style.RESET_ALL, end='')

        # clear the table
        for player in range(num_players):
            players[player].hand.clear()
