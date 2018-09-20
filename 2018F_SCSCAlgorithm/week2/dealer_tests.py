import unittest

from card import Card
from dealer import Dealer


class DealerTest(unittest.TestCase):
    def setUp(self):
        suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
        ranks = ['Ace',
                 '2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'Jack', 'Queen', 'King']
        self.deck = list()
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def tearDown(self):
        del self.deck

    def test__create_deck(self):
        dealer = Dealer()
        deck = dealer._create_deck()
        self.assertEqual(self.deck, deck)

    def test_get_card(self):
        dealer = Dealer()
        for index in range(0, len(self.deck)):
            hand = dealer.get_card()
            self.assertIn(hand, self.deck)

    def test_get_values_k10(self):
        hands = [Card('Hearts', 'King'),
                 Card('Spades', '10')]
        dealer = Dealer()
        self.assertEqual(20, dealer.get_values(hands))

    def test_get_values_q08(self):
        hands = [Card('Diamonds', 'Queen'),
                 Card('Clubs', '8')]
        dealer = Dealer()
        self.assertEqual(18, dealer.get_values(hands))

    def test_get_values_aj10(self):
        hands = [Card('Spades', 'Jack'),
                 Card('Hearts', 'Ace'),
                 Card('Diamonds', '10')]
        dealer = Dealer()
        self.assertEqual(21, dealer.get_values(hands))

    def test_get_values_aa09(self):
        hands = [Card('Hearts', 'Ace'),
                 Card('Diamonds', 'Ace'),
                 Card('Clubs', '9')]
        dealer = Dealer()
        self.assertEqual(21, dealer.get_values(hands))

    def test_get_values_akqj(self):
        hands = [Card('Spades', 'Ace'),
                 Card('Hearts', 'King'),
                 Card('Diamonds', 'Queen'),
                 Card('Clubs', 'Jack')]
        dealer = Dealer()
        self.assertEqual(31, dealer.get_values(hands))


if __name__ == '__main__':
    unittest.main(verbosity=2)
