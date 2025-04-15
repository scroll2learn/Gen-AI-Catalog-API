from datetime import datetime, timezone
from typing import Dict, Optional
from fastapi import Depends, HTTPException, Header
import jwt
import logging
from fastapi.security import APIKeyHeader

from app.api.deps import get_context
from app.core.context import Context

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
logger = logging.getLogger(__name__)


ROLE_MATRIX = {
    "dashboard": {
        "ops-user": "view",
        "admin-user": "view",
        "designer-user": "view",
    },
    "designer": {
        "ops-user": "view",
        "admin-user": "view",
        "designer-user": "edit",
    },
    "ops_hub": {
        "ops-user": "edit",
        "admin-user": "view",
        "designer-user": "view",
    },
    "admin_module": {
        "ops-user": "view",
        "admin-user": "edit",
        "designer-user": "view",
    },
}

ALGORITHM = "HS256"


def decode_jwt_token(token: str) -> Optional[Dict]:
    """
    Decodes the provided JWT token and returns the payload

    Args:
        token (str): The JWT token to decode

    Returns:
        Optional[Dict]: The decoded payload or None if the decoding fails
    """
    try:
        # Decode the JWT token
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded
    except jwt.ExpiredSignatureError:
        logger.error("Token is expired")
    except jwt.InvalidSignatureError:
        logger.error("Invalid token signature")
    except jwt.DecodeError:
        logger.error("Invalid token")
    except Exception as e:
        logger.error(f"Unknown error: {str(e)}")
    return None


# Check if token is expired
def is_token_expired(decoded_token: Dict) -> bool:
    """
    Checks if the JWT token is expired

    Args:
        decoded_token (Dict): The decoded JWT token

    Returns:
        bool: True if the token is expired, False otherwise
    """
    # Get the expiration time from the decoded token
    exp = decoded_token.get("exp")

    # If the expiration time is not present, the token is invalid
    if exp is None:
        return True

    # Compare the current time with the expiration time
    # Use timezone-aware datetime comparison to handle different timezones
    return datetime.now(tz=timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc)


# Simulate checking if a user is active and refreshing the token
def refresh_token_if_active(user_id: str) -> Optional[str]:
    """
    Simulates checking if a user is active and refreshing the token

    This function is a placeholder for the actual implementation of checking
    if a user is active and refreshing the token. If the user is not active,
    it should return None.

    Args:
        user_id (str): The ID of the user to check

    Returns:
        Optional[str]: The new token if the user is active, None otherwise
    """
    # TODO: Implement the actual logic to check if the user is active
    # and refresh the token
    return None


# Custom exception for authorization
class AuthorizationException(HTTPException):
    """
    Custom exception for authorization

    This exception is raised when there is an issue with the authorization.
    It is used to return an HTTP 403 response with a message.

    Attributes:
        detail (str): The message to be returned in the response.
    """

    def __init__(self, detail: str = "Unauthorized"):
        """
        Initialize the exception

        Args:
            detail (str): The message to be returned in the response.
        """
        super().__init__(status_code=403, detail=detail)


# Dependency to handle token extraction and decoding
async def get_current_user(
    token: str = Depends(api_key_header),
) -> Dict:
    """
    Dependency to handle token extraction and decoding

    This dependency is used to extract the token from the request headers and
    decode it using the secret key. If the token is invalid or expired, it
    raises an HTTPException with a 403 status code.

    The dependency returns the decoded user data if the token is valid.

    Args:
        token (str): The token to be decoded.

    Returns:
        Dict: The decoded user data.
    """

    if not token:
        # Raise an exception if the token is missing
        raise HTTPException(status_code=403, detail="Token is missing")

    token = token.replace("Bearer ", "")
    decoded = decode_jwt_token(token)

    if not decoded:
        # Raise an exception if the token is invalid
        raise AuthorizationException(detail="Invalid token")

    if is_token_expired(decoded):
        user_id = decoded.get("user_id")
        new_token = refresh_token_if_active(user_id)
        if new_token:
            # Raise an exception to return a 200 status code with a new token
            raise HTTPException(
                status_code=200,
                detail={"message": "Token refreshed", "token": new_token},
            )
        # Raise an exception if the token is expired
        raise HTTPException(status_code=401, detail="Token expired")

    # Return the decoded user data
    return decoded


def authorize(api_module: str, action: str) -> Optional[Dict]:
    """
    Authorization decorator to check if a user is authorized based on their roles and the
    permissions defined in ROLE_MATRIX.

    Args:
        api_module (str): The API module being accessed (e.g., 'dashboard', 'admin_module').
        action (str): The action being performed (e.g., 'view', 'edit').

    Returns:
        Optional[Dict]: A dictionary with 'authorized' status and 'username' if permission is granted.
                        Raises an AuthorizationException if the user is not authorized.
    """

    async def wrapper(
        user: Dict = Depends(get_current_user), ctx: Context = Depends(get_context)
    ):
        """
        Inner function that checks if the user has the necessary permissions.

        Args:
            user (Dict): The current user's information, including their roles.

        Returns:
            Optional[Dict]: A dictionary with 'authorized' status and 'username' if authorized.

        Raises:
            AuthorizationException: If the user does not have permission for the requested action.
        """
        # Extract user roles from the realm_access part of the user data
        user_roles = set(user.get("realm_access", {}).get("roles", []))

        user_detail = await ctx.user_detail_service.get_or_create_user_detail(
            user.get("preferred_username"), user.get("email")
        )
        # Check if any of the user's roles grants the required access to the specified API module
        if any(
            # The walrus operator (:=) assigns the role's access level in the module to 'access' and
            # then checks if the access level matches the required action, or if 'view' is allowed when 'edit' is granted.
            (access := ROLE_MATRIX.get(api_module, {}).get(role)) == action
            or (action == "view" and access == "edit")
            for role in user_roles
        ):
            # if user is authorized then check if user present in user detail model
            # If the user has the required permission, return authorized status and the username
            return {
                "authorized": True,
                "username": user.get("preferred_username"),
                "user_detail_id": user_detail.user_detail_id,
            }

        # Raise an exception if the user does not have the required permissions
        raise AuthorizationException(detail="User does not have permission")

    return wrapper
