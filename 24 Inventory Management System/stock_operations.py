from product_operations import find_product_by_id
from storage import save


def purchase_stock(products):
    product_id = int(input("Enter product ID: "))
    product = find_product_by_id(products, product_id)

    if not product:
        print("Product not found.")
        return

    quantity = int(input("Enter purchase quantity: "))

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    product["Quantity"] += quantity
    save(products)
    print("Stock purchased successfully.")


def sell_stock(products):
    product_id = int(input("Enter product ID: "))
    product = find_product_by_id(products, product_id)

    if not product:
        print("Product not found.")
        return

    if product["Status"] == "Archived":
        print("Cannot sell archived product.")
        return

    quantity = int(input("Enter selling quantity: "))

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    if quantity > product["Quantity"]:
        print("Not enough stock.")
        return

    product["Quantity"] -= quantity
    product["Sold quantity"] += quantity
    save(products)
    print("Stock sold successfully.")


def return_stock(products):
    product_id = int(input("Enter product ID: "))
    product = find_product_by_id(products, product_id)

    if not product:
        print("Product not found.")
        return

    quantity = int(input("Enter returned quantity: "))

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    if quantity > product["Sold quantity"]:
        print("Returned quantity cannot be more than sold quantity.")
        return

    product["Quantity"] += quantity
    product["Sold quantity"] -= quantity
    save(products)
    print("Stock returned successfully.")


def damaged_stock(products):
    product_id = int(input("Enter product ID: "))
    product = find_product_by_id(products, product_id)

    if not product:
        print("Product not found.")
        return

    quantity = int(input("Enter damaged quantity: "))

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    if quantity > product["Quantity"]:
        print("Damaged quantity cannot be more than available stock.")
        return

    product["Quantity"] -= quantity
    product["Damaged quantity"] += quantity
    save(products)
    print("Damaged stock updated successfully.")
