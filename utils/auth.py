from typing import List, Optional
from utils.config import Config

class AuthManager:
    """Handles user authentication and Role-Based Access Control (RBAC)."""
    
    def __init__(self):
        self.users = Config.USERS
        
    def authenticate(self, email: str) -> bool:
        """Validates if a given email is a registered user."""
        return email in self.users
        
    def get_allowed_companies(self, email: str) -> List[str]:
        """Returns the list of companies a user is allowed to access."""
        return self.users.get(email, [])
        
    def get_all_mock_users(self) -> dict:
        """Returns all users and their access roles for UI display."""
        return self.users
