import re
import unittest
from pathlib import Path

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class FactoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Chair", 99.0, 5, self.supplier, 12.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_weight(), 12.5)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "E-Book", 9.9, 50, self.supplier, 25)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 25)

    def test_unknown_type_raises_value_error_with_clear_message(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Install", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_products_are_only_created_inside_the_factory(self):
        """Application code must go through ProductFactory (old Lab 8 demo scripts are ignored)."""
        allowed = {"product_factory.py"}
        pattern = re.compile(r"(?<!class )\b(PhysicalProduct|DigitalProduct)\(")
        offenders = []
        for path in PROJECT_ROOT.glob("*.py"):
            if path.name in allowed or path.name.endswith("_test.py"):
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if pattern.search(line) and not line.lstrip().startswith(("class ", "#")):
                    offenders.append(f"{path.name}:{number}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
