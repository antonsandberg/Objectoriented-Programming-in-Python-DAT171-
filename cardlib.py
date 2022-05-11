import random
from enum import IntEnum
from abc import ABC, abstractmethod
from collections import Counter


""" 
Assignment 2
Author: Anton Sandberg (2021) and Oliver Johansson (2021) 
antsandb@student.chalmers.se and olijoh@student.chalmers.se 
"""


def createtable(amount):
    """
    Creates a table with x amount of random PlayingCards for texas Hold'em

    :param amount: amount of cards wanted
    :return cards: returning a table with cards

    """

    cards = []
    for i in range(amount):
        cards.append(deck.card())
    return cards


class Suit(IntEnum):
    """
    Converts string suits to value
    """
    Hearts = 3
    Spades = 2
    Diamonds = 1
    Clubs = 0


class HandRanks(IntEnum):
    """
    Convert Handranks to values, which makes them comparable
    """
    Straight_flush = 10
    Fourofakind = 9
    Full_house = 8
    Flush = 7
    Straight = 6
    Threeofakind = 5
    Twopair = 4
    Pair = 3
    Highcard = 2


suits_symb = ["♣", "♦", "♠", "♥"]  # Unicode for suits symbols


class PlayingCard(ABC):
    """
    Class PlayingCard for creating a Card with inputs value, suit for numbered card and suit for J,Q,K,A*-
    """
    def __init__(self, suit):
        """
        Initializing the class with a suit
        """
        self.suit = suit

    @abstractmethod
    def get_value(self):
        """
        An abstract method to be able to be inherited by the different card classes
        """
        return self.value

    def __lt__(self, other):
        """
        Compare values, if values are the same, it compares suit
        """
        return (self.get_value(), self.suit) < (other.get_value(), other.suit)


    def __eq__(self, other):
        """
        Comparison if both values and suit are the same
        """
        return self.get_value() == other.get_value() and self.suit == other.suit



class NumberedCard(PlayingCard):
    """
    Creates a NumberedCard with a suit and value
    """

    def __init__(self, value, suit):
        """
        Initializing the class with a value and a suit

        """
        self.suit = suit
        self.value = value

    def get_value(self):
        """
        Extract the numbered card's value

        :return: self.value
        """
        return self.value

    def __str__(self):                  # Creating a str for Card to be able to be printed nicely
        """
        Creating a suitable string method for the card
        """
        s = suits_symb[self.suit]
        return str(self.value) + " " + s.replace("'", "")


class JackCard(PlayingCard):
    """
    Creates a JackCard with a suit
    """
    def get_value(self):
        """
        Extracts the value of the JackCard
        :return: 11
        """
        return 11

    def __str__(self):
        """
        Creating a suitable string method for the card
        """
        s = suits_symb[self.suit]
        return "J" + " " + s.replace("'", "")


class QueenCard(PlayingCard):
    """
    Creates a QueenCard with a suit
    """
    def get_value(self):
        """
        Extracts the value of the QueenCard

        :return: 12
        """
        return 12

    def __str__(self):
        """
        Creating a suitable string method for the card
        """
        s = suits_symb[self.suit]
        return "Q" + " " + s.replace("'", "")


class KingCard(PlayingCard):
    """
    Creates a KingCard with suit and value 13
    """
    def get_value(self):
        """
        Extracts the value of the KingCard

        :return: 13
        """
        return 13

    def __str__(self):              # Creating a str for Card to be able to be printed nicely
        """
        Creating a suitable string method for the card
        """
        s = suits_symb[self.suit]
        return "K"+" " + s.replace("'", "")


class AceCard(PlayingCard):
    """
    Creates an AceCard with suit and value 14
    """
    def get_value(self):
        """
        Extracts the value of the AceCard

        :return: 14
        """
        return 14

    def __str__(self):
        """
        Creating a suitable string method for the card
        """
        s = str(suits_symb[self.suit])
        return "A"+" " + s.replace("'", "")


class StandardDeck:
    """
    Creates a deck with 52 playing cards from numbers + J,Q,K,A in all 4 suits
    The deck has methods for shuffling itself and taking a card
    """
    def __init__(self):
        """
        Initializing the class, creates a list and builds the deck
        """
        self.cards = []
        self.build()

    def build(self):
        """
        Creates a complete deck of cards
        """
        numbers = range(2, 11)  # list with number 2-10

        for suit in Suit:
            for number in numbers:
                self.cards.append(NumberedCard(number, suit))
            for k in [JackCard, QueenCard, KingCard, AceCard]:
                self.cards.append(k(Suit(suit)))

    def __str__(self):
        """
        A method to be able to print the deck nicely
        """
        return " ".join(['[' + str(card) + ']' for card in self.cards])

    def shuffle(self):                  # Deck shuffle
        """
        A method to be able to shuffle the cards in the deck

        """
        for i in range(3):
            random.shuffle(self.cards)

    def card(self):
        """
        To be able to take the card "on top", takes furthest card in list

        :return: The deck without the last card
        """
        return self.cards.pop()

#    def discard(self, position_list):
#        """
#        A method to remove a number of cards by given positions

#        :param position_list: the positions of the cards to be discarded in a list format
#        """
#
#        for index in sorted(position_list, reverse=True):
#            del self.cards[index]


class Table:
    """
    Creates a table class to hold the cards needed to play the game
    """
    def __init__(self):
        """
        Initiating the class and creating an empty table
        """
        self.cards = []

    def new_card(self, card):
        """
        Add a card to the table

        :param card: card which to be added to the table
        :return: the table with the card added
        """
        self.table.append(card)


class Hand:
    """
    Creates a Hand for a player which can add cards, sort, discard and calculate best poker hand
    with cards on a potential table
    """
    def __init__(self, amount=None, table=None):

        """
        Initiating the class and creating empty variables

        """
        self.cards = []
        if amount is None:
            self.amount = 0
        if table is None:
            self.table = []

    def add_card(self, card):
        """
        Method to add a card to the hand

        :param card: The card to be added
        """
        self.cards.append(card)

    def __str__(self):
        """
        Layout for printing the Hand in a nice way

        :return: a nice string layout
        """
        return " ".join(['[' + str(card) + ']' for card in self.cards])

    def order(self):
        """
        A method to sort the cards in the hand
        """

        self.cards = sorted(self.cards, reverse=True) # <- kolla varför detta inte funkar key=lambda card: card.get_value()

    def discard(self, position_list):
        """
        A method to remove a number of cards by given positions

        :param position_list: the positions of the cards to be discarded in a list format
        """

        for index in sorted(position_list, reverse=True):
            del self.cards[index]


    def best_poker_hand(self, cards=[]):
        """
        Give a number of cards calculates the best possible hand available

        :param cards: all cards on the table
        :return: The highest pokerhand available
        """
        pokercards = cards + self.cards
        return PokerHand(pokercards)


class PokerHand:
    """
    PokerHand, can calculate all the available pokerhands with players' cards + table, returns the best
    available pokerhand for those cards with a pokerhand ranking and potential value + suit
    """

    @staticmethod
    def check_straight_flush(cards):
        """
        Goes through the cards and sees if there are 5 numbers in a row with the same suit

        :param cards: puts in the cards for potential pokerhands
        :return: HandRanks.Straight_Flush, it's number (10) and a list with the 5 highest cards
        """
        vals = [(c.get_value(), c.suit) for c in cards] + [(1, c.suit) for c in cards if c.get_value == 14]
        for c in reversed(cards):
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return [c.get_value(), c.get_value() - 1, c.get_value() - 2, c.get_value() - 3, c.get_value() - 4]

    @staticmethod
    def check_fourofakind(cards):
        """
        Counts among the cards to see if there are four of the same of any kind

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Fourofakind, it's value (9) and a list with the 5 highest cards
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        fours = [v[0] for v in count.items() if v[1] == 4]
        if len(fours) > 0:
            value = fours[0]
            vals = [c.get_value() for c in cards]
            vals.sort(reverse=True)
            for i in range(4):
                vals.remove(value)
            return [value, value, value, value, vals[0]]

    @staticmethod
    def check_full_house(cards):
        """
        Goes through the cards and looks for three of the same number and thereafter two of the same number
        Sorts the numbers in descending order to get highest pairs and thereafter checks to see if the
        three of a kind is unique to the pair.

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Full_house, it's value (8) and a list with two integers, first three of a kind then the pair
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()

        # Threes are dominant in full house, lets check that value first:
        for three in reversed(threes):
            for two in reversed(twos):
                if two != three:
                    return [three, three, three, two, two]

    @staticmethod
    def check_flush(cards):
        """
        Check among the cards if there are five cards of the same suit and if so sorts them in descending order
        so it can give you the highest value in the flush

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Flush, it's value (7) and a list with the 5 highest cards:
        """

        suits_count = Counter()
        for c in cards:
            suits_count[c.suit] += 1
        suits = [v[0] for v in suits_count.items() if v[1] >= 5]
        suits.sort(reverse=True)

        flush = []
        if len(suits) > 0:
            flush = suits[0]

        cards.sort(reverse=True)  # sorts the cards available to be able to return the highest card of the flush
        retlist = []
        i = 0
        for c in cards:
            if c.suit == flush and i < 5:
                retlist.append(c.get_value())
                i += 1
        if len(retlist) == 5:
            return retlist

    @staticmethod
    def check_straight(cards):
        """
        Goes through the cards to see if there are any 5 cards with values in a row

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Straight, it's value (6) and a list with the 5 highest cards
        """

        vals = [(c.get_value()) for c in cards] + [1 for c in cards if c.get_value == 14]
        for c in cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return [c.get_value(), c.get_value() - 1, c.get_value() - 2, c.get_value() - 3, c.get_value() - 4]

    @staticmethod
    def check_threeofakind(cards):
        """
        Counts through the cards to see if there are any cards with three of the same value

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Threeofakind, it's value (5) and a list with the 5 highest cards
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        threes = [v[0] for v in count.items() if v[1] == 3]
        if len(threes) > 0:
            value = max(threes)
            vals = [c.get_value() for c in cards]
            vals.sort(reverse=True)

            for i in range(3):
                vals.remove(value)

            return [value, value, value, vals[0], vals[1]]

    @staticmethod
    def check_twopair(cards):
        """
        Counts among the cards to see if there are any pair of cards
        Stores the pairs and thereafter returns the two highest pairs if there are two pairs in the list

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Twopair, it's value (4) and a list with the 5 highest cards
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        twopair = [v[0] for v in count.items() if v[1] == 2]
        if len(twopair) > 0:
            if len(twopair) >= 2:  # takes out the highest two pairs of all the available
                max1 = max(twopair)
                twopair.remove(max1)
                max2 = max(twopair)
                twopair.clear()
                twopair = [max1, max1, max2, max2]

                vals = [c.get_value() for c in cards]
                vals.sort(reverse=True)

                for i in range(2):
                    vals.remove(max1)
                    vals.remove(max2)
                twopair.append(vals[0])
                return twopair

    @staticmethod
    def check_pair(cards):
        """
        Counts among the cards to see if there are any pair of cards, stores all pairs

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Pair, it's value (3) and a list with the 5 highest cards
        """
        count = Counter()
        for c in cards:
            count[c.get_value()] += 1
        twos = [v[0] for v in count.items() if v[1] == 2]

        if len(twos) > 0:
            vals = [c.get_value() for c in cards]
            vals.sort(reverse=True)
            value = max(twos)

            for i in range(2):
                vals.remove(value)
            return [value, value, vals[0], vals[1], vals[2]]

    @staticmethod
    def check_highcard(cards):
        """
        Takes the value and suit of each card that is available and sorts them in descending order

        :param cards: Puts in the cards for potential pokerhands
        :return: HandRanks.Highcard, it's value (2) and a list with the 5 highest cards
        """
        vals = [c.get_value() for c in cards]
        vals.sort(reverse=True)
        return [vals[0], vals[1], vals[2], vals[3], vals[4]]

    def __init__(self, pokercards):
        super().__init__()
        """
        Initiating the class,

        :param pokercards: The cards to be evaluated
        """
        self.ranking = []
        self.cards = sorted(pokercards)

        if PokerHand.check_straight_flush(pokercards) is not None:
            value = PokerHand.check_straight_flush(pokercards)
            self.ranking = HandRanks.Straight_flush
            self.value = value

        elif PokerHand.check_fourofakind(pokercards) is not None:
            value = PokerHand.check_fourofakind(pokercards)
            self.ranking = HandRanks.Fourofakind
            self.value = value

        elif PokerHand.check_full_house(pokercards) is not None:
            value = PokerHand.check_full_house(pokercards)
            self.ranking = HandRanks.Full_house
            self.value = value

        elif PokerHand.check_flush(pokercards) is not None:
            value = PokerHand.check_flush(pokercards)
            self.ranking = HandRanks.Flush
            self.value = value

        elif PokerHand.check_straight(pokercards) is not None:
            value = PokerHand.check_straight(pokercards)
            self.ranking = HandRanks.Straight
            self.value = value

        elif PokerHand.check_threeofakind(pokercards) is not None:
            value = PokerHand.check_threeofakind(pokercards)
            self.ranking = HandRanks.Threeofakind
            self.value = value

        elif PokerHand.check_twopair(pokercards) is not None:
            value = PokerHand.check_twopair(pokercards)
            self.ranking = HandRanks.Twopair
            self.value = value

        elif PokerHand.check_pair(pokercards) is not None:
            value = PokerHand.check_pair(pokercards)
            self.ranking = HandRanks.Pair
            self.value = value

        else:
            value = PokerHand.check_highcard(pokercards)
            self.ranking = HandRanks.Highcard
            self.value = value

    def __str__(self):
        """
        Layout for printing the Hand in a nice way

        :return: a nice string layout
        """
        results = ["High card", "Pair", "Two pair",
                   "Three of a kind", "Straight",
                   "Flush", "Full house",
                   "Four of a kind", "Straight flush"]

        return "Player has: {} of cards: {}".format(results[self.ranking-2], " ".join(['[' + str(card) + ']' for card in self.cards]))

    def __lt__(self, other):
        """
        Comparison of the HandRank and the values of the cards, if the hand is better
        than the other

        :return: True or False
        """
        return (self.ranking, self.value) < (other.ranking, other.value)

    def __eq__(self, other):
        """
        Comparison of the HandRank and the values of the cards, if the hands are the same

        :return: True or False
        """
        return (self.ranking, self.value) == (other.ranking, other.value)


if __name__ == '__main__':

    deck = StandardDeck()
    deck.shuffle()
    table = createtable(5)
    print(" ".join(['[' + str(card) + ']' for card in table]))
    print("--------")
    hand1 = Hand()
    hand2 = Hand()


    for i in range(2):
        hand1.add_card(deck.card())
        hand2.add_card(deck.card())

    x = hand1.best_poker_hand(table)
    y = hand2.best_poker_hand(table)
    print(x.ranking)
    print(x.value)
    print(x)
    print("--------")
    print(y.ranking)
    print(y.value)
    print(y)

    cards = [NumberedCard(6, Suit.Hearts), AceCard(Suit.Hearts)]
    h1 = Hand()
    h1.add_card(cards)
    print(h1)
    h1.order()
    print(h1)