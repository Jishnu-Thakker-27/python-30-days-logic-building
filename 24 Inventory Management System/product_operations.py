from storage import save


def find_product_by_id(products, product_id):
    for product_items in products:
        if product_items["ID"] == product_id:
            return product_items
    return None


def add(products):
    product_items = {}

    id = int(input("Enter the id number of the product: "))

    if find_product_by_id(products, id):
        print("Product with this ID already exists.")
        return

    name = input("Enter the name of the product: ")
    category = input("Enter the category of the product: ")
    cost_price = int(input("Enter the cost price of the product: "))
    selling_price = int(input("Enter the selling price of the product: "))
    quantity = int(input("Enter the quantity of the product: "))
    minimum_stock = int(input("Enter the minimum stock of the product: "))
    sold_quantity = int(input("Enter the sold quantity of the product: "))
    damaged_quantity = int(input("Enter the damaged quantity of the product: "))

    archive = input('Do you want to archive this stock? Press "1" for Yes and "0" for No: ')

    archive_dict = {
        "1": "Archived",
        "0": "Not Archived"
    }

    if archive not in archive_dict:
        print("Invalid archive choice.")
        return

    product_items["ID"] = id
    product_items["Name"] = name
    product_items["Category"] = category
    product_items["Cost price"] = cost_price
    product_items["Selling price"] = selling_price
    product_items["Quantity"] = quantity
    product_items["Minimum stock"] = minimum_stock
    product_items["Sold quantity"] = sold_quantity
    product_items["Damaged quantity"] = damaged_quantity
    product_items["Status"] = archive_dict[archive]

    products.append(product_items)
    save(products)
    print("Product added successfully.")

def search(products):
    print("1. Search by ID")
    print("2. Search by name")
    print("3. Search by category")

    search = int(input("Enter the index number of the option you want to proceed with: "))

    if search == 1:
        search_id = int(input("Enter the id number of the product: "))

        for product_items in products:
            if product_items["ID"] == search_id:
                print(f'{"ID":<5}{"Name":<15}{"Category":<20}{"Cost Price":<15}{"Selling Price":<15}{"Quantity":<15}{"Minimum Stock":<15}{"Sold":<8}{"Damaged":<10}{"Status":<15}')
                print("=" * 150)
                print(f'{product_items["ID"]:<5}{product_items["Name"]:<15}{product_items["Category"]:<20}{product_items["Cost price"]:<15}{product_items["Selling price"]:<15}{product_items["Quantity"]:<15}{product_items["Minimum stock"]:<15}{product_items["Sold quantity"]:<8}{product_items["Damaged quantity"]:<10}{product_items["Status"]:<15}')
                break
        else:
            print("No such product found.")

    elif search == 2:
        product_found = False
        search_name = input("Enter the name of the product: ").lower()

        print(f'{"ID":<5}{"Name":<15}{"Category":<20}{"Cost Price":<15}{"Selling Price":<15}{"Quantity":<15}{"Minimum Stock":<15}{"Sold":<8}{"Damaged":<10}{"Status":<15}')
        print("=" * 150)

        for product_items in products:
            if product_items["Name"].lower() == search_name:
                print(f'{product_items["ID"]:<5}{product_items["Name"]:<15}{product_items["Category"]:<20}{product_items["Cost price"]:<15}{product_items["Selling price"]:<15}{product_items["Quantity"]:<15}{product_items["Minimum stock"]:<15}{product_items["Sold quantity"]:<8}{product_items["Damaged quantity"]:<10}{product_items["Status"]:<15}')
                product_found = True

        if not product_found:
            print("No such product found.")

    elif search == 3:
        product_found = False
        search_category = input("Enter the category of the product: ").lower()

        print(f'{"ID":<5}{"Name":<15}{"Category":<20}{"Cost Price":<15}{"Selling Price":<15}{"Quantity":<15}{"Minimum Stock":<15}{"Sold":<8}{"Damaged":<10}{"Status":<15}')
        print("=" * 150)

        for product_items in products:
            if product_items["Category"].lower() == search_category:
                print(f'{product_items["ID"]:<5}{product_items["Name"]:<15}{product_items["Category"]:<20}{product_items["Cost price"]:<15}{product_items["Selling price"]:<15}{product_items["Quantity"]:<15}{product_items["Minimum stock"]:<15}{product_items["Sold quantity"]:<8}{product_items["Damaged quantity"]:<10}{product_items["Status"]:<15}')
                product_found = True

        if not product_found:
            print("No such product found.")

    else:
        print("Invalid search option.")
        
        
def update(products):
    update_id = int(input("Enter the ID of the product you want to update: "))

    selected_product = find_product_by_id(products, update_id)

    if not selected_product:
        print("No product with given ID exists.")
        return

    print("\nUpdate:")
    print("1. ID")
    print("2. Name")
    print("3. Category")
    print("4. Cost Price")
    print("5. Selling Price")
    print("6. Minimum Stock")
    print("7. Status")

    updates = int(input("Enter the option number you want to update: "))

    if updates == 1:
        new_id = int(input("Enter the new ID: "))

        id_exists = False

        for product_items in products:
            if product_items["ID"] == new_id:
                id_exists = True
                break

        if id_exists:
            print("This ID already exists. Enter a unique ID.")
        else:
            selected_product["ID"] = new_id
            save(products)
            print("ID updated successfully.")

    elif updates == 2:
        new_name = input("Enter the new name: ")
        selected_product["Name"] = new_name
        save(products)
        print("Name updated successfully.")

    elif updates == 3:
        new_category = input("Enter the new category: ")
        selected_product["Category"] = new_category
        save(products)
        print("Category updated successfully.")

    elif updates == 4:
        new_cost_price = int(input("Enter the new cost price: "))
        selected_product["Cost price"] = new_cost_price
        save(products)
        print("Cost price updated successfully.")

    elif updates == 5:
        new_selling_price = int(input("Enter the new selling price: "))
        selected_product["Selling price"] = new_selling_price
        save(products)
        print("Selling price updated successfully.")

    elif updates == 6:
        new_minimum_stock = int(input("Enter the new minimum stock: "))
        selected_product["Minimum stock"] = new_minimum_stock
        save(products)
        print("Minimum stock updated successfully.")

    elif updates == 7:
        print("1. Archived")
        print("0. Not Archived")

        status_choice = input("Enter status choice: ")

        if status_choice == "1":
            selected_product["Status"] = "Archived"
            save(products)
            print("Status updated successfully.")

        elif status_choice == "0":
            selected_product["Status"] = "Not Archived"
            save(products)
            print("Status updated successfully.")

        else:
            print("Invalid status choice.")

    else:
        print("Invalid update option.")

    

def archive(products):
    archive_id = int(input("Enter the id of the product you want to archive: "))

    product_items = find_product_by_id(products, archive_id)

    if not product_items:
        print("No product with given ID exists.")
        return

    if product_items["Status"] == "Not Archived":
        product_items["Status"] = "Archived"
        save(products)
        print("Product archived successfully.")
    else:
        print("Product is already archived.")
            
