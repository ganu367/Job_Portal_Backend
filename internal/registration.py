from fastapi import APIRouter, Depends, status, HTTPException, Response, Form, UploadFile, File, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
import database
import schemas
import models
import hashing
import tokens
import oauth2
from routers import alerts
from routers import utility
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
import os
import hashlib

router = APIRouter(prefix="/auth", tags=["Registration"])

get_db = database.get_db

@router.post("/register/new-employer")
def NewRegisterEmployer(request_fields: schemas.EmployerRegister, request: Request, db: Session = Depends(get_db)):
    val_employer = db.query(models.Employer).filter(
        models.Employer.username == request_fields.username).first()

    if not val_employer:
        if db.query(models.Employer).count() == 0:
            current_employer_id = 1
        else:
            last_id = db.query(func.max(models.Employer.id)).first()
            current_employer_id = last_id[0] + 1

        # token = randbytes(10)
        employer_id_string = str(current_employer_id)
        hashedCode = hashlib.sha256()
        hashedCode.update(employer_id_string.encode('utf-8'))
        verification_code = hashedCode.hexdigest()

        new_employer = models.Employer(company_name=request_fields.company_name, country_code=request_fields.country_code,
                                       mobile_number=request_fields.mobile_number, username=request_fields.username, password=hashing.Hash.bcrypt(request_fields.password), verification_code=verification_code)
        db.add(new_employer)
        db.commit()
        db.refresh(new_employer)

        url = f"{request.url.scheme}://localhost:{3000}/employer/verified/{verification_code}"
        alerts.SendEmail(request_fields.username, url, "employer")

        access_token = tokens.create_access_token(data={"user": {
                                                  "username": request_fields.username, "userType": "employer", "isProfileCompleted": False, "isActive": False}})
        # return access_token
        return {f"We have sent a email on your email addresses. Check your Gmail!"}

    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Username already exists")


@router.post("/register/new-candidate")
def NewRegisterCandidate(request_fields: schemas.CandidateRegister, request: Request, db: Session = Depends(get_db)):
    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == request_fields.username).first()

    if not val_candidate:
        if db.query(models.Candidate).count() == 0:
            current_candidate_id = 1
        else:
            last_id = db.query(func.max(models.Candidate.id)).first()
            current_candidate_id = last_id[0] + 1

        # token = randbytes(10)
        candidate_id_string = str(current_candidate_id)
        hashedCode = hashlib.sha256()
        hashedCode.update(candidate_id_string.encode('utf-8'))
        verification_code = hashedCode.hexdigest()
        new_candidate = models.Candidate(name=request_fields.name, country_code=request_fields.country_code,
                                         mobile_number=request_fields.mobile_number, username=request_fields.username, password=hashing.Hash.bcrypt(request_fields.password), verification_code=verification_code)
        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)

        url = f"{request.url.scheme}://localhost:{3000}/candidate/verified/{verification_code}"
        alerts.SendEmail(request_fields.username, url, "candidate")
        access_token = tokens.create_access_token(data={"user": {
                                                  "username": request_fields.username, "userType": "candidate", "isProfileCompleted": False, "isActive": False}})
        # # return access_token

        return {f"We have sent a email on your email addresses. Check your Gmail!"}
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Username already exists")


@router.post("/register/new-admin")
def NewRegisterAdmin(organisation_name=Form(...), logo: UploadFile = File(...), username=Form(...), password=Form(...), db: Session = Depends(get_db)):
    if db.query(models.Admin).count() == 0:
        path = os.getcwd() + "\\admin" + "\\logo"

        if not os.path.exists(path):
            os.makedirs(path)

        try:
            if logo is not None:
                _new_logo_ = "logof" + "_" + logo.filename

                contents = logo.file.read()
                with open(os.path.join(path, _new_logo_), 'wb') as f:
                    f.write(contents)

                logo_path = f"{os.getcwd()}\\admin\\logo\\{_new_logo_}"

            new_admin = models.Admin(organisation_name=organisation_name, logo=logo_path,
                                     username=username, password=hashing.Hash.bcrypt(password))
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)

        finally:
            if logo is not None:
                logo.file.close()

        access_token = tokens.create_access_token(data={"user": {
                                                  "username": username, "userType": "admin", "isProfileCompleted": True, "isActive": True}})
        return access_token
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Admin already exists")
