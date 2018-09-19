import unittest

import greeting


class GreetingTest(unittest.TestCase):
    def test_greeting_en(self):
        self.assertEqual('Hello, World!',
                         greeting.hello_en())

    def test_greeting_kr(self):
        self.assertEqual('안녕하세요!',
                         greeting.hello_kr())


if __name__ == '__main__':
    unittest.main(verbosity=2)