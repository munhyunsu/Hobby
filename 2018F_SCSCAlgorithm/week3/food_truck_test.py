import unittest

from order import Order
from food_truck import FoodTruck


class FoodTruckTest(unittest.TestCase):
    def test___init__(self):
        price = 5000
        making_time = 60
        var_food_truck = FoodTruck(price, making_time)
        self.assertEqual(price, var_food_truck.price)
        self.assertEqual(making_time, var_food_truck.making_time)
        self.assertEqual(None, var_food_truck.current_order)
        self.assertEqual(0, var_food_truck.time_remaining)

    def test_tick(self):
        price = 5000
        making_time = 60
        var_truck = FoodTruck(price, making_time)
        var_truck.current_order = Order(10)
        var_truck.time_remaining = 10
        for index in range(9, -1, -1):
            var_truck.tick()
            self.assertEqual(index, var_truck.time_remaining)
        self.assertEqual(None, var_truck.current_order)

    def test_is_busy(self):
        price = 4000
        making_time = 60
        var_truck = FoodTruck(price, making_time)
        var_truck.current_order = Order(10)
        var_truck.time_remaining = 10
        self.assertEqual(True, var_truck.is_busy())
        var_truck.current_order = None
        var_truck.time_remaining = 0
        self.assertEqual(False, var_truck.is_busy())

    def test_start_next_food(self):
        price = 3000
        making_time = 60
        var_truck = FoodTruck(price, making_time)
        next_order = Order(10)
        var_truck.start_next_food(next_order)
        self.assertEqual(next_order, var_truck.current_order)
        self.assertEqual(making_time*next_order.get_qty(), var_truck.time_remaining)


if __name__ == '__main__':
    unittest.main(verbosity=2)
