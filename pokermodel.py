from PyQt5.QtCore import *
from cardlib import *
from abc import abstractmethod

""" 
Assignment 3
Author: Anton Sandberg (2021) and Oliver Johansson (2021) 
antsandb@student.chalmers.se and olijoh@student.chalmers.se 
"""

class CardModel(QObject):
    """
    Base class that described what is expected from the CardView widget
    """

    new_cards = pyqtSignal()  # Signal to pokerview

    @abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""

class Player(QObject):
    """
    Class for a player:
    holds their name, money, hand and their bets
    """
    new_player_money = pyqtSignal()  # Signal to pokerview

    def __init__(self, name, money):
        super().__init__()


        self.name = name
        self.money = money
        self.bet_amount = 0
        self.hand = HandModel()

    def winner(self, amount):
        self.money += amount
        self.bet_amount = 0
        self.new_player_money.emit()

    def bet(self, amount):
        self.money -= amount
        self.bet_amount += amount
        self.new_player_money.emit()

    def reset_bet(self):
        self.bet_amount = 0
        self.new_player_money.emit()


class Pot(QObject):
    """
    Class for the pot:
    contains the pot and some simple methods
    """
    new_pot = pyqtSignal()  # Signal to pokerview

    def __init__(self):
        super().__init__()
        self.money = 0

    def clear(self):
        self.money = 0
        self.new_pot.emit()

    def __add__(self, amount):
        self.money += amount
        self.new_pot.emit()


class TableClass(Table, CardModel):
    """
    Class for the table:
    holding the cards, clearing and adding cards
    """
    def __init__(self):
        super().__init__()
        Table.__init__(self)
        CardModel.__init__(self)

    def clear(self):
        self.cards.clear()
        self.new_cards.emit()   # new_cards signal is defined in pokerview

    def deal_card(self, cards):
        self.cards.append(cards)
        self.new_cards.emit()

    def __iter__(self):
        return iter(self.cards)

class HandModel(Hand, CardModel):
    """
    Class for the hand:
    flipping cards, aswell as adding two new cards at the start of a round
    """
    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)

        # Additional state needed by the UI
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!



class PokerGame(QObject):

    quit_signal = pyqtSignal()  # Signals to pokerview
    player_turn = pyqtSignal()
    last_winner = pyqtSignal()

    def __init__(self, players, money):
        super().__init__()
        # Initialising with some useful variables
        self.players = [Player(players[0], money), Player(players[1], money)]
        self.pot = Pot()
        self.recent_bet = 0
        self.deck = None
        self.table = TableClass()
        self.round = 0
        self.current_player = 0
        self.last_better = False
        self.bet_this_round = 0
        self.winning_player = 0
        self.all_in_variable = 0

        self.new_round()

    def next_player(self):
        """ Method for changing the active player """
        self.current_player = (1 + self.current_player) % 2
        self.player_turn.emit()



    def new_round(self):
        """ Method for starting a new round """
        for player in self.players:
            if player.money == 0:
                self.quit_signal.emit()

        self.round += 1
        self.recent_bet = 0
        self.pot.clear()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.last_better = False

        for player in self.players:
            player.hand.cards.clear()
            for i in range(2):
                card = self.deck.card()
                player.hand.add_card(card)
            player.hand.flipped_cards = True

        self.table.clear()

    def check(self):
        """ Method for checking depending on situation """
        # If you're the first checker
        if self.recent_bet == 0 and not self.last_better:
            self.last_better = True
            self.next_player()

        # If you're the second checker
        elif self.recent_bet == 0:
            self.last_better = False
            self.next_player()
            self.add_card()

    def call(self):
        """ Method for calling the other players raise """
        if self.recent_bet != 0 and self.last_better:
            self.bet(self.recent_bet)
            if self.all_in_variable == 1:
                self.fill_table()

    def bet(self, amount):
        """
        Method for betting depending on situation:

        :param amount: the amount of money that the player wants to bet, typed into the bet window """
        self.players[self.current_player].bet(amount)
        self.pot.__add__(amount)

        # If you're the first raiser
        if self.recent_bet == 0:
            self.recent_bet = amount
            self.last_better = True

        # If you're counter raising
        elif self.recent_bet < amount:
            self.recent_bet = amount-self.recent_bet
            self.last_better = True

        # If you're calling with the bet button
        elif self.recent_bet == amount:
            self.add_card()

        self.next_player()

    def fold(self):
        """
        Method for folding:
        gives the other player the win and starts a new round
        """
        self.winning_player = (self.current_player + 1) % 2
        self.players[self.winning_player].winner(self.pot.money)
        self.new_round()
        self.next_player()
        self.last_winner.emit()

    def all_in(self):
        """ Method when a player goes all in """
        maxbet = min(self.players[0].money, self.players[1].money)
        # If you're the second better
        if self.last_better:
            self.bet(maxbet)
        else:
            # If you're the first better
            self.bet(maxbet)
            self.last_better = True

        self.all_in_variable = 1

    def check_winner(self):
        """Method for deciding winner and providing the pot"""
        # Checks both players current hand
        best_current_hand = self.players[self.current_player].hand.best_poker_hand(self.table.cards)
        best_other_hand = self.players[(self.current_player + 1) % 2].hand.best_poker_hand(self.table.cards)


        if best_current_hand > best_other_hand:
            self.winning_hand = best_current_hand
            self.winning_player = self.current_player
        else:
            self.winning_hand = best_other_hand
            self.winning_player = (self.current_player + 1) % 2

        # Handing out the price money and displaying winner
        self.players[self.winning_player].winner(self.pot.money)
        self.last_winner.emit()

    def add_card(self):
        """
        Method for adding /a cards/card to the table
        """
        # Removes the top card from the deck before adding to the table
        self.deck.card()

        # flop
        if len(self.table.cards) == 0:
            for i in range(3):
                card = self.deck.card()
                self.table.deal_card(card)

        # turn and river
        elif len(self.table.cards) == 3 or len(self.table.cards) == 4:
            card = self.deck.card()
            self.table.deal_card(card)

        # 5 cards are out, time to decide a winner
        else:
            self.check_winner()
            self.next_player()
            self.new_round()

        self.last_better = False
        self.recent_bet = 0
        for player in self.players:
            player.reset_bet()

    def fill_table(self):
        """ Method when one player wen't all and the other player called """
        cards_left = 5 - len(self.table.cards)
        # Dealing out the remaining cards
        for i in range(cards_left):
            card = self.deck.card()
            self.table.deal_card(card)

        self.check_winner()
        self.next_player()
        self.new_round()

