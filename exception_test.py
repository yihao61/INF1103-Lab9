import builtins
from supplier import Supplier
from inventory import Inventory
from inventory_manager import get_positive_float
import FileHandling

# Prediction 5.1 (before running): input "abc" prints
#   "Please enter a valid number, e.g. 12.50"; "-5" prints
#   "Please enter a number greater than zero."; "12.50" prints nothing and returns 12.5.
# Prediction 5.2 (before running): 3 products load (P001, D001, P003). Order:
#   3 "Product added successfully!" with a "Skipping row 4: Unknown product type: service"
#   after D001, "Skipping row 5: could not convert string to float: 'abc'" after that,
#   then "3 products loaded." then "Load attempt finished."
#   With the file renamed: only "Products file not found: ..." (except) and
#   "Load attempt finished." (finally). The else block does not run.

print("=== 5.1 get_positive_float with inputs abc, -5, 12.50 ===")
answers = iter(["abc", "-5", "12.50"])
builtins.input = lambda prompt="": next(answers)
result = get_positive_float("Price: ")
print("Returned:", result)

supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")

print("\n=== 5.2 load_products with products.csv ===")
inventory = Inventory()
FileHandling.load_products("products.csv", inventory, supplier)
print("Inventory now holds:", [p.get_product_id() for p in inventory.get_inventory()])

print("\n=== 5.2 load_products with a missing file ===")
inventory = Inventory()
FileHandling.load_products("products_missing.csv", inventory, supplier)
print("Inventory now holds:", len(inventory.get_inventory()), "products")
