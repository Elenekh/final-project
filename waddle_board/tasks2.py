import json #stores user data
from datetime import datetime #for deadlines

# Function to process date and check if it's valid
def parse_date(date_str):
    try: #one who executes 
        return datetime.strptime(date_str, "%Y-%m-%d") #converts to smth datetime understands
    except ValueError: #one who's in charge if theres an error
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None #LOL FAILURE

# Function to save tasks to the file
def save_tasks(filename, username, tasks):
    with open(filename, "r") as file: #opens file + closes in the end
        data = json.load(file) #then loads the data from the file
    data["users"][username]["tasks"] = tasks #gets users section data of specific usesr, 
    #then gets to their task section and updates with new task
    with open(filename, "w") as file: #now in write mode
        json.dump(data, file, indent=4) #converts it to json readable language
 
# Function to create a new task and assign it to a column
def create_task(tasks, filename, username): # current task dict + json file for saving + user who creates it
    print("\n CREATE NEW WADDLETASK")
    title = input("Enter WaddleTask title: ").strip()
    description = input("Enter WaddleTask description: ").strip()
    due_date_str = input("Enter due date (YYYY-MM-DD): ").strip()
    due_date = parse_date(due_date_str)
    if not due_date:
        return

    priority = input("Set priority (High, Medium, Low): ").strip().capitalize()

    print("\n CHOOSE A COLUMN FOR THIS WADDLETASK ")
    print("1. To-Do")
    print("2. In Progress")
    print("3. Done")

    column_choice = input("Select column (1, 2, 3): ").strip()

    column_mapping = {
        "1": "To-Do",
        "2": "In Progress",
        "3": "Done"
    }
    #maps column numbers to names
    column = column_mapping.get(column_choice, "To-Do")  # Default to "To-Do" if invalid input
    
    task = {
        "title": title,
        "description": description,
        "due_date": due_date_str,
        "priority": priority,
        "completed": False
    }
#creates task dict -> appends task to column -> saves it in save_tasks 
    tasks[column].append(task)
    save_tasks(filename, username, tasks)
    print(f"WaddleTask created successfully and added to '{column}' column!")

# Function to list tasks in all columns -> further organization
def list_tasks(tasks):
    if not any(tasks[column] for column in tasks): #iterates through columns
        print("No WaddleTasks available.")
        return

    for column in tasks:
        print(f"\n {column} ")
        if not tasks[column]:
            print("No WaddleTasks in this column.")
            continue

        for i, task in enumerate(tasks[column], 1): #goes through every detail, plus starts from 1 cuz it's mor humane
            print(f"\nTask {i}:")
            print(f"  Title: {task['title']}")
            print(f"  Description: {task['description']}")
            print(f"  Due Date: {task['due_date']}")
            print(f"  Priority: {task['priority']}")
            print(f"  Completed: {'Yes' if task['completed'] else 'No'}")

# Function to handle "All Tasks" menu
def all_tasks_menu(tasks, filename, username):
    while True:
        list_tasks(tasks)
        print("\nALL TASKS MENU")
        print("1. Edit Task")
        print("2. Delete Task")
        print("3. Exit to Main Menu")
        
        choice = input("Choose an option: ").strip()

        if choice == "1":
            edit_task(tasks, filename, username)
        elif choice == "2":
            delete_task(tasks, filename, username)
        elif choice == "3":
            break
        else:
            print("Invalid option! Please try again.")

# Function to edit an existing task
def edit_task(tasks, filename, username):
    list_tasks(tasks)
    column_choice = input("Enter the column where the WaddleTask exists (To-Do, In Progress, Done): ").strip().capitalize()

    if column_choice not in tasks or not tasks[column_choice]:
        print("Invalid column or no tasks available.")
        return

    task_id = int(input("Enter the WaddleTask number to edit: ")) - 1 # -1 cuz it 0 in comp language

    if 0 <= task_id < len(tasks[column_choice]): #checks if that task is within valid bounds
        print("Leave fields blank to keep current values.")
        task = tasks[column_choice][task_id]

        title = input(f"New title ({task['title']}): ").strip()
        description = input(f"New description ({task['description']}): ").strip()
        due_date_str = input(f"New due date ({task['due_date']}): ").strip()
        priority = input(f"New priority ({task['priority']}): ").strip().capitalize()

        task["title"] = title or task["title"]
        task["description"] = description or task["description"]
        task["due_date"] = due_date_str or task["due_date"]
        task["priority"] = priority or task["priority"]

        save_tasks(filename, username, tasks)
        print("WaddleTask updated successfully!")
    else:
        print("Invalid Waddletask number.")

# Function to delete a task
def delete_task(tasks, filename, username):
    list_tasks(tasks)
    column_choice = input("Enter the column where the WaddleTask exists (To-Do, In Progress, Done): ").strip().capitalize()

    if column_choice not in tasks or not tasks[column_choice]:
        print("Invalid column or no tasks available.")
        return

    task_id = int(input("Enter the WaddleTask number to delete: ")) - 1

    if 0 <= task_id < len(tasks[column_choice]):
        tasks[column_choice].pop(task_id)
        save_tasks(filename, username, tasks)
        print("WaddleTask deleted successfully!")
    else:
        print("Invalid WaddleTask number.")

# Function to handle user login
def login(filename):
    print("\n LOGIN ")
    username = input("Enter username: ").strip()

    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("User data not found. Please register first.")
        return None

    if username in data["users"]:
        password = input("Enter password: ").strip()
        if data["users"][username]["password"] == password:
            print(f"Welcome back, {username}!")
            return username
        else:
            print("Incorrect password!")
            return None
    else:
        print("Username not found! Please register first.")
        return None

# Function to handle user registration
def register(filename):
    print("\n REGISTER ")
    username = input("Enter username: ").strip()

    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"users": {}}

    if username in data["users"]:
        print("Username already exists! Please log in.")
        return None
    else:
        password = input("Enter password: ").strip()
        data["users"][username] = {
            "password": password,
            "tasks": {"To-Do": [], "In Progress": [], "Done": []}
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"User '{username}' registered successfully!")
        return username

# Main menu function
def main():
    filename = "user_data.json"

    while True:
        print("\n WADDLEBOARD ")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = register(filename)
            if username:
                with open(filename, 'r') as file:
                    data = json.load(file)
                tasks = data["users"][username]["tasks"]
                task_menu(tasks, filename, username)

        elif choice == "2":
            username = login(filename)
            if username:
                with open(filename, 'r') as file:
                    data = json.load(file)
                tasks = data["users"][username]["tasks"]
                task_menu(tasks, filename, username)

        elif choice == "3":
            print("Goodbye! Have a great day!")
            break
        else:
            print("Invalid option! Please try again.")

# Task menu function after login/registration
def task_menu(tasks, filename, username):
    while True:
        print("\n WADDLETASK MENU ")
        print("1. All Tasks")
        print("2. Create Task")
        print("3. Exit")

        task_choice = input("Choose an option: ").strip()

        if task_choice == "1":
            all_tasks_menu(tasks, filename, username)
        elif task_choice == "2":
            create_task(tasks, filename, username)
        elif task_choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    main()