import pytest
from cardlib import *



def test_cards():
    assert NumberedCard(10, Suit.Diamonds).suit == Suit.Diamonds
    assert NumberedCard(10, Suit.Diamonds).value == 10
    assert JackCard(Suit.Hearts).get_value() == 11
    assert JackCard(Suit.Hearts).suit == Suit.Hearts
    assert AceCard(Suit.Spades).get_value() == 14
    assert AceCard(Suit.Spades).suit == Suit.Spades



def test_standarddeck():
    deck = StandardDeck()
    assert len(deck.cards) == 52
    deck = StandardDeck()
    hand = Hand()

    hand.add_card(deck.card())
    assert len(hand.cards) == 1
    assert len(deck.cards) == 51
    try:
        for i in range(52):
            hand.add_card(deck.card())
    except IndexError:
        print("The deck is empty!")

    deck = StandardDeck()
    card1 = deck.card()
    card2 = deck.card()
    assert card1 == AceCard(Suit.Clubs) and card2 == KingCard(Suit.Clubs)
    assert not card1 == card2

def test_table():
    deck = StandardDeck()
    deck.shuffle()
    table = Table()

    for i in range(5):
        table.new_card(deck.card())

    assert len(table.cards) == 5




def test_hand():
    deck = StandardDeck()
    hand = Hand()
    hand.add_card(deck.card())

    assert len(hand.cards) == 1
    hand.discard([0])

    assert len(hand.cards) == 0
    try:
        hand.discard([0])
    except IndexError:
        print("The hand is empty or the index is out of range!")

    cards = [NumberedCard(6, Suit.Clubs), NumberedCard(7, Suit.Diamonds), NumberedCard(8, Suit.Hearts),
                     NumberedCard(9, Suit.Clubs), KingCard(Suit.Spades)]
    h1 = Hand()
    for card in cards:
        h1.add_card(card)
    h1.order_value()
    assert h1.cards == [KingCard(Suit.Spades), NumberedCard(9, Suit.Clubs), NumberedCard(8, Suit.Hearts),
                  NumberedCard(7, Suit.Diamonds), NumberedCard(6, Suit.Clubs)]
    h1.order_suit()
    assert h1.cards == [NumberedCard(8, Suit.Hearts), KingCard(Suit.Spades), NumberedCard(7, Suit.Diamonds),
                        NumberedCard(9, Suit.Clubs), NumberedCard(6, Suit.Clubs)]



def test_pokerhand():
    cards_highcard = [NumberedCard(9, Suit.Hearts), NumberedCard(9, Suit.Clubs), KingCard(Suit.Spades),
                      NumberedCard(4, Suit.Hearts), NumberedCard(5, Suit.Clubs)]
    highcard = PokerHand.check_highcard(cards_highcard)

    assert highcard[0] == 13 and highcard[1] == 9 and highcard[2] == 9

    cards_pair = [JackCard(Suit.Hearts), JackCard(Suit.Diamonds), NumberedCard(10, Suit.Spades),
                  NumberedCard(4, Suit.Hearts), NumberedCard(5, Suit.Clubs), NumberedCard(2, Suit.Clubs)]
    pair = PokerHand.check_pair(cards_pair)

    assert pair == [11, 11, 10, 5, 4]

    cards_twopair = [NumberedCard(7, Suit.Clubs), NumberedCard(7, Suit.Diamonds), NumberedCard(8, Suit.Hearts),
                     NumberedCard(8, Suit.Clubs), KingCard(Suit.Spades)]
    twopair = PokerHand.check_twopair(cards_twopair)

    assert twopair == [8, 8, 7, 7, 13]

    cards_threeofakind = [NumberedCard(8, Suit.Hearts), NumberedCard(9, Suit.Clubs), QueenCard(Suit.Spades),
                          QueenCard(Suit.Hearts), QueenCard(Suit.Diamonds)]
    threeofakind = PokerHand.check_threeofakind(cards_threeofakind)

    assert threeofakind == [12, 12, 12, 9, 8]

    cards_fourofakind = [NumberedCard(9, Suit.Hearts), NumberedCard(9, Suit.Clubs), QueenCard(Suit.Spades),
                         QueenCard(Suit.Hearts), QueenCard(Suit.Diamonds), QueenCard(Suit.Clubs)]
    fourofakind = PokerHand.check_fourofakind(cards_fourofakind)

    assert fourofakind == [12, 12, 12, 12, 9]

    cards_straight = [NumberedCard(9, Suit.Hearts), NumberedCard(10, Suit.Clubs), QueenCard(Suit.Spades),
                      JackCard(Suit.Spades), NumberedCard(8, Suit.Hearts), AceCard(Suit.Clubs)]
    straight = PokerHand.check_straight(cards_straight)

    assert straight == [12, 11, 10, 9, 8]

    cards_flush = [NumberedCard(9, Suit.Hearts), NumberedCard(9, Suit.Spades), QueenCard(Suit.Spades),
                   QueenCard(Suit.Hearts), AceCard(Suit.Diamonds), NumberedCard(2, Suit.Spades),
                   NumberedCard(4, Suit.Spades), NumberedCard(5, Suit.Spades)]
    flush = PokerHand.check_flush(cards_flush)

    assert flush == [12, 9, 5, 4, 2]  # highest card is Queen in flush so it goes first and in order

    cards_fullhouse = [NumberedCard(9, Suit.Hearts), NumberedCard(9, Suit.Clubs), QueenCard(Suit.Spades),
                       QueenCard(Suit.Hearts), QueenCard(Suit.Diamonds), AceCard(Suit.Spades)]
    fullhouse = PokerHand.check_full_house(cards_fullhouse)

    assert fullhouse[0] == 12 and fullhouse[3] == 9   # three of queen [0-2] and two of nines [3-4]

    cards_straightflush = [NumberedCard(8, Suit.Hearts), NumberedCard(9, Suit.Hearts), QueenCard(Suit.Hearts), NumberedCard(10, Suit.Hearts),
                        JackCard(Suit.Hearts), AceCard(Suit.Spades)]
    straightflush = PokerHand.check_straight_flush(cards_straightflush)

    assert straightflush == [12, 11, 10, 9, 8]        # highest card in straightflush is queen of hearts

    cards = [NumberedCard(9, Suit.Hearts), NumberedCard(8, Suit.Clubs), QueenCard(Suit.Spades), QueenCard(Suit.Hearts),
          QueenCard(Suit.Diamonds), JackCard(Suit.Hearts), AceCard(Suit.Spades)]
    pokerhand = PokerHand(cards)

    assert pokerhand.ranking == 5 and pokerhand.value[0] == 12 # threeofakind ranking is 5 and queen is value 12

    PlayerHand1 = PokerHand(cards_pair)
    PlayerHand2 = PokerHand(cards_twopair)
    PlayerHand3 = PokerHand(cards_threeofakind)
    PlayerHand4 = PokerHand(cards_straight)
    PlayerHand5 = PokerHand(cards_flush)
    PlayerHand6 = PokerHand(cards_fullhouse)
    PlayerHand7 = PokerHand(cards_fourofakind)
    PlayerHand8 = PokerHand(cards_straightflush)

    assert PlayerHand2 > PlayerHand1 and PlayerHand4 > PlayerHand3 and PlayerHand6 > PlayerHand5 and PlayerHand8 > PlayerHand7