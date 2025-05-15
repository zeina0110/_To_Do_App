from typing import Optional, Dict, List
from datetime import datetime
from .models import Task, TaskRepository
from authentication.validation import Validator

class TaskManager:
    def __init__(self):
        self.validator = Validator()
        self.task_repo = TaskRepository()

    def create_task(self, user_email: str) -> Optional[Dict]:
        print("\n=== Create New Task ===")
        try:
            title = self._get_valid_input("Task title: ", required=True)
            if not title:
                return None
                
            description = input("Task description (optional): ").strip()
            priority = self._get_valid_priority()
            status = self._get_valid_status()
            due_date = self._get_valid_date()
            
            new_task = Task(title, description, priority, status, due_date, user_email)
            self.task_repo.add_task(new_task)
            
            print("Task created successfully!")
            return new_task.to_dict()
            
        except Exception as e:
            print(f"\nTask creation failed: {str(e)}")
            return None

    def view_tasks(self, user_email: str) -> None:
        try:
            tasks = self.task_repo.get_user_tasks(user_email)
            if not tasks:
                print("\nNo tasks found.")
                return

            print("\n=== Your Tasks ===")
            for idx, task in enumerate(tasks, 1):
                print(f"\nTask #{idx}")
                print(f"Title: {task['title']}")
                print(f"Description: {task['description']}")
                print(f"Priority: {task['priority'].capitalize()}")
                print(f"Status: {task['status'].replace('_', ' ').capitalize()}")
                print(f"Due Date: {task['due_date']}")
                
        except Exception as e:
            print(f"\nFailed to view tasks: {str(e)}")

    def update_task(self, user_email: str) -> Optional[Dict]:
        print("\n=== Update Task ===")
        try:
            tasks = self.task_repo.get_user_tasks(user_email)
            if not tasks:
                print("No tasks found to update.")
                return None
                
            self.view_tasks(user_email)
            task_num = self._get_task_number(len(tasks))
            if task_num is None:
                return None
                
            task = tasks[task_num]
            print("\nLeave field blank to keep current value:")
            
            new_title = self._get_valid_input(
                f"Title [{task['title']}]: ",
                default=task['title']
            )
            
            new_desc = input(f"Description [{task['description']}]: ").strip() or task['description']
            new_priority = self._get_valid_priority(default=task['priority'])
            new_status = self._get_valid_status(default=task['status'])
            new_date = self._get_valid_date(default=task['due_date'])
            
            updated_task = {
                "title": new_title,
                "description": new_desc,
                "priority": new_priority,
                "status": new_status,
                "due_date": new_date
            }
            
            self.task_repo.update_task(task['title'], updated_task)
            print("Task updated successfully!")
            return updated_task
            
        except Exception as e:
            print(f"\nTask update failed: {str(e)}")
            return None

    def complete_task(self, user_email: str) -> bool:
        print("\n=== Complete Task ===")
        try:
            tasks = self.task_repo.get_user_tasks(user_email)
            if not tasks:
                print("No tasks found to complete.")
                return False
                
            self.view_tasks(user_email)
            task_num = self._get_task_number(len(tasks))
            if task_num is None:
                return False
                
            task = tasks[task_num]
            if task['status'] == 'completed':
                print("Task is already completed!")
                return False
                
            confirm = input(f"Mark '{task['title']}' as completed? (y/n): ").lower()
            if confirm == 'y':
                self.task_repo.update_task(
                    task['title'],
                    {"status": "completed"}
                )
                print("Task marked as completed!")
                return True
            return False
            
        except Exception as e:
            print(f"\nFailed to complete task: {str(e)}")
            return False

    def delete_task(self, user_email: str) -> bool:
        print("\n=== Delete Task ===")
        try:
            tasks = self.task_repo.get_user_tasks(user_email)
            if not tasks:
                print("No tasks found to delete.")
                return False
                
            self.view_tasks(user_email)
            task_num = self._get_task_number(len(tasks))
            if task_num is None:
                return False
                
            task = tasks[task_num]
            confirm = input(f"Are you sure you want to delete '{task['title']}'? (y/n): ").lower()
            
            if confirm == 'y':
                self.task_repo.delete_task(task['title'])
                print("Task deleted successfully!")
                return True
            return False
            
        except Exception as e:
            print(f"\nFailed to delete task: {str(e)}")
            return False

    def search_tasks(self, user_email: str) -> None:
        print("\n=== Search Tasks ===")
        try:
            search_term = input("Enter search term (task title): ").strip().lower()
            if not search_term:
                print("Please enter a search term.")
                return
                
            tasks = self.task_repo.get_user_tasks(user_email)
            results = [task for task in tasks if search_term in task['title'].lower()]
            
            if results:
                print(f"\nFound {len(results)} matching tasks:")
                self.view_tasks(user_email)  # Reuse view_tasks for consistent output
            else:
                print("No tasks found matching your search.")
                
        except Exception as e:
            print(f"\nSearch failed: {str(e)}")

    def filter_tasks(self, user_email: str) -> None:
        print("\n=== Filter Tasks ===")
        try:
            print("Filter by:")
            print("1. Priority")
            print("2. Status")
            print("3. Due Date")
            
            choice = input("Enter your choice (1-3): ").strip()
            tasks = self.task_repo.get_user_tasks(user_email)
            
            if choice == "1":
                priority = input("Enter priority (High/Medium/Low): ").strip().lower()
                filtered = [t for t in tasks if t['priority'] == priority]
                self._display_filtered(filtered, f"Priority: {priority}")
                
            elif choice == "2":
                status = input("Enter status (To_Do/In_Progress/Completed): ").strip().lower()
                filtered = [t for t in tasks if t['status'] == status]
                self._display_filtered(filtered, f"Status: {status}")
                
            elif choice == "3":
                date = input("Enter due date (YYYY-MM-DD): ").strip()
                filtered = [t for t in tasks if t['due_date'] == date]
                self._display_filtered(filtered, f"Due Date: {date}")
                
            else:
                print("Invalid choice!")
                
        except Exception as e:
            print(f"\nFilter failed: {str(e)}")

    def _get_valid_input(self, prompt: str, required: bool = False, default: str = "") -> str:
        while True:
            try:
                value = input(prompt).strip()
                if required and not value:
                    print("This field is required!")
                    continue
                return value or default
            except Exception as e:
                print(f"Input error: {str(e)}")

    def _get_valid_priority(self, default: str = "") -> str:
        while True:
            try:
                priority = input(
                    f"Priority (High/Medium/Low) [{default}]: "
                ).strip().lower() or default
                
                if priority in ["high", "medium", "low"]:
                    return priority
                print("Invalid priority! Please choose from High/Medium/Low")
            except Exception as e:
                print(f"Priority error: {str(e)}")

    def _get_valid_status(self, default: str = "to_do") -> str:
        while True:
            try:
                status = input(
                    f"Status (To_Do/In_Progress/Completed) [{default}]: "
                ).strip().lower() or default
                
                if status in ["to_do", "in_progress", "completed"]:
                    return status
                print("Invalid status! Please choose from To_Do/In_Progress/Completed")
            except Exception as e:
                print(f"Status error: {str(e)}")

    def _get_valid_date(self, default: str = "") -> str:
        while True:
            try:
                date_str = input(
                    f"Due date (YYYY-MM-DD) [{default}]: "
                ).strip() or default
                
                is_valid, error = self.validator.validate_date(date_str)
                if is_valid:
                    return date_str
                print(f"Error: {error}")
            except Exception as e:
                print(f"Date error: {str(e)}")

    def _get_task_number(self, max_tasks: int) -> Optional[int]:
        while True:
            try:
                task_num = input("Enter task number: ").strip()
                if not task_num:
                    return None
                    
                task_num = int(task_num) - 1
                if 0 <= task_num < max_tasks:
                    return task_num
                print(f"Please enter a number between 1 and {max_tasks}")
            except ValueError:
                print("Please enter a valid number!")
            except Exception as e:
                print(f"Error: {str(e)}")
                return None

    def _display_filtered(self, tasks: List[Dict], filter_type: str) -> None:
        if tasks:
            print(f"\nTasks filtered by {filter_type}:")
            for idx, task in enumerate(tasks, 1):
                print(f"\nTask #{idx}")
                print(f"Title: {task['title']}")
                print(f"Priority: {task['priority'].capitalize()}")
                print(f"Status: {task['status'].replace('_', ' ').capitalize()}")
                print(f"Due Date: {task['due_date']}")
        else:
            print(f"No tasks found for {filter_type}")