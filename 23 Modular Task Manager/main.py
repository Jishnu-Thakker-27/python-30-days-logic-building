from task_operations import add_task
from task_operations import delete_task
from task_operations import complete_task
from task_operations import save_task
from task_operations import view_task

while True:
    print("Task Manager")
    print("1.Add Task")
    print("2.View Task")
    print("3.Mark tasks as completed")
    print("4.Save tasks permanently")
    print("5.Delete Task")
    print("6.Exit")
    try:
        Task=int(input("Enter the index number for your task."))
    except ValueError:
        print("Enter the integer value")
        print("Invalid Input.")
    if Task==1:
        add_task()
    elif Task==2:
        view_task()
    elif Task==3:
        complete_task()
    elif Task==4:
        save_task()
    elif Task==5:
        delete_task()
    elif Task==6:
        break
    else:
        print("Invalid Input.")
