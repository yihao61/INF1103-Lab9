import unittest

from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class ValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")

    def create(self, product_type="physical", price=10.0, stock=5):
        return ProductFactory.create(product_type, "X001", "Item", price, stock, self.supplier, 1.0)

    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -1, -0.01):
            for product_type in ("physical", "digital"):
                with self.subTest(price=bad_price, type=product_type):
                    with self.assertRaises(ValueError):
                        self.create(product_type, price=bad_price)

    def test_stock_cannot_be_negative(self):
        for product_type in ("physical", "digital"):
            with self.subTest(type=product_type):
                with self.assertRaises(ValueError):
                    self.create(product_type, stock=-1)

    def test_zero_stock_is_allowed(self):
        self.assertEqual(self.create(stock=0).get_stock(), 0)

    def test_update_stock_rejects_negative_and_keeps_old_value(self):
        for product_type in ("physical", "digital"):
            with self.subTest(type=product_type):
                product = self.create(product_type, stock=5)
                with self.assertRaises(ValueError):
                    product.update_stock(-3)
                self.assertEqual(product.get_stock(), 5)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        order = Order("O1")
        product = self.create()
        for bad_quantity in (0, -2):
            with self.subTest(quantity=bad_quantity):
                with self.assertRaises(ValueError) as context:
                    order.add_order_line(product, bad_quantity)
                self.assertEqual(str(context.exception), "Quantity must be greater than zero.")
        self.assertEqual(order.get_order_lines(), [])

    def test_valid_order_quantity_is_accepted(self):
        order = Order("O1")
        order.add_order_line(self.create(), 1)
        self.assertEqual(len(order.get_order_lines()), 1)


if __name__ == "__main__":
    unittest.main()
