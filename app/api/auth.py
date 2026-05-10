from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from jose import jwt, JWTError
from app.core.config import settings
import traceback

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # التحقق من وجود الإيميل
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # تشفير الباسورد
        hashed_password = get_password_hash(user.password)
        
        # إنشاء المستخدم
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
            dietary_preferences=user.dietary_preferences
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    except Exception as e:
        # طباعة الخطأ في Logs عشان نعرف السبب الحقيقي
        print("❌ Register Error:")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500, 
            detail=f"Internal Server Error: {str(e)}"
        )


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        print("❌ Login Error:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Login failed")
