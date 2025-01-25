from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json

app = Flask(__name__)

TASKS_FILE = "tasks.json"

# Load tasks data
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save tasks data
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

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

    task_data = request.json
    title = task_data.get('Title', '').strip()
    description = task_data.get('Description', '').strip()
    due_date_str = task_data.get('Due_date', '').strip()
    priority = task_data.get('Priority', '').strip().capitalize()
    column = task_data.get('Column', 'To-Do').strip()

    if not title or not description or not due_date_str or not priority:
        return jsonify({"error": "Missing required fields"}), 400

    if column not in tasks[username]["tasks"]:
        return jsonify({"error": "Invalid column"}), 400

    due_date = parse_date(due_date_str)
    if not due_date:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    task = {
        "title": title,
        "description": description,
        "due_date": due_date_str,
        "priority": priority,
        "completed": False
    }

    tasks[username]["tasks"][column].append(task)
    save_tasks(tasks)
    return jsonify({"message": "Task created successfully", "task": task}), 201
