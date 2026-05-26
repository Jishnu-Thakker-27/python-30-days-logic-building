from storage import save_task

def add_task(tasks):
    task_items={}
    task_id=int(input("Enter the task number "))
    for item in tasks:
        if item["id"]==task_id:
            print("Task Id already exist.")
            return add_task(tasks)
        
    task=input("Enter the task") 
    status=input("Add status to the task([Y] for Complete/[N] for Incomplete) ").upper()
    status_dict={
        "Y": "Completed",
        "N": "Pending",
        
    }
    task_items['id']=task_id
    task_items['Task']=task
    task_items['Status']=status_dict[status]
    
    tasks.append(task_items)
    save_task(tasks)

def delete_task(tasks):
    delete_id=int(input("Enter the id of task you want to delete."))
    for index,item in enumerate(tasks):
        if item['id']==delete_id:
            tasks.pop(index)
            save_task(tasks)
            print("Task deleted successfully.")
            break
    else:
        print("No such task id exists.")
            
def complete_task(tasks):
    complete_id=int(input("Enter the id of task you have completed."))
    for index,item in enumerate(tasks):
        if item['id']==complete_id:
            if item['Status']=="Y":
                print("This task was already marked as completed")
            else:
                item['Status']="Y"
                save_task(tasks)
                print("Task Marked as completed")
            break
    else:
        print("No such task id exists.")
