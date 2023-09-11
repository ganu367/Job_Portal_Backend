from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database
import models
import database
import os
from os import getcwd, remove
import base64
import hashlib
from random import randbytes
# from routers.email import Email
from datetime import datetime


router = APIRouter(prefix="/api/utility", tags=["Utility"])

get_db = database.get_db


@router.get("/send-file")
def sendFile(file_path: str):
    if os.path.exists(str(file_path)):

        # remove(str(file_path))
        with open(file_path, mode="rb") as image_file:
            image_string = base64.b64encode(image_file.read())
            return image_string
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found")


def deleteFile(file_path: str):
    if os.path.exists(str(file_path)):
        remove(str(file_path))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found")


@router.get("/get-logo")
def getLogo(db: Session = Depends(get_db)):
    logo_p = db.query(models.Admin.logo,
                      models.Admin.organisation_name).first()
    if logo_p:
        logo_path = logo_p.logo
        organisation_name = logo_p.organisation_name
    else:
        logo_path = None
    if logo_path != None and logo_p:
        if os.path.exists(str(logo_path)):
            with open(logo_path, mode="rb") as image_file:
                image_string = base64.b64encode(image_file.read())
                logo = image_string
        else:
            logo = None
    else:
        logo = None
        organisation_name = None

    return {"logo": logo, "organisation_name": organisation_name}



@router.get('/verifyemail/{token}')
def verify_me(token: str):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()

    result = models.Candidate.update({"verification_code": verification_code}, {
        "$set": {"verification_code": None, "is_active": True, "updated_at": datetime.utcnow()}}, new=True)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code or account already verified')

    return {
        "status": "success",
        "message": "Account verified successfully"
    }
