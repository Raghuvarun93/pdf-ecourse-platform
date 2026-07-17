from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import Profile
from app.schemas.auth import MeResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=MeResponse)
def get_me(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns the current user's profile. The profile row itself is created
    automatically by a Postgres trigger (handle_new_user) the moment someone
    signs up via Supabase Auth — this endpoint just reads it.
    """
    profile = db.query(Profile).filter(Profile.id == current_user.id).first()
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        name=profile.name if profile else None,
        avatar_url=profile.avatar_url if profile else None,
    )
