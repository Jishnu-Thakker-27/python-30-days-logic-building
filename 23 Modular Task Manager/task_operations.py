tasks=[]
task_items={}
def add_task():
    task_id=int(input("Enter the task number "))
    task=input("Enter the task") 
    status=input("Add status to the task([Y] for Complete/[N] for Incomplete) ")
    task_items["id"]=task_id
    task_items["Task"]=task
    task_items["Status"]=status
    
    tasks.append(task_items)
    print(tasks)
def delete_task():
    pass
def complete_task():
    pass
def save_task():
    pass
def view_task():
    pass
