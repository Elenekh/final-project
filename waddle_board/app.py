from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# File paths
USERS_FILE = "users.json"
TASKS_FILE = "tasks.json"

# Utility functions for users.json
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Utility functions for tasks.json
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Function to process date and check if it's valid
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

# Routes
@app.route('/')
def home():
    return render_template('first-page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not username or not password or not email:
            return "All fields are required. Please try again."
        
        users = load_users()

        for user in users:
            if user['email'] == email:
                return "Email already registered. Please log in."

        new_user = {"username": username, "password": password, "email": email}
        users.append(new_user)
        save_users(users)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        attempted_email = request.form['email']
        attempted_password = request.form['password']

        users = load_users()

        for user in users:
            if user["email"] == attempted_email and user['password'] == attempted_password:
                return redirect(url_for('main_page', username=user['username']))
            
        return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/mainpage/<username>', methods=['GET', 'POST'])
def main_page(username):
    tasks = load_tasks()
    user_tasks = tasks.get(username, {}).get("tasks", {})
    return render_template('mainpage.html', username=username, tasks=user_tasks)

@app.route('/tasks/<username>', methods=['POST'])
def create_task(username):
    tasks = load_tasks()

    if username not in tasks:
        tasks[username] = {
            "tasks": {
                "To-Do": [],
                "In Progress": [],
                "Completed": []
            }
        }

    task_data = request.form  # Using form data from the HTML form
    title = task_data.get('Title', '').strip()
    description = task_data.get('Description', '').strip()
    due_date_str = task_data.get('Due_date', '').strip()
    priority = task_data.get('Priority', '').strip().capitalize()

    # Ensure the task has valid data
    if not title or not description or not due_date_str or not priority:
        return jsonify({"error": "Missing required fields"}), 400

    # Ensure that the task is always added to the 'To-Do' column
    task = {
        "title": title,
        "description": description,
        "due_date": due_date_str,
        "priority": priority,
        "completed": False
    }

    # Add the task to the "To-Do" column
    tasks[username]["tasks"]["To-Do"].append(task)

    # Save the tasks to the file
    save_tasks(tasks)

    # Redirect the user to the main page
    return redirect(url_for('main_page', username=username))


@app.route('/edit_task/<username>/<column>/<int:task_id>', methods=['GET', 'POST'])
def edit_task(username, column, task_id):
    tasks = load_tasks()
    user_tasks = tasks.get(username, {}).get("tasks", {})

    if column not in user_tasks or task_id >= len(user_tasks[column]):
        return "Task not found", 404

    task = user_tasks[column][task_id]

    if request.method == 'POST':
        title = request.form.get('Title', '').strip()
        description = request.form.get('Description', '').strip()
        due_date_str = request.form.get('Due_date', '').strip()
        priority = request.form.get('Priority', '').strip().capitalize()

        task["title"] = title or task["title"]
        task["description"] = description or task["description"]
        task["due_date"] = due_date_str or task["due_date"]
        task["priority"] = priority or task["priority"]

        save_tasks(tasks)
        return redirect(url_for('main_page', username=username))

    return render_template('edit_task.html', task=task, username=username, column=column, task_id=task_id)

# Route for deleting a task
@app.route('/delete_task/<username>/<column>/<int:task_id>', methods=['POST'])
def delete_task(username, column, task_id):
    tasks = load_tasks()
    user_tasks = tasks.get(username, {}).get("tasks", {})

    if column not in user_tasks or task_id >= len(user_tasks[column]):
        return "Task not found", 404

    # Remove the task from the list
    user_tasks[column].pop(task_id)
    
    # Save the updated tasks to the file
    save_tasks(tasks)
    
    return redirect(url_for('main_page', username=username))

@app.route('/move_task/<username>/<task_id>', methods=['POST'])
def move_task(username, task_id):
    tasks = load_tasks()

    # Find the task by username and task_id
    task_id = int(task_id)
    task_found = False

    for column in tasks.get(username, {}).get('tasks', {}):
        task_list = tasks[username]["tasks"][column]
        if 0 <= task_id < len(task_list):
            task = task_list.pop(task_id)
            new_column = request.form['new_column']
            tasks[username]["tasks"][new_column].append(task)
            task_found = True
            break

    if task_found:
        save_tasks(tasks)
        return redirect(url_for('main_page', username=username))
    else:
        return "Task not found", 404



@app.route('/logout')
def log_out():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
