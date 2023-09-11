from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import database
import schemas
import models
import oauth2
import tokens
import datetime

now = datetime.datetime.now()
dt = now

router = APIRouter(prefix="/api/employer", tags=["Employer"])

get_db = database.get_db


@router.put("/profile/update-profile", status_code=status.HTTP_201_CREATED)
def updateProfileEmployer(request: schemas.EmployerProfileCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:

        if (val_employer.is_deleted != True):

            db.query(models.Employer).filter(models.Employer.username == _username_).update({"country_code": request.country_code, "mobile_number": request.mobile_number, "company_name": request.company_name, "address": request.address,
                                                                                             "employer_name": request.employer_name, "gst_number": request.gst_number, "pan_number": request.pan_number, "profile": request.profile, "web_url": request.web_url, "isProfileCompleted": True, "created_by": _username_, "modified_by": _username_, "modified_on": dt})
            db.commit()

            access_token = tokens.create_access_token(data={"user": {
                                                      "username": _username_, "userType": "employer", "isProfileCompleted": True}})

            if val_employer.isProfileCompleted != True:
                return {"msg": "Successfully! You are created a new account", "access_token": access_token}

            return {"msg": "You are profile is updated", "access_token": access_token}

        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/profile/view-profile")
def viewProfileEmployer(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_employer.is_deleted != True):

            my_profile = db.query(models.Employer.employer_name, models.Employer.country_code, models.Employer.company_name, models.Employer.mobile_number, models.Employer.username, models.Employer.address, models.Employer.profile,
                                  models.Employer.gst_number, models.Employer.pan_number, models.Employer.web_url).filter(models.Employer.id == val_employer.id, models.Employer.is_deleted == False).first()
            return my_profile

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Your profile is deleted")


@router.put("/account/deactivate-employer")
def deleteAccountEmployer(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_employer.is_deleted != True):

            employer = db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.username == _username_).update(
                {"is_deleted": True, "is_active": False, "company_name": "del_"+str(val_employer.id)+"_"+val_employer.company_name, "username": "del_"+str(val_employer.id)+"_"+_username_})
            db.commit()

            job_post = db.query(models.JobPost).filter(
                models.JobPost.employer_id == val_employer.id).update({"is_deleted": True})
            db.commit()

            if employer is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Employer's not found")

            if job_post is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Job Posts are not found")

            return {"Your account has been deleted"}

        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="already account deleted")
