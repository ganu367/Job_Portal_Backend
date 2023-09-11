from fastapi import APIRouter, Depends, status,Form,HTTPException, File, UploadFile
from sqlalchemy.orm import Session 
from sqlalchemy import func
import database, schemas, models,oauth2,tokens
from typing import List,Optional
import psycopg2,os
from routers.utility import deleteFile
from os import getcwd,remove
import base64
import datetime

router = APIRouter(prefix="/api/admin",tags=["Admin"])

get_db = database.get_db

@router.get("/profile/view-profile")
def viewProfileAdmin(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_admin = current_user
    _username_ = current_admin.user["username"]

    val_admin = db.query(models.Admin).filter(
        models.Admin.username == _username_).first()

    if not val_admin:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        my_profile = db.query(models.Admin).filter(models.Admin.id == val_admin.id).first()
        return my_profile

@router.put("/profile/update-profile",status_code=status.HTTP_201_CREATED)
def UpdateProfileAdmin(logo:Optional[UploadFile] = File(None),organisation_name =Form(...),username=Form(...),db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        
        current_admin = current_user
        _username_ = current_admin.user["username"]

        val_admin = db.query(models.Admin).filter(models.Admin.username ==_username_).first()

        if not val_admin:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            path = os.getcwd() + "\\admin\\logo"

            if not os.path.exists(path):
                os.makedirs(path)
                
            try:

                if logo is not None:
                    _new_logo_file_ = "logof"+ "_" + logo.filename

                    contents = logo.file.read()
                    with open(os.path.join(path,_new_logo_file_),'wb') as f:
                        f.write(contents)

                    logo_path =  f"{os.getcwd()}\\admin\\logo\\{_new_logo_file_}"     

                    db.query(models.Admin).filter(models.Admin.username==_username_).update({"organisation_name":organisation_name,"username":username,
                    "logo":logo_path})

                db.commit()

            finally:
                if logo is not None:
                    logo.file.close()

            access_token = tokens.create_access_token(data={"user":{"username": username,"userType" : "admin", "isProfileCompleted":True}})

            return {"msg": "You are profile is updated","access_token": access_token}

@router.get("/get-companies")
def AdminGetCompanies(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_admin = current_user
        _username_ = current_admin.user["username"]

        val_admin = db.query(models.Admin).filter(models.Admin.username ==_username_).first()

        if not val_admin:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            companies =  db.query(models.Employer.id,models.Employer.company_name).filter(models.Employer.is_deleted==False).order_by(models.Employer.company_name).all()
            return companies

@router.post("/get-license-values")
def AdminGetCompanies(request: schemas.LicenseValues, db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_admin = current_user
        _username_ = current_admin.user["username"]

        val_admin = db.query(models.Admin).filter(models.Admin.username ==_username_).first()

        if not val_admin:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            license_vals =  db.query(models.Employer.id,models.Employer.company_name,models.Employer.expiry_date,models.Employer.no_of_candidates_to_view).filter(models.Employer.is_deleted==False,models.Employer.company_name == request.company_name).first()
            return license_vals

@router.put("/update-license", status_code=status.HTTP_201_CREATED)
def updateLicense(request: schemas.LicenseBase, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_admin = current_user
    _username_ = current_admin.user["username"]

    val_admin = db.query(models.Admin).filter(
        models.Admin.username == _username_).first()

    if not val_admin:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        mdate=datetime.datetime.strptime(request.expiry_date,'%Y-%m-%d').date()
        db.query(models.Employer).filter(models.Employer.company_name == request.company_name).update({"expiry_date": mdate, "no_of_candidates_to_view": request.no_of_candidates_to_view, "modified_by": _username_})
        db.commit()

        return {"License updated!"}

@router.get("/get-employers")
def AdminGetEmployers(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_admin = current_user
        _username_ = current_admin.user["username"]

        val_admin = db.query(models.Admin).filter(models.Admin.username ==_username_).first()

        if not val_admin:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            companies =  db.query(models.Employer).order_by(models.Employer.company_name).all()
            return companies

@router.get("/get-jobs")
def AdminGetJobs(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_admin = current_user
        _username_ = current_admin.user["username"]

        val_admin = db.query(models.Admin).filter(models.Admin.username ==_username_).first()

        if not val_admin:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            jobs =  db.query(models.JobPost).order_by(models.JobPost.job_title).all()

            for i in jobs:
                job_id = i.id
                total_app = db.query(models.JobCandidate).filter(
                    models.JobCandidate.job_id == job_id, models.JobCandidate.applied == "Yes").count()
                i.total_app = total_app
                shortlist_app = db.query(models.JobCandidate).filter(models.JobCandidate.job_id == job_id,
                                                                    models.JobCandidate.shortlisted == "Yes", models.JobCandidate.status == "shortlisted").count()
                i.shortlist_app = shortlist_app
                hire_app = db.query(models.JobCandidate).filter(models.JobCandidate.job_id == job_id,
                                                                models.JobCandidate.hired == "Yes", models.JobCandidate.status == "hired").count()
                i.hire_app = hire_app
                reject_app = db.query(models.JobCandidate).filter(models.JobCandidate.job_id == job_id,
                                                                models.JobCandidate.rejected == "Yes", models.JobCandidate.status == "rejected").count()
                i.reject_app = reject_app
                employer_name = db.query(models.Employer.employer_name).filter(models.Employer.id == i.employer_id).first().employer_name
                i.employer_name = employer_name

            return jobs

@router.get("/get-candidates")
def AdminGetCandidates(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_admin = current_user
        _username_ = current_admin.user["username"]

        val_admin = db.query(models.Admin).filter(models.Admin.username ==_username_).first()

        if not val_admin:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            candidates =  db.query(models.Candidate).order_by(models.Candidate.name).all()

            return candidates

