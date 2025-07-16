from typing import Optional

# Dummy admin user, ganti dengan query ke database pada implementasi nyata
ADMIN_USER = {
    "username": "admin",
    "password": "admin123"  # Gunakan hash password di produksi!
}

class User:
    def __init__(self, username: str):
        self.username = username
        self.role = "admin"

def authenticate_admin(username: str, password: str) -> Optional[User]:
    if username == ADMIN_USER["username"] and password == ADMIN_USER["password"]:
        return User(username)
    return None
