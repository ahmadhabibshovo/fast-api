from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import secrets

from .. import database, models, schemas, oauth2, utils
from ..social_utils import verify_google_token, verify_apple_token

router = APIRouter(prefix="/auth/social", tags=["Social Authentication"])

def handle_social_login(db: Session, email: str):
    """
    Helper function to check if a user exists by email.
    If not, creates a new user with a random secure password.
    Returns a JWT access token.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        # Create a strong random password for social login users since they don't have one
        random_password = utils.hash(secrets.token_urlsafe(32))
        
        user = models.User(email=email, password=random_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        
    # Create the access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/google", response_model=schemas.Token)
def google_login(request: schemas.SocialLoginRequest, db: Session = Depends(database.get_db)):
    """
    Exchange a Google ID Token for an API access token.
    """
    user_info = verify_google_token(request.token)
    
    if not user_info or not user_info.get("email"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Google token or email missing"
        )
        
    return handle_social_login(db, email=user_info["email"])

@router.post("/apple", response_model=schemas.Token)
def apple_login(request: schemas.SocialLoginRequest, db: Session = Depends(database.get_db)):
    """
    Exchange an Apple ID Token for an API access token.
    """
    user_info = verify_apple_token(request.token)
    
    if not user_info or not user_info.get("email"):
        # Note: Apple only returns the user's email on their FIRST ever login.
        # For a production app, you will need to map the Apple 'sub' (User ID) 
        # to the database user instead of relying purely on the email.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Apple token or email missing"
        )
        
    return handle_social_login(db, email=user_info["email"])
