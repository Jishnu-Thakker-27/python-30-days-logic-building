

def view_task(tasks):
    if not tasks:   
        print("No tasks found.")
        return
    print(f"{'ID':<5}{'TASK':<20}{'STATUS':<15}")
    print("=" * 40)
    for item  in tasks:
        if item['Status']== "Completed":
            print(f"{item['id']:<5}{item['Task']:<20}✅ {item['Status']:<15}")
        else:
            print(f"{item['id']:<5}{item['Task']:<20}⏳ {item['Status']:<15}")
            
        
    print("These are your Current Tasks.\n")
