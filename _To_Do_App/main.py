from authentication.auth import AuthManager
from tasks.manager import TaskManager
from datetime import datetime
from typing import NoReturn

class ToDoApp:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.task_manager = TaskManager()
        self.current_user = None

    def run(self) -> NoReturn:
        print("\n=== To-Do App ===")
        while True:
            if not self.current_user:
                self._show_unauth_menu()
            else:
                self._show_reminders()
                self._show_auth_menu()

    def _show_unauth_menu(self) -> None:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.current_user = self.auth_manager.register()
            elif choice == "2":
                self.current_user = self.auth_manager.login()
            elif choice == "3":
                self._exit_app()
            else:
                print("Invalid choice! Please enter 1, 2 or 3")
                
        except Exception as e:
            print(f"Menu error: {str(e)}")

    def _show_auth_menu(self) -> None:
        print(f"\nWelcome, {self.current_user['first_name']}!")
        print("1. Task Management")
        print("2. Profile Settings")
        print("3. Logout")
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self._task_management()
            elif choice == "2":
                updated_user = self.auth_manager.update_profile(self.current_user['email'])
                if updated_user:
                    self.current_user = updated_user
            elif choice == "3":
                self.current_user = None
                print("Logged out successfully!")
            else:
                print("Invalid choice! Please enter 1, 2 or 3")
                
        except Exception as e:
            print(f"Menu error: {str(e)}")

    def _task_management(self) -> None:
        while True:
            print("\n=== Task Management ===")
            print("1. Create New Task")
            print("2. View All Tasks")
            print("3. Edit Task")
            print("4. Mark Task as Completed")
            print("5. Delete Task")
            print("6. Search Tasks")
            print("7. Filter Tasks")
            print("8. Back to Main Menu")
            
            try:
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    self.task_manager.create_task(self.current_user['email'])
                elif choice == "2":
                    self.task_manager.view_tasks(self.current_user['email'])
                elif choice == "3":
                    self.task_manager.update_task(self.current_user['email'])
                elif choice == "4":
                    self.task_manager.complete_task(self.current_user['email'])
                elif choice == "5":
                    self.task_manager.delete_task(self.current_user['email'])
                elif choice == "6":
                    self.task_manager.search_tasks(self.current_user['email'])
                elif choice == "7":
                    self.task_manager.filter_tasks(self.current_user['email'])
                elif choice == "8":
                    break
                else:
                    print("Invalid choice! Please enter a number between 1-8")
                    
            except Exception as e:
                print(f"Task management error: {str(e)}")

    def _show_reminders(self) -> None:
        try:
            tasks = self.task_manager.task_repo.get_user_tasks(self.current_user['email'])
            today = datetime.now().date()
            
            overdue = []
            upcoming = []
            
            for task in tasks:
                try:
                    due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                    days_left = (due_date - today).days
                    
                    if days_left < 0:
                        overdue.append(task)
                    elif 0 <= days_left <= 1:
                        upcoming.append(task)
                        
                except ValueError:
                    continue
            
            if overdue:
                print("\n⚠️ OVERDUE TASKS:")
                for task in overdue:
                    print(f"- {task['title']} (was due on {task['due_date']})")
            
            if upcoming:
                print("\n🔔 UPCOMING DEADLINES (within 24 hours):")
                for task in upcoming:
                    print(f"- {task['title']} (due on {task['due_date']})")
            
            if overdue or upcoming:
                input("\nPress Enter to continue...")
                
        except Exception as e:
            print(f"\nFailed to check reminders: {str(e)}")

    def _exit_app(self) -> NoReturn:
        print("\nGoodbye!")
        exit()

if __name__ == "__main__":
    try:
        app = ToDoApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApp closed by user")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")