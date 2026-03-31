from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from backend.services.base import BaseAIService # Inherit from BaseAIService if needed or a generic BaseService

class AuthService:
    """Service for handling authentication and user registration."""

    def __init__(self):
        # We could inject database session or user repository here
        pass

    def register_user(self, email: str, full_name: str) -> Dict[str, Any]:
        """Registers a new user."""
        try:
            # Placeholder for database logic
            data = {
                "email": email,
                "full_name": full_name,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            return self._standardize_response(data)
        except Exception as e:
            return self._error_response(f"Failed to register user: {str(e)}")

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticates a user and returns a token."""
        try:
            if "@" not in email:
                return self._error_response("Invalid credentials", status_code=401)

            # Placeholder for password check and token generation
            expires_at = datetime.now(timezone.utc) + timedelta(hours=12)
            data = {
                "access_token": f"demo-token-{email}",
                "token_type": "bearer",
                "expires_at": expires_at.isoformat(),
            }
            return self._standardize_response(data)
        except Exception as e:
            return self._error_response(f"Login failed: {str(e)}")

    def _standardize_response(self, data: Any) -> Dict[str, Any]:
        return {"status": "success", "data": data}

    def _error_response(self, message: str, status_code: int = 400) -> Dict[str, Any]:
        return {"status": "error", "message": message, "code": status_code}
