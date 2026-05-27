def view(products):
    if not products:
        print("No product found")
    print(f"{"ID":<5}{"Name":<10}{"Category":<20}{"Cost Price":<15}{"Selling Price":<15}{"Quantity":<15}{"Minimum Stock":<15}{"Sold":<5}{"Damaged":<15}{"Archived":<15}")
    print("="* 150)
    
    for product_items in products:
        print(f"{product_items["ID"]:<10}{product_items["Name"]:<10}{product_items["Category"]:<20}{product_items["Cost price"]:<15}{product_items["Selling price"]:<15}{product_items["Quantity"]:<15}{product_items["Minimum stock"]:<15}{product_items["Sold quantity"]:<5}{product_items["Damaged quantity"]:<15}{product_items["Archived"]:<15}")