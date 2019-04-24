from colorama import Fore, Style


def print_table(players, dealer_cover=True, print_sums=False, add_blank=True):
    if dealer_cover:
        card_burned = False
    else:
        card_burned = True  # just tell the logic that a card has already been burnt

    if add_blank:
        print()   # start by adding one blank line

    for player in players:
        if "Dealer" == player.name:
            print()   # Add an extra line before the dealer to separate it from the players
        print(player.name, ":", end='', sep='')

        for card in player.hand:
            if "Dealer" == player.name and not card_burned:
                print('XX', sep='', end=' ')
                card_burned = True
            else:
                print(card.rank, card.suit, sep='', end=' ')

        if is_bust(player.hand):
            print(Fore.RED + "\t(Busted)", end='')
            print(Style.RESET_ALL, end='')
        if not is_bust(player.hand) and print_sums:
            print("\t\t-> {}".format(hand_sum(player.hand)), end='')
        print()


def hand_sum(hand):
    sum_ = 0
    aces_11 = 0
    ace_in_hand = False
    for card in hand:
        if isinstance(card.rank, int):
            sum_ += card.rank
        elif 'A' == card.rank:
            aces_11 += 1
            sum_ += 11
        else:
            sum_ += 10
    while sum_ > 21 and aces_11 > 0:
        sum_ -= 10
        aces_11 -= 1
    return sum_


def is_bust(hand):
    return hand_sum(hand) > 21
