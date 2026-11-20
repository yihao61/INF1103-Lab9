import inspect
import unittest

from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


# Predict first (2.3): an order whose lines add up to 250 returns 230.0 with
# BulkDiscount(200, 20), then 225.0 after set_discount(PercentageDiscount(10)).
class DiscountTests(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
        self.lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.0, 100, supplier, 1.0)

    def make_order(self, discount=None) -> Order:
        order = Order("O1", discount) if discount is not None else Order("O1")
        order.add_order_line(self.lamp, 10)  # 10 x 25 = 250
        return order

    def test_default_order_uses_no_discount(self):
        self.assertEqual(self.make_order().calculate_total(), 250.0)

    def test_percentage_discount(self):
        self.assertAlmostEqual(self.make_order(PercentageDiscount(10)).calculate_total(), 225.0)

    def test_bulk_discount_applies_at_threshold(self):
        self.assertEqual(self.make_order(BulkDiscount(200, 20)).calculate_total(), 230.0)
        self.assertEqual(self.make_order(BulkDiscount(250, 20)).calculate_total(), 230.0)

    def test_bulk_discount_not_applied_below_threshold(self):
        self.assertEqual(self.make_order(BulkDiscount(300, 20)).calculate_total(), 250.0)

    def test_strategies_inherit_from_discount_strategy(self):
        for strategy in (NoDiscount(), PercentageDiscount(5), BulkDiscount(1, 1), StudentDiscount()):
            self.assertIsInstance(strategy, DiscountStrategy)

    def test_discount_strategy_cannot_be_created_directly(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_set_discount_changes_existing_order(self):
        order = self.make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self):
        class HalfPrice(DiscountStrategy):  # defined here, Order knows nothing about it
            def apply(self, total: float) -> float:
                return total / 2

        self.assertEqual(self.make_order(HalfPrice()).calculate_total(), 125.0)

    def test_student_discount(self):
        self.assertAlmostEqual(self.make_order(StudentDiscount()).calculate_total(), 237.5)

    def test_two_orders_can_share_one_strategy(self):
        """Order -> DiscountStrategy is an association: the order uses the strategy, it does not own it."""
        shared = PercentageDiscount(10)
        order_a = self.make_order(shared)
        order_b = self.make_order(shared)
        self.assertIs(order_a._Order__discount, order_b._Order__discount)
        self.assertAlmostEqual(order_a.calculate_total(), 225.0)
        self.assertAlmostEqual(order_b.calculate_total(), 225.0)

    def test_order_has_no_discount_if_elif_logic(self):
        source = inspect.getsource(Order)
        self.assertNotIn("elif", source)
        self.assertNotIn("isinstance", source)
        self.assertNotIn("discount_type", source)


if __name__ == "__main__":
    unittest.main()
