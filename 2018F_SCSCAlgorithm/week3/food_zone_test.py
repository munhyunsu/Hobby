import unittest

from food_truck import FoodTruck
from food_zone import FoodZone


class FoodZoneTest(unittest.TestCase):
    def test___init__(self):
        order_probability = 300
        var_food_zone = FoodZone(order_probability)
        self.assertEqual(set(), var_food_zone.food_trucks)
        self.assertEqual(list(), var_food_zone.order_queue)
        self.assertEqual(list(), var_food_zone.waiting_times)
        self.assertEqual(list(), var_food_zone.income)
        self.assertEqual(order_probability, var_food_zone.order_probability)

    def test_add_truck(self):
        order_probability = 300
        var_food_zone = FoodZone(order_probability)
        price = 3000
        making_time = 60
        var_truck = FoodTruck(price, making_time)
        var_food_zone.add_truck(var_truck)
        self.assertIn(var_truck, var_food_zone.food_trucks)

    def test_is_new_order(self):
        order_probability = 300
        var_food_zone = FoodZone(order_probability)
        self.assertEqual(True, var_food_zone.is_new_order(order_probability))
        self.assertEqual(False, var_food_zone.is_new_order(order_probability - 1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
