import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class Task:
    def __init__(self, title: str, description: str, priority: str, 
                 status: str, due_date: str, owner: str):
        self.title = title
        self.description = description
        self.priority = priority.lower()
        self.status = status.lower()
        self.due_date = due_date
        self.owner = owner
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "owner": self.owner,
            "created_at": self.created_at
        }

class TaskRepository:
    def __init__(self, file_path: str = "data/tasks.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> List[Dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks: List[Dict]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

    def get_user_tasks(self, user_email: str) -> List[Dict]:
        tasks = self.load_tasks()
        return [task for task in tasks if task["owner"] == user_email]

    def find_task_by_title(self, user_email: str, title: str) -> Optional[Dict]:
        tasks = self.load_tasks()
        return next((task for task in tasks 
                    if task["owner"] == user_email and task["title"] == title), None)