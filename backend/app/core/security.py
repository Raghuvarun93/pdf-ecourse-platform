"""
Verifies the Supabase JWT sent by the Next.js frontend on every request.

Flow:
  1. User logs in via Supabase Auth on the frontend (Google or email/password).
  2. Frontend attaches the Supabase access_token as: Authorization: Bearer <token>
  3. This dependency decodes + verifies it using the Supabase JWT secret
     (Project Settings > API > JWT Secret) and returns the user's id + email.

No separate login endpoint is needed on the backend — Supabase handles auth,
FastAPI just verifies the token Supabase already issued.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import get_settings

settings = get_settings()
bearer_scheme = HTTPBearer()


class CurrentUser:
    def __init__(self, id: str, email: str | None):
        self.id = id
        self.email = email


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing subject")

    return CurrentUser(id=user_id, email=payload.get("email"))
