import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, TypeVar, Generic

T = TypeVar('T')

class BaseModel:
    def to_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

class BaseRepository(Generic[T]):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, items: List[Dict]) -> None:
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=4, ensure_ascii=False)
        except (IOError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to save data: {str(e)}")

    def load(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            raise Exception("Invalid JSON data in storage file")
        except Exception as e:
            raise Exception(f"Failed to load data: {str(e)}")

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, 
                 password: str, phone_number: str, is_active: bool = True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.is_active = is_active
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class UserRepository(BaseRepository):
    def __init__(self, file_path: str = "data/users.json"):
        super().__init__(file_path)

    def find_by_email(self, email: str) -> Optional[Dict]:
        try:
            users = self.load()
            return next((user for user in users if user["email"].lower() == email.lower()), None)
        except Exception as e:
            raise Exception(f"Error finding user: {str(e)}")

    def add_user(self, user: User) -> None:
        try:
            users = self.load()
            users.append(user.to_dict())
            self.save(users)
        except Exception as e:
            raise Exception(f"Error adding user: {str(e)}")

    def update_user(self, email: str, updated_data: Dict) -> None:
        try:
            users = self.load()
            user_index = next((i for i, u in enumerate(users) if u["email"] == email), None)
            
            if user_index is not None:
                users[user_index] = {**users[user_index], **updated_data}
                self.save(users)
        except Exception as e:
            raise Exception(f"Error updating user: {str(e)}")

class Task(BaseModel):
    def __init__(self, title: str, description: str, priority: str, 
                 status: str, due_date: str, owner: str):
        self.title = title
        self.description = description
        self.priority = priority.lower()
        self.status = status.lower()
        self.due_date = due_date
        self.owner = owner
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TaskRepository(BaseRepository):
    def __init__(self, file_path: str = "data/tasks.json"):
        super().__init__(file_path)

    def get_user_tasks(self, user_email: str) -> List[Dict]:
        try:
            tasks = self.load()
            return [task for task in tasks if task["owner"] == user_email]
        except Exception as e:
            raise Exception(f"Error getting user tasks: {str(e)}")

    def find_by_title(self, user_email: str, title: str) -> Optional[Dict]:
        try:
            tasks = self.load()
            return next((task for task in tasks 
                       if task["owner"] == user_email and task["title"].lower() == title.lower()), None)
        except Exception as e:
            raise Exception(f"Error finding task: {str(e)}")

    def add_task(self, task: Task) -> None:
        try:
            tasks = self.load()
            tasks.append(task.to_dict())
            self.save(tasks)
        except Exception as e:
            raise Exception(f"Error adding task: {str(e)}")

    def update_task(self, task_title: str, updated_data: Dict) -> None:
        try:
            tasks = self.load()
            task_index = next((i for i, t in enumerate(tasks) if t["title"] == task_title), None)
            
            if task_index is not None:
                tasks[task_index] = {**tasks[task_index], **updated_data}
                self.save(tasks)
        except Exception as e:
            raise Exception(f"Error updating task: {str(e)}")

    def delete_task(self, task_title: str) -> None:
        try:
            tasks = self.load()
            tasks = [task for task in tasks if task["title"] != task_title]
            self.save(tasks)
        except Exception as e:
            raise Exception(f"Error deleting task: {str(e)}")