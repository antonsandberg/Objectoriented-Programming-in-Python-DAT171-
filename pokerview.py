from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from cardlib import *

""" 
Assignment 3
Author: Anton Sandberg (2021) and Oliver Johansson (2021) 
antsandb@student.chalmers.se and olijoh@student.chalmers.se 
"""


class PlayerInfo(QVBoxLayout):
    """ Class for displaying all the player information """
    def __init__(self, players, model):
        super().__init__()

        self.model = model
        self.players = players
        name = QLabel("{}".format(self.players.name))
        self.money = QLabel("{}".format(self.players.money))
        self.bet = QLabel("{}".format(self.players.bet_amount))
        flip = QPushButton("Show Cards")

        flip.clicked.connect(self.flip_cards)
        self.players.new_player_money.connect(self.update_money)
        self.players.new_player_money.connect(self.update_bet)

        self.addWidget(name)
        self.addWidget(self.money)
        self.addWidget(self.bet)
        self.addWidget(flip)

    def flip_cards(self):
        """ Method for flipping the cards """
        self.players.hand.flip()

    def update_money(self):
        """ Method for updating both players money """
        self.money.setText("{}".format(self.players.money))

    def update_bet(self):
        """ Method for updating the bet players currently have """
        self.bet.setText("{} bets {}".format(self.players.name, self.players.bet_amount))


class TableInfo(QVBoxLayout):
    """ Class for displaying all the table information """
    def __init__(self, model):
        super().__init__()

        self.model = model
        self.model.player_turn.connect(self.UpdateTurn)
        self.model.last_winner.connect(self.UpdateWinner)

        button_window = QFormLayout()
        turn_and_winner = QVBoxLayout()

        pot_display = PotValue(self.model.pot)

        self.bet_amount = BetAmount(self.model.players[self.model.current_player].money)

        bet_button = QPushButton("Bet")
        fold_button = QPushButton("Fold")
        check_button = QPushButton("Check")
        call_button = QPushButton("Call")
        all_in_button = QPushButton("All in")

        bet_button.clicked.connect(self.Bet)
        fold_button.clicked.connect(self.model.fold)
        check_button.clicked.connect(self.model.check)
        call_button.clicked.connect(self.model.call)
        all_in_button.clicked.connect(self.model.all_in)

        button_window.addWidget(pot_display)
        button_window.addWidget(bet_button)
        button_window.addWidget(self.bet_amount)
        button_window.addWidget(fold_button)
        button_window.addWidget(check_button)
        button_window.addWidget(call_button)
        button_window.addWidget(all_in_button)

        self.turn_text = QLabel("{}'s Turn".format(self.model.players[self.model.current_player].name))
        self.winner_text = QLabel("TBD")

        turn_and_winner.addWidget(self.winner_text)
        turn_and_winner.addWidget(self.turn_text)

        self.addLayout(turn_and_winner)
        self.addLayout(button_window)

        self.close = closeEvent(self.model)
        self.model.quit_signal.connect(self.close.quit)

    def Bet(self):
        if self.bet_amount.value() < self.model.recent_bet:
            pass
        elif self.bet_amount.value() > self.model.players[self.model.current_player].money:
            pass
        else:
            placed_bet = self.bet_amount.value()
            self.model.bet(placed_bet)

    def UpdateTurn(self):
        """ Method for updating which player's turn it is"""
        self.turn_text.setText("{}'s Turn".format(self.model.players[self.model.current_player].name))

    def UpdateWinner(self):
        """ Method for updating the winning player """
        self.winner_text.setText("{}'s Won Last Round".format(self.model.players[self.model.winning_player].name))


class closeEvent(QMessageBox):
    """ Class for letting the players end the game if a winner was decided """
    def __init__(self, model):
        super().__init__()
        self.model = model
    def quit(self):
        msg = "{} Won this game, would you like to exit?".format(self.model.players[self.model.winning_player].name)
        reply = self.question(self, "Poker Texas Hold'em", msg, self.Yes, self.No)

        if reply == self.Yes:
            self.model.end_game()
        else:
            pass

class BetAmount(QSpinBox):
    def __init__(self, maxbet):
        super().__init__()
        self.setMaximum(maxbet)

class PotValue(QLabel):
    def __init__(self, pot):
        super().__init__()
        self.pot = pot
        pot.new_pot.connect(self.UpdatePot)

    def UpdatePot(self):
        self.setText("Pot: {}".format(self.pot.money))


class PlayerView(QHBoxLayout):
    """ Class for displaying the player information """
    def __init__(self, players, playerinfo):
        super().__init__()
        self.player_cards = players.hand
        self.view = CardView(self.player_cards)

        self.addWidget(self.view)
        self.addLayout(playerinfo)


class TableView(QHBoxLayout):
    """ Class for displaying the table information """
    def __init__(self, model, tableinfo):
        super().__init__()
        self.table = model.table
        self.view = CardView(self.table)
        self.addWidget(self.view)
        self.addLayout(tableinfo)


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    for suit_file, suit in zip('HDSC', range(4)):  # Check the order of the suits here!!!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit_file
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: [], card_spacing: int = 250, padding: int = 10):
        """
        Initializes the view to display the content of the given model
        :param cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.model = card_model
        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        # The view can listen to changes:
        card_model.new_cards.connect(self.change_cards)

        # Add the cards the first time around to represent the initial state.
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit)
            renderer = self.back_card if self.model.flipped() else self.all_cards[graphics_key]
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)

            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height()-2*self.padding)/313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding//scale, -self.padding//scale,
                          self.viewport().width()//scale, self.viewport().height()//scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)

    def mouseDoubleClickEvent(self, event):
        self.model.flip()  # Another possible event. Lets add it to the flip functionality for fun!


class PokerTable(QMainWindow):
    """
    This class binds together all the other classes and creates a window where you can play poker against 1 person
    This class is connected to the pokermodel
    """
    def __init__(self, gamestate):
        super().__init__()
        self.model = gamestate

        self.centralwidget = QWidget()
        desktop = QDesktopWidget()
        size = desktop.availableGeometry(desktop.primaryScreen())
        height = int(size.height())
        width = int(size.width())
        self.setMinimumSize(int(width * 0.8), int(height * 0.7))

        player_info = [PlayerInfo(player, self.model) for player in self.model.players]
        players = [PlayerView(player, info) for player, info in zip(self.model.players, player_info)]

        tableinfo = TableInfo(self.model)
        table_overview = TableView(self.model, tableinfo)

        player_overview = QHBoxLayout()
        player_overview.addLayout(players[0])
        player_overview.addLayout(players[1])

        overview = QVBoxLayout()
        overview.addLayout(table_overview)
        overview.addLayout(player_overview)

        self.centralwidget.setLayout(overview)
        self.setCentralWidget(self.centralwidget)
