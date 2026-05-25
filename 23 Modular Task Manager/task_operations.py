tasks=[]
def add_task():
    task_items={}
    task_id=int(input("Enter the task number "))
    for item in tasks:
        if item["id"]==task_id:
            print("Task Id already exist.")
            return add_task()
        
    task=input("Enter the task") 
    status=input("Add status to the task([Y] for Complete/[N] for Incomplete) ").upper()
    task_items['id']=task_id
    task_items['Task']=task
    task_items['Status']=status
    
    tasks.append(task_items)
    print(tasks)
def delete_task():
    delete_id=int(input("Enter the id of task you want to delete."))
    for index,item in enumerate(tasks):
        if item['id']==delete_id:
            tasks.pop(index)
            print("Task deleted successfully.")
            break
    else:
        print("No such task id exists.")
            
def complete_task():
    complete_id=int(input("Enter the id of task you have completed."))
    for index,item in enumerate(tasks):
        if item['id']==complete_id:
            if item['Status']=="Y":
                print("This task was already marked as completed")
            else:
                item['Status']="Y"
                print("Task Marked as completed")
            break
    else:
        print("No such task id exists.")
def save_task():
    pass
def view_task():
    if not tasks:   
        print("No tasks found.")
        return
    for item  in tasks:
        print(f"{item['id']}")
        print(f"{item['Task']}")
        print(f"{item['Status']}")
    print("These are your Current Tasks.")
