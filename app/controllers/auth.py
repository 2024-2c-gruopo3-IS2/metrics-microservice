
from fastapi import HTTPException, Header
import requests
from app.configs.config import settings


def get_admin_from_token(token: str = Header(None)) -> str:
        """
        This function gets the user from the token.
        """
        
        response = requests.get(
            settings.AUTH_SERVICE_URL + "/auth/get-email-from-token",
            headers={"Content-Type": "application/json"},
            json={"token": token}
        )
        if response.status_code == 200:
            return response.json().get("email")
        raise HTTPException(status_code=401, detail="Invalid token")