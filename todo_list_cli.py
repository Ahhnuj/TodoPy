import sys
import argparse
import os
import json
from datetime import datetime
from tabulate import tabulate  # type: ignore


TODO_LIST = []

def save_to_file():
    """Save tasks to a file in JSON format."""
    with open("todo_list.txt", "w", encoding="utf-8") as f:
        json.dump(TODO_LIST, f, ensure_ascii=False, indent=4)

def load_from_file():
    """Load tasks from a file in JSON format."""
    global TODO_LIST
    if os.path.exists("todo_list.txt"):
        try:
            with open("todo_list.txt", "r", encoding="utf-8") as f:
                TODO_LIST.extend(json.load(f))
        except (json.JSONDecodeError, ValueError):
            print("Error: Failed to load tasks from file. The file might be corrupted.")

def add_task(name):
    """Add a new task to the to-do list."""
    task = {
        "index": len(TODO_LIST) + 1,
        "name": name,
        "status": "❌",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None,
    }
    TODO_LIST.append(task)
    save_to_file()
    print(f"Task '{name}' added successfully!")

def delete_task(index):
    """Delete a task by its index."""
    try:
        index = int(index) - 1
        if 0 <= index < len(TODO_LIST):
            removed_task = TODO_LIST.pop(index)
            # Recalculate indices
            for i, task in enumerate(TODO_LIST):
                task["index"] = i + 1
            save_to_file()
            print(f"Task '{removed_task['name']}' deleted successfully!")
        else:
            print("Invalid task index.")
    except ValueError:
        print("Please provide a valid numeric index.")

def toggle_task(index):
    """Toggle the completion status of a task by its index."""
    try:
        index = int(index) - 1
        if 0 <= index < len(TODO_LIST):
            task = TODO_LIST[index]
            if task["status"] == "❌":
                task["status"] = "✅"
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                task["status"] = "❌"
                task["completed_at"] = None
            save_to_file()
            print(f"Task '{task['name']}' status toggled successfully!")
        else:
            print("Invalid task index.")
    except ValueError:
        print("Please provide a valid numeric index.")

def display_tasks():
    """Display all tasks in a tabular format."""
    if TODO_LIST:
        headers = ["Index", "Task Name", "Status", "Created At", "Completed At"]
        rows = [
            [
                task["index"],
                task["name"],
                task["status"],
                task["created_at"],
                task["completed_at"] or "--",
            ]
            for task in TODO_LIST
        ]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("No tasks in the to-do list.")

def main():
    """Main function to handle CLI arguments and commands."""
    parser = argparse.ArgumentParser(description="To-Do List CLI")
    parser.add_argument("command", help="Command to execute (add, delete, toggle, display)")
    parser.add_argument("--name", help="Name of the task (required for 'add' command)")
    parser.add_argument("--index", help="Index of the task (required for 'delete' and 'toggle' commands)")

    args = parser.parse_args()

    load_from_file()

    if args.command == "add" and args.name:
        add_task(args.name)
    elif args.command == "delete" and args.index:
        delete_task(args.index)
    elif args.command == "toggle" and args.index:
        toggle_task(args.index)
    elif args.command == "display":
        display_tasks()
    else:
        print("Invalid command or missing arguments. Use --help for usage information.")

if __name__ == "__main__":
    main()
