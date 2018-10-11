import unittest

from order import Order


class OrderTest(unittest.TestCase):
    def setUp(self):
        self.timestamp = 48
        self.var_order = Order(self.timestamp)

    def tearDown(self):
        del self.timestamp
        del self.var_order

    def test___init__(self):
        self.assertEqual(self.timestamp, self.var_order.order_time)
        self.assertGreaterEqual(self.var_order.qty, 1)
        self.assertLessEqual(self.var_order.qty, 5)

    def test_get_order_time(self):
        self.assertEqual(self.timestamp, self.var_order.get_order_time())

    def test_get_qty(self):
        self.assertGreaterEqual(self.var_order.get_qty(), 1)
        self.assertLessEqual(self.var_order.get_qty(), 5)

    def test_wait_time(self):
        current_time = 60
        self.assertEqual(12, self.var_order.wait_time(current_time))



if __name__ == '__main__':
    unittest.main(verbosity=2)
