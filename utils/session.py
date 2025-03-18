import json
import os

class Session:
    # Define the session file path relative to the project structure
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Gets E:\Users\ploan\python_EAUT\BTL
    SESSION_FILE = os.path.join(BASE_DIR, "view", "utils", "session.json")  # Full path to session.json
    current_user = None

    @staticmethod
    def set_user(user):
        """Lưu thông tin tài khoản sau khi đăng nhập vào file"""
        Session.current_user = user
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(Session.SESSION_FILE), exist_ok=True)
            with open(Session.SESSION_FILE, "w", encoding="utf-8") as file:
                json.dump(user, file, ensure_ascii=False)  # Proper Unicode support
            return True
        except (IOError, json.JSONEncodeError) as e:
            print(f"Error saving session: {e}")
            return False

    @staticmethod
    def get_user():
        """Lấy thông tin tài khoản từ file nếu có"""
        if Session.current_user is not None:
            return Session.current_user

        if os.path.exists(Session.SESSION_FILE):
            try:
                with open(Session.SESSION_FILE, "r", encoding="utf-8") as file:
                    user = json.load(file)
                    Session.current_user = user
                    return user
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading session: {e}")
                return None
        return None

    @staticmethod
    def clear():
        """Đăng xuất khỏi hệ thống và xóa file session"""
        Session.current_user = None
        if os.path.exists(Session.SESSION_FILE):
            try:
                os.remove(Session.SESSION_FILE)
                return True
            except OSError as e:
                print(f"Error clearing session: {e}")
                return False
        return True