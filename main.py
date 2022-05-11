from pokerview import *
from pokermodel import *
import sys

""" 
Assignment 3
Author: Anton Sandberg (2021) and Oliver Johansson (2021) 
antsandb@student.chalmers.se and olijoh@student.chalmers.se 
"""

app = QApplication(sys.argv)
gamestate = PokerGame(['Oliver','Anton'], 2000)
gui = PokerTable(gamestate)
gui.show()
app.exec_()