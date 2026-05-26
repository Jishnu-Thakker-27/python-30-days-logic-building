from task_operations import add_task
from task_operations import delete_task
from task_operations import complete_task
from storage import load_task
from display import view_task


tasks=load_task()

while True:
    print("Task Manager")
    print("1.Add Task")
    print("2.View Task")
    print("3.Mark tasks as completed")
    print("4.Delete Task")
    print("5.Exit")
    try:
        Task=int(input("Enter the index number for your task."))
    except ValueError:
        print("Enter the integer value")
        print("Invalid Input.")
        continue
    if Task==1:
        add_task(tasks)
    elif Task==2:
        view_task(tasks)
    elif Task==3:
        complete_task(tasks)
    elif Task==4:
        delete_task(tasks)
    elif Task==5:
        break
    else:
        print("Invalid Input.")
