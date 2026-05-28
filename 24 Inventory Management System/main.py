from storage import load
from product_operations import add
from product_operations import search
from product_operations import update
from product_operations import archive
from stock_operations import purchase_stock
from stock_operations import sell_stock
from stock_operations import return_stock
from stock_operations import damaged_stock
from reports import low_stock_report
from reports import inventory_value_report
from reports import profit_report
from reports import category_report
from display import view

products=load()

while True:
    print("Inventory Management System")
    print("1. Add Product ")
    print("2. View Products ")
    print("3. Search Products ")
    print("4. Update Product ")
    print("5. Archive Product")
    print("6. Stock Management")
    print("7. Reports")
    print("8. Exit")

    choice=int(input("Enter the index number of the option you want to proceed with."))
    if choice==1:
        add(products)
        
    elif choice==2:
        view(products)
        
    elif choice==3:
        search(products)
    
    elif choice==4:
        update(products)
    
    elif choice==5:
        archive(products)

    elif choice==6:
        print("Stock Management")
        print("1. Purchase Stock")
        print("2. Sell Stock")
        print("3. Return Stock")
        print("4. Mark Damaged Stock")
        print("5. Back")

        stock_choice=int(input("Enter the index number of the option you want to proceed with."))

        if stock_choice==1:
            purchase_stock(products)
        elif stock_choice==2:
            sell_stock(products)
        elif stock_choice==3:
            return_stock(products)
        elif stock_choice==4:
            damaged_stock(products)
        elif stock_choice==5:
            pass
        else:
            print("Invalid choice.")

    elif choice==7:
        print("Reports")
        print("1. Low Stock Report")
        print("2. Inventory Value Report")
        print("3. Profit Report")
        print("4. Category Report")
        print("5. Back")

        report_choice=int(input("Enter the index number of the option you want to proceed with."))

        if report_choice==1:
            low_stock_report(products)
        elif report_choice==2:
            inventory_value_report(products)
        elif report_choice==3:
            profit_report(products)
        elif report_choice==4:
            category_report(products)
        elif report_choice==5:
            pass
        else:
            print("Invalid choice.")
        
    elif choice==8:
        break
    
    else:
        print("Invalid choice.")
    

