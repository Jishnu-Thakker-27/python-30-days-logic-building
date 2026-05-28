def print_header():
    print(f'{"ID":<5}{"Name":<15}{"Category":<20}{"Cost Price":<15}{"Selling Price":<15}{"Quantity":<15}{"Minimum Stock":<15}{"Sold":<8}{"Damaged":<10}{"Status":<15}')
    print("=" * 150)


def print_product(product_items):
    print(f'{product_items["ID"]:<5}{product_items["Name"]:<15}{product_items["Category"]:<20}{product_items["Cost price"]:<15}{product_items["Selling price"]:<15}{product_items["Quantity"]:<15}{product_items["Minimum stock"]:<15}{product_items["Sold quantity"]:<8}{product_items["Damaged quantity"]:<10}{product_items["Status"]:<15}')


def view(products):
    if not products:
        print("No product found")
        return

    print_header()

    for product_items in products:
        print_product(product_items)
