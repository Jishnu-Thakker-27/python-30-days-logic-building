import json
def add(products):
    product_items={}
    id=int(input("Enter the id number of the product."))
    name=input("Enter the name of the product.")
    category=input("Enter the category of the product.")
    cost_price=input("Enter the cost price of the product.")
    selling_price=input("Enter the selling price of the product.")
    quantity=input("Enter the quantity of the product.")
    minimum_stock=input("Enter the minimum stock of the product.")
    sold_quantity=input("Enter the sold quantity of the product.")
    damaged_quantity=input("Enter the damaged quantity of the product.")
    archive=bool(input("Do you want to  archive this stock? Press \"1\" for Yes and for \"0\" No."))
    
    archive_dict={
        1: "Archived",
        0: "Not Archived"
    }
    
    product_items["ID"]=id
    product_items["Name"]=name
    product_items["Category"]=category
    product_items["Cost price"]=cost_price
    product_items["Selling price"]=selling_price
    product_items["Quantity"]=quantity
    product_items["Minimum stock"]=minimum_stock
    product_items["Sold quantity"]=sold_quantity
    product_items["Damaged quantity"]=damaged_quantity
    product_items["Archived"]=archive_dict[archive]
    
    products.append(product_items)
    
    with open("products.json","w") as f:
        json.dump(products,f)    
def search(products):
    print("1.Search by ID: ")
    print("2.Search by name: ")
    print("3.Search by category: ")
    
    search=int(input("Enter the index number of the option you want to proceed with."))
    
    if search==1:
        search_id=int(input("Enter the id number of the product."))
        for product_items in products:
            if product_items["ID"]==search_id:
                print(product_items)
    
    if search==2:
        search_name=input("Enter the name of the product.")
        for product_items in products:
            if product_items["Name"]==search_name:
                print(product_items)
    
    if search==3:
        search_category=input("Enter the category of the product.")
        for product_items in products:
            if product_items["Category"]==search_category:
                print(product_items)
        

def update():
    pass

def archive():
    pass