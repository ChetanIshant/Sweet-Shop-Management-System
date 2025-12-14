from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request
from . import auth, crud
from .database import get_session

# allow the dependency to NOT auto-raise so we can fallback / return clearer errors
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def get_current_user(token: Optional[str] = Depends(oauth2), request: Request = None, session=Depends(get_session)):
    """
    Resolve the current user from a bearer token.

    - Uses OAuth2PasswordBearer(tokenUrl, auto_error=False) so it won't auto-raise.
    - If OAuth2 dependency didn't return a token, try parsing Authorization header manually.
    - Raises explicit 401/403 HTTPExceptions for missing/invalid/expired token or missing/disabled user.
    """
    # fallback: try to read header manually if oauth2 didn't provide a token
    if not token and request is not None:
        auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")

    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token missing subject")

    user = crud.get_user(session, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # require verified accounts for protected endpoints
    if not getattr(user, "is_verified", False):
        raise HTTPException(status_code=403, detail="User email/ID not verified")

    return user