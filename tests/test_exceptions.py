import contextlib
import io
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import FileHandling
from inventory import Inventory
from inventory_manager import get_positive_float
from supplier import Supplier

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_quietly(function, *args):
    """Call function and return (its result, everything it printed)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class GetPositiveFloatTests(unittest.TestCase):
    def test_asks_again_until_valid_and_prints_messages(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as mocked_input:
            value, output = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(mocked_input.call_count, 3)
        self.assertEqual(output.splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "1"]):
            value, output = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 1.0)
        self.assertIn("greater than zero", output)


class LoadProductsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
        self.inventory = Inventory()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def write_csv(self, text: str) -> str:
        path = Path(self.temp_dir.name) / "products.csv"
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_bad_rows_are_reported_and_skipped_and_good_rows_load(self):
        path = self.write_csv(CSV_TEXT)
        _, output = run_quietly(FileHandling.load_products, path, self.inventory, self.supplier)
        ids = [p.get_product_id() for p in self.inventory.get_inventory()]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("could not convert string to float: 'abc'", output)
        self.assertIn("3 products loaded.", output)

    def test_message_order_ends_with_count_then_finally(self):
        path = self.write_csv(CSV_TEXT)
        _, output = run_quietly(FileHandling.load_products, path, self.inventory, self.supplier)
        lines = [line for line in output.splitlines() if line.strip()]
        self.assertEqual(lines[-2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_is_handled_gracefully(self):
        missing = str(Path(self.temp_dir.name) / "does_not_exist.csv")
        _, output = run_quietly(FileHandling.load_products, missing, self.inventory, self.supplier)
        self.assertIn(f"Products file not found: {missing}", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded", output)
        self.assertEqual(self.inventory.get_inventory(), [])

    def test_row_with_missing_columns_is_skipped(self):
        path = self.write_csv("product_type,product_id,name,price,stock_quantity\nphysical,P001,Lamp\n"
                              "physical,P002,Chair,10,2\n")
        _, output = run_quietly(FileHandling.load_products, path, self.inventory, self.supplier)
        self.assertEqual([p.get_product_id() for p in self.inventory.get_inventory()], ["P002"])
        self.assertIn("1 products loaded.", output)

    def test_negative_price_row_is_skipped_by_validation(self):
        path = self.write_csv("product_type,product_id,name,price,stock_quantity\nphysical,P001,Lamp,-5,2\n")
        _, output = run_quietly(FileHandling.load_products, path, self.inventory, self.supplier)
        self.assertEqual(self.inventory.get_inventory(), [])
        self.assertIn("Price must be greater than zero.", output)


class SpecificExceptTests(unittest.TestCase):
    def test_no_bare_or_broad_except_in_project_code(self):
        pattern = re.compile(r"^\s*except\s*(:|Exception\b|BaseException\b)")
        offenders = []
        for name in ("inventory_manager.py", "FileHandling.py", "inventory.py", "order.py",
                     "orderline.py", "product.py", "product_factory.py"):
            lines = (PROJECT_ROOT / name).read_text(encoding="utf-8").splitlines()
            offenders += [f"{name}:{n}" for n, line in enumerate(lines, start=1) if pattern.match(line)]
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
