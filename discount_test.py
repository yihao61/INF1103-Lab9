from supplier import Supplier
from physical_product import PhysicalProduct
from order import Order
from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount

# Prediction (before running):
# Lines add up to 250. BulkDiscount(200, 20) -> 230.0 (250 >= 200, so 20 off).
# After set_discount(PercentageDiscount(10)) on the same order -> 225.0.

supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
lamp = PhysicalProduct("P001", "Desk Lamp", 25.0, 100, supplier, 1.0)

order = Order("O1", BulkDiscount(200, 20))
order.add_order_line(lamp, 10)
print("Total with BulkDiscount(200, 20):", order.calculate_total())
order.set_discount(PercentageDiscount(10))
print("Total after set_discount(PercentageDiscount(10)):", order.calculate_total())
order.set_discount(StudentDiscount())
print("Total after set_discount(StudentDiscount()):", order.calculate_total())
print("Default order (NoDiscount):", Order("O2").calculate_total())
