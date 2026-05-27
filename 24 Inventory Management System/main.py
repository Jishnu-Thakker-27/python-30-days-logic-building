from storage import load
from product_operations import add
from product_operations import search
from product_operations import update
from product_operations import archive
from display import view
products=load()
while True:
    print("Inventory Management System")
    print("Menu : ")
    print("1. Product Management")
    print("2. Stock Management")
    print("3. Reports")
    print("4. Transaction History")
    print("5. Exit")

    primary_choice=int(input("Enter the index number of the option you want to proceed with."))

    while True:
        if primary_choice==1:
            print("Product Management: ")
            print("1. Add Product ")
            print("2. View Products ")
            print("3. Search Products ")
            print("4. Update Product ")
            print("5. Archive Product")
            print("6. Back to main menu")
            
            secondary_choice=int(input("Enter the index number of the option you want to proceed with."))
            
            if secondary_choice==1:
                add(products)
                
            elif secondary_choice==2:
                view(products)
                
            elif secondary_choice==3:
                search(products)
            
            elif secondary_choice==4:
                update(products)
            
            elif secondary_choice==5:
                archive(products)
            
        elif primary_choice==2:
            print("Stock Management: ")
            print("1. Purchase Stock ")
            print("2. Sell Stock ")
            print("3. Return Stock ")
            print("4. Mark Damaged Stock ")
            print("5. Manual Adjustment")
        
        elif primary_choice==3:
            print("Reports")
            print("1. Low Stock Report")
            print("2. Inventory Value Report")
            print("3. Profit Report")
            print("4. Category Report")

        elif primary_choice==4:
            pass

        elif primary_choice==5:
            pass
        
        elif primary_choice==6:
            break
