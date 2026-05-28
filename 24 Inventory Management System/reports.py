from display import print_header, print_product


def low_stock_report(products):
    found = False

    print("\nLow Stock Report")
    print_header()

    for product in products:
        if product["Status"] == "Not Archived" and product["Quantity"] <= product["Minimum stock"]:
            print_product(product)
            found = True

    if not found:
        print("No low stock products found.")


def inventory_value_report(products):
    total_cost_value = 0
    total_selling_value = 0

    for product in products:
        if product["Status"] == "Not Archived":
            total_cost_value += product["Cost price"] * product["Quantity"]
            total_selling_value += product["Selling price"] * product["Quantity"]

    print("\nInventory Value Report")
    print(f"Total cost value: {total_cost_value}")
    print(f"Total selling value: {total_selling_value}")


def profit_report(products):
    total_profit = 0

    print("\nProfit Report")
    print(f'{"ID":<5}{"Name":<15}{"Sold":<8}{"Profit/Item":<15}{"Total Profit":<15}')
    print("=" * 60)

    for product in products:
        profit_per_item = product["Selling price"] - product["Cost price"]
        product_profit = profit_per_item * product["Sold quantity"]
        total_profit += product_profit

        print(f'{product["ID"]:<5}{product["Name"]:<15}{product["Sold quantity"]:<8}{profit_per_item:<15}{product_profit:<15}')

    print("=" * 60)
    print(f"Total profit: {total_profit}")


def category_report(products):
    categories = {}

    for product in products:
        if product["Status"] == "Archived":
            continue

        category = product["Category"]

        if category not in categories:
            categories[category] = {
                "products": 0,
                "quantity": 0,
                "selling_value": 0,
            }

        categories[category]["products"] += 1
        categories[category]["quantity"] += product["Quantity"]
        categories[category]["selling_value"] += product["Selling price"] * product["Quantity"]

    if not categories:
        print("No active products found.")
        return

    print("\nCategory Report")
    print(f'{"Category":<20}{"Products":<10}{"Quantity":<10}{"Selling Value":<15}')
    print("=" * 60)

    for category, data in categories.items():
        print(f'{category:<20}{data["products"]:<10}{data["quantity"]:<10}{data["selling_value"]:<15}')
