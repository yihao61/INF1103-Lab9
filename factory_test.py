from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
import FileHandling

# Prediction (before running):
# ProductFactory.create("service", ...) reaches the else branch and the
# `raise ValueError(f"Unknown product type: {product_type}")` line raises.
# Nothing catches it here, so the program would stop with a traceback.

supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")

chair = ProductFactory.create("physical", "P001", "Gaming Chair", 999.0, 10, supplier, 12.5)
ebook = ProductFactory.create("digital", "D001", "E-Book", 19.9, 50, supplier, 25)
print(type(chair).__name__, isinstance(chair, Product), isinstance(chair, PhysicalProduct))
print(type(ebook).__name__, isinstance(ebook, Product), isinstance(ebook, DigitalProduct))
for product in (chair, ebook):  # polymorphism: only the Product type is needed
    print(product.display_information())

print("\nLoading inventory.json through the factory:")
loaded = FileHandling.load_inventory("inventory.json")
print(len(loaded), "products loaded")

print("\nCalling ProductFactory.create('service', ...) with nothing catching it:")
ProductFactory.create("service", "S001", "Installation", 30.0, 5, supplier)
print("This line is never reached.")
