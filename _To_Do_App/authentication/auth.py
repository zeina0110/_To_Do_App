from typing import Optional, Dict, Tuple
from .models import User, UserRepository
from .validation import Validator

class AuthManager:
    def __init__(self):
        self.validator = Validator()
        self.user_repo = UserRepository()

    def register(self) -> Optional[Dict]:
        print("\n=== User Registration ===")
        try:
            first_name = self._get_valid_input(
                "First name: ", 
                self.validator.validate_name, 
                ("First name",)
            )
            
            last_name = self._get_valid_input(
                "Last name: ", 
                self.validator.validate_name, 
                ("Last name",)
            )
            
            email = self._get_valid_input(
                "Email: ",
                self._validate_unique_email
            )
            
            password = self._get_valid_password()
            
            phone = self._get_valid_input(
                "Phone (+20 or 0020 format): ",
                self.validator.validate_phone
            )

            hashed_password = self.validator.hash_password(password)
            new_user = User(first_name, last_name, email, hashed_password, phone)
            self.user_repo.add_user(new_user)
            
            print("\nRegistration successful!")
            return new_user.to_dict()
            
        except Exception as e:
            print(f"\nRegistration failed: {str(e)}")
            return None

    def login(self) -> Optional[Dict]:
        print("\n=== User Login ===")
        try:
            email = input("Email: ").strip()
            password = input("Password: ")
            
            user = self.user_repo.find_by_email(email)
            if not user:
                print("Invalid email or password")
                return None
                
            if not self.validator.check_password(password, user["password"]):
                print("Invalid email or password")
                return None
                
            print(f"\nWelcome back, {user['first_name']}!")
            return user
            
        except Exception as e:
            print(f"\nLogin failed: {str(e)}")
            return None

    def update_profile(self, email: str) -> Optional[Dict]:
        print("\n=== Update Profile ===")
        try:
            user = self.user_repo.find_by_email(email)
            if not user:
                print("User not found!")
                return None

            print("\nLeave field blank to keep current value:")
            
            new_first = self._get_valid_input(
                f"First name [{user['first_name']}]: ",
                self.validator.validate_name,
                ("First name",),
                optional=True,
                default=user['first_name']
            )
            
            new_last = self._get_valid_input(
                f"Last name [{user['last_name']}]: ",
                self.validator.validate_name,
                ("Last name",),
                optional=True,
                default=user['last_name']
            )
            
            new_phone = self._get_valid_input(
                f"Phone [{user['phone_number']}]: ",
                self.validator.validate_phone,
                optional=True,
                default=user['phone_number']
            )

            updated_data = {
                "first_name": new_first,
                "last_name": new_last,
                "phone_number": new_phone
            }
            
            self.user_repo.update_user(email, updated_data)
            print("\nProfile updated successfully!")
            return {**user, **updated_data}
            
        except Exception as e:
            print(f"\nProfile update failed: {str(e)}")
            return None

    def _get_valid_input(self, prompt: str, validation_func: callable, 
                        validation_args: tuple = (), optional: bool = False,
                        default: str = "") -> str:
        while True:
            try:
                value = input(prompt).strip()
                if optional and not value:
                    return default
                    
                if validation_args:
                    is_valid, error = validation_func(value, *validation_args)
                else:
                    is_valid, error = validation_func(value)
                    
                if is_valid:
                    return value
                print(f"Error: {error}")
            except Exception as e:
                print(f"Input error: {str(e)}")

    def _validate_unique_email(self, email: str) -> Tuple[bool, str]:
        is_valid, error = self.validator.validate_email(email)
        if not is_valid:
            return False, error
        if self.user_repo.find_by_email(email):
            return False, "Email already registered"
        return True, ""

    def _get_valid_password(self) -> str:
        while True:
            try:
                password = input("Password: ")
                confirm_password = input("Confirm password: ")
                is_valid, error = self.validator.validate_password(password, confirm_password)
                if is_valid:
                    return password
                print(f"Error: {error}")
            except Exception as e:
                print(f"Password error: {str(e)}")