from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database
import schemas
import models
import hashing
import tokens
import oauth2
from routers import alerts
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import hashlib

router = APIRouter(prefix="/auth", tags=["Authentication"])

get_db = database.get_db

#user_type = "employer"
#user_type = "candidate"

@router.post("/sign-in/{user_type}")
# @router.post("/sign-in")
def login(user_type: str, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # def employerLogin(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if user_type == "employer":
        val_employer = db.query(models.Employer).filter(
            models.Employer.username == request.username).first()
        
        if not val_employer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="user does not exists")
        else:
            if not (db.query(models.Employer).filter(val_employer.is_active == True, val_employer.is_deleted == False).first()):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="This account is deleted")
            else:

                today = datetime.now()
                lic_exp = db.query(models.Employer.expiry_date).filter(
                    models.Employer.id == val_employer.id).first()
                lic_expiry = lic_exp[0] + timedelta(days=1)

                if today > lic_expiry:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="License expired!")

                # verify password between requesting by a user & database password
                if not hashing.Hash.verify(val_employer.password, request.password):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="incorrect passwords")

                if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.address == None, models.Employer.employer_name == None, models.Employer.pan_number == None, models.Employer.profile == None).first():

                    access_token = tokens.create_access_token(data={"user": {
                                                              "username": request.username, "userType": "employer", "isProfileCompleted": False, "isActive": val_employer.is_active}})
                    return {"access_token": access_token, "token_type": "bearer"}

                else:

                    access_token = tokens.create_access_token(data={"user": {
                                                              "username": request.username, "userType": "employer", "isProfileCompleted": True, "isActive": val_employer.is_active}})
                    return {"access_token": access_token, "token_type": "bearer"}

    elif user_type == "candidate":
        val_candidate = db.query(models.Candidate).filter(
            models.Candidate.username == request.username).first()

        if not val_candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="user does not exists")
        else:
            if not (db.query(models.Candidate).filter(val_candidate.is_active == True, val_candidate.is_deleted == False).first()):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="this account is deleted")
            else:
                # verify password between requesting by a user & database password
                if not hashing.Hash.verify(val_candidate.password, request.password):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="incorrect passwords")

                if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.address == None, models.Candidate.current_location == None,
                                                     models.Candidate.profile_summery == None, models.Candidate.total_no_of_month_exp == None,
                                                     models.Candidate.total_no_of_years_exp == None, models.Candidate.skill == None, models.Candidate.qualification == None).first():

                    access_token = tokens.create_access_token(data={"user": {
                                                              "username": request.username, "userType": "candidate", "isProfileCompleted": False, "isActive": val_candidate.is_active}})
                    return {"access_token": access_token, "token_type": "bearer"}

                else:

                    access_token = tokens.create_access_token(data={"user": {
                                                              "username": request.username, "userType": "candidate", "isProfileCompleted": True, "isActive": val_candidate.is_active}})
                    return {"access_token": access_token, "token_type": "bearer"}

    else:
        val_admin = db.query(models.Admin).filter(
            models.Admin.username == request.username).first()

        if db.query(models.Admin).count() != 0:

            if not val_admin:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"{request.username} does not exists")
            else:
                if not hashing.Hash.verify(val_admin.password, request.password):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="incorrect passwords")

                access_token = tokens.create_access_token(data={"user": {
                    "username": request.username, "userType": "admin", "isProfileCompleted": True, "isActive": True}})
                return {"access_token": access_token, "token_type": "bearer"}

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Please register as admin!")


@router.put("/update-password", status_code=status.HTTP_202_ACCEPTED)
# @router.put("/reset-password", status_code=status.HTTP_202_ACCEPTED)
# def resetPassword(user_type:str, request: schemas.UserPassword, db: Session = Depends(get_db)):
def updatePassword(request: schemas.UserPassword, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    # current_user = current_user
    user_type = current_user.user["userType"]
    _username_ = current_user.user["username"]

    if user_type == "employer":

        val_user = db.query(models.Employer).filter(
            models.Employer.username == _username_).first()

        if not val_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="user does not exists")
        else:
            if not hashing.Hash.verify(val_user.password, request.current_password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="incorrect passwords")

            elif (request.new_password != request.confirm_password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="password does not matched")
            else:
                db.query(models.Employer).filter(models.Employer.username == _username_).update(
                    {"password": hashing.Hash.bcrypt(request.new_password)})
                db.commit()
                return {f"Password successfully updated"}
    elif user_type == "candidate":

        val_user = db.query(models.Candidate).filter(
            models.Candidate.username == _username_).first()

        if not val_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        else:
            if not hashing.Hash.verify(val_user.password, request.current_password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Incorrect Passwords")

            elif (request.new_password != request.confirm_password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Password not matched")
            else:

                db.query(models.Candidate).filter(models.Candidate.username == _username_).update(
                    {"password": hashing.Hash.bcrypt(request.new_password)})
                db.commit()
                return {f"Password successfully updated"}

    else:
        current_user = current_user
        _username_ = current_user.user["username"]

        val_user = db.query(models.Admin).filter(
            models.Admin.username == _username_).first()

        if not val_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Admin not found")
        else:
            if not hashing.Hash.verify(val_user.password, request.current_password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Incorrect Passwords")

            elif (request.new_password != request.confirm_password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Password does not matched")
            else:

                db.query(models.Admin).filter(models.Admin.username == _username_).update(
                    {"password": hashing.Hash.bcrypt(request.new_password)})
                db.commit()
                return {f"Password successfully updated"}

# @router.put("/forget-password/{user_type}/{username}")
@router.put("/forget-password/{username}")
async def ForgetPassword(user_type:str,username: str, request: schemas.ForgetPassword, db: Session = Depends(get_db)):
# async def ForgetPassword(username: str, request: schemas.ForgetPassword, db: Session = Depends(get_db)):
    try:

        if (request.new_password != request.confirm_password):

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Password doest not match")
        else:
            if user_type == "employer":
                db.query(models.Employer).filter(models.Employer.username == request.username).update(
                    {"password": hashing.Hash.bcrypt(request.new_password)})
            else:
                db.query(models.Candidate).filter(models.Candidate.username == request.username).update(
                    {"password": hashing.Hash.bcrypt(request.new_password)})
            db.commit()

            return {f"Password successfully updated"}
    except Exception as e:
        print(e)


@router.get('/verifyemail/{user_type}/{verification_code}')
def VerifyEmail(user_type: str, verification_code: str, db: Session = Depends(get_db)):
    if user_type == "employer":
        result = db.query(models.Employer).filter(
            models.Employer.verification_code == verification_code)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code')
        else:
            result.update({"is_active": True, "verification_code": None})
            db.commit()

        return {"Account verified successfully!"}

    else:
        result = db.query(models.Candidate).filter(
            models.Candidate.verification_code == verification_code)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code')
        else:
            result.update({"is_active": True, "verification_code": None})
            db.commit()

        return {"Account verified successfully!"}
