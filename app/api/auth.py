from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if user.email:
            existing_user = db.query(User).filter(User.email == user.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=400, 
                    detail="Email already registered"
                )

        hashed_password = None
        if user.password:
            hashed_password = get_password_hash(user.password)

        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            name=user.name,
            age=user.age,
            gender=user.gender,
            weight=user.weight,
            height=user.height,
            goal=user.goal,
            experience_level=user.experience_level,
            injuries=user.injuries,
            available_equipment=user.available_equipment,
            dietary_preferences=user.dietary_preferences,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print("❌ Register Error:")
        import traceback
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=60*24*7)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
