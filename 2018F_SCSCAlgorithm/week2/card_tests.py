import unittest

from card import Card


class CardTest(unittest.TestCase):
    def test_create(self):
        suit = 'Hearts'
        rank = 'Ace'
        card1 = Card(suit, rank)
        self.assertEqual((suit, rank), card1.get_value())

    def test___eq__(self):
        card1 = Card('Spades', 'Queen')
        card2 = Card('Spades', 'Queen')
        self.assertEqual(card1, card2)
        card3 = Card('Hearts', 'Queen')
        self.assertNotEqual(card1, card3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
