import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Import database functions
from app.main import insert_task, delete_task, update_task, get_task_by_id, get_all_tasks

# Create Flask app
app = Flask(__name__)


# Home page - show all tasks
@app.route("/", methods=['GET'])
def index():
    # Get all tasks from database
    tasks = get_all_tasks()

    # Sort tasks by id
    sorted_tasks = sorted(tasks, key=lambda x: x["id"])

    # Render HTML page with tasks
    return render_template("index.html", tasks=sorted_tasks)


# Add a new task
@app.route("/add", methods=['POST'])
def add():
    # Get task name from form input
    task_name = request.form.get("task")

    # Insert into database if not empty
    if task_name:
        insert_task(task_name)

    # Redirect back to homepage
    return redirect("/")


# Delete a task
@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete(task_id):
    # Delete task from database
    task = delete_task(task_id)

    # If task doesn't exist
    if not task:
        return {"error": "Task not found"}, 404
    
    return {"message": "Deleted"}


# Show edit page
@app.route("/tasks/<int:task_id>/edit", methods=['GET'])
def edit(task_id):
    # Get task by ID
    task = get_task_by_id(task_id)

    # If task doesn't exist
    if not task:
        return "Task not found", 404
    
    # Render edit page with task data
    return render_template("edit.html", task=task)


# Update a task
@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update(task_id):
    # Get JSON data from request
    data = request.get_json()

    # Update task in database
    task = update_task(task_id, data["name"])

    # If task doesn't exist
    if not task:
        return {"error": "Task not found"}, 404

    return {"message": "Updated", "task": task}


# Run the app
if __name__ == "__main__":
    app.run(debug=True)