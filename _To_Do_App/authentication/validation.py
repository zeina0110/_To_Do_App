import re
import bcrypt
from datetime import datetime
from typing import Tuple

class Validator:
    @staticmethod
    def validate_name(name: str, field_name: str) -> Tuple[bool, str]:
        try:
            if not name.strip():
                return False, f"{field_name} is required"
            if len(name.strip()) < 2 or len(name.strip()) > 50:
                return False, f"{field_name} must be between 2-50 characters"
            if not re.match(r'^[a-zA-Z\s\-]+$', name):
                return False, f"{field_name} should contain only English letters"
            return True, ""
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        try:
            if not email.strip():
                return False, "Email is required"
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                return False, "Invalid email format (user@example.com)"
            return True, ""
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        try:
            if not phone.strip():
                return False, "Phone is required"
            if not re.match(r'^(?:\+20|0020)1[0125]\d{8}$', phone):
                return False, "Invalid Egyptian phone number (start with +20 or 0020)"
            return True, ""
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    @staticmethod
    def validate_password(password: str, confirm_password: str) -> Tuple[bool, str]:
        try:
            if len(password) < 8:
                return False, "Password should be at least 8 characters"
            if not any(c.isupper() for c in password):
                return False, "Password should have at least one uppercase letter"
            if not any(c.isdigit() for c in password):
                return False, "Password should have at least one digit"
            if password != confirm_password:
                return False, "Passwords do not match"
            return True, ""
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date_obj <= datetime.now().date():
                return False, "Date must be in the future"
            return True, ""
        except ValueError:
            return False, "Invalid date format (YYYY-MM-DD)"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    @staticmethod
    def hash_password(password: str) -> str:
        try:
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        except Exception as e:
            raise Exception(f"Password hashing failed: {str(e)}")

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), hashed_password.encode())
        except Exception as e:
            raise Exception(f"Password verification failed: {str(e)}")