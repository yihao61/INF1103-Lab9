from supplier import Supplier
from product_factory import ProductFactory
from order import Order

# Prediction (before running):
# DigitalProduct must not skip or change the stock rule, because it is a Product
# (LSP). The rule lives in Product, so DigitalProduct inherits it and rejects
# negative stock exactly like PhysicalProduct.

supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")


def expect_error(description, action):
    try:
        action()
    except ValueError as error:
        print(f"[PASS] {description}: ValueError('{error}')")
    else:
        print(f"[FAIL] {description}: no error raised")


expect_error("price 0 rejected", lambda: ProductFactory.create("physical", "P1", "A", 0, 1, supplier, 1))
expect_error("negative price rejected", lambda: ProductFactory.create("physical", "P1", "A", -5, 1, supplier, 1))
expect_error("negative stock rejected (physical)", lambda: ProductFactory.create("physical", "P1", "A", 5, -1, supplier, 1))
expect_error("negative stock rejected (digital)", lambda: ProductFactory.create("digital", "D1", "A", 5, -1, supplier, 1))

digital = ProductFactory.create("digital", "D1", "E-Book", 10.0, 5, supplier, 20)
expect_error("update_stock(-3) rejected on DigitalProduct", lambda: digital.update_stock(-3))
print("Stock unchanged after rejected update:", digital.get_stock())

order = Order("O1")
expect_error("order quantity 0 rejected", lambda: order.add_order_line(digital, 0))
expect_error("order quantity -2 rejected", lambda: order.add_order_line(digital, -2))
print("Order lines after rejections:", len(order.get_order_lines()))
order.add_order_line(digital, 1)
print("Valid quantity accepted, lines:", len(order.get_order_lines()))
