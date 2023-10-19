from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database.models import TransactionType, UserDB
from sqlalchemy.orm import Session
from utils import pwd_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from api.dependencies import get_db, get_current_user
from database.schemas import RegisterUser, User
from database.models import UserDB, MonthlyReport
from datetime import timedelta
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)



def get_user(db: Session, email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = UserDB(email=user.email, fname=user.fname, sname=user.sname, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user_details")
def get_user_details(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = get_user(db, current_user.email)
    if db_user:
        monthly_report = db.query(MonthlyReport).filter(MonthlyReport.Email == current_user.email).first()
        
        if monthly_report:
            return {
                "email": db_user.email,
                "total_income": monthly_report.Total_Income,
                "total_expense": monthly_report.Total_Expense,
                "total_investment": monthly_report.Total_Investment
            }
        else:
            raise HTTPException(status_code=404, detail="Monthly report not found for the user")
    
    raise HTTPException(status_code=404, detail="User not found")
