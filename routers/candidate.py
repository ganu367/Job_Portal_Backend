from fastapi import APIRouter, Depends, status,Body,Form,HTTPException, File, UploadFile
from sqlalchemy.orm import Session 
from sqlalchemy import func
import database, schemas, models,oauth2,tokens
from typing import List,Optional
import psycopg2,os
from routers.utility import deleteFile
from os import getcwd,remove
import base64
import datetime

now = datetime.datetime.now()
dt = now

router = APIRouter(prefix="/api/candidate",tags=["Candidate"])

get_db = database.get_db

@router.put("/profile/update-profile",status_code=status.HTTP_201_CREATED)
def UpdateProfileCandidate(photo_files:Optional[UploadFile] = File(None),resume_files:UploadFile = File(...),country_code =Form(...),mobile_number=Form(...),address  = Form(...),profile_summery = Form(...)
                ,video_profile = Form(None),total_no_of_years_exp = Form(...),total_no_of_month_exp = Form(...),prefered_job_location = Form(...),prefered_job_type = Form(...),prefered_job_tenuer = Form(...),prefered_job_mode  = Form(...)
                ,current_ctc = Form(...),excepted_ctc_min = Form(...),excepted_ctc_max = Form(None),qualification = Form(...),skill  = Form(...),current_location = Form(...),notice_period = Form(...),db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        
        current_candidate = current_user
        _username_ = current_candidate.user["username"]

        val_candidate = db.query(models.Candidate).filter(models.Candidate.username ==_username_).first()

        if not val_candidate:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            if (val_candidate.is_deleted != True):

                path = os.getcwd() + "\\candidate\\" + str(val_candidate.id)  +"\\docs"

                if not os.path.exists(path):
                    os.makedirs(path)
                    
                try:

                    if resume_files is not None:
                            _new_resume_file_ = str(val_candidate.id) +"_"+"rfile"+ "_" + resume_files.filename

                            contents = resume_files.file.read()
                            with open(os.path.join(path,_new_resume_file_),'wb') as f:
                                f.write(contents)

                            resume_files_path =  f"{os.getcwd()}\\candidate\\{val_candidate.id}\\docs\\{_new_resume_file_}"     

                            if photo_files is not None:
                                _new_photo_file_ = str(val_candidate.id) +"_"+"pfile"+ "_" +  photo_files.filename

                                contents = photo_files.file.read()
                                with open(os.path.join(path,_new_photo_file_),'wb') as f:
                                    f.write(contents)
                                
                                photo_files_path =  f"{os.getcwd()}\\candidate\\{val_candidate.id}\\docs\\{_new_photo_file_}"
                            
                            else:
                                        photo_files_path = None       

                            db.query(models.Candidate).filter(models.Candidate.username==_username_).update({"country_code":country_code,"mobile_number":mobile_number,"address":address,"current_location":current_location,
                            "photo":photo_files_path,
                            "resume":resume_files_path,
                            "profile_summery":profile_summery,
                            "prefered_job_location":prefered_job_location,
                            "video_profile" :video_profile,
                            "total_no_of_years_exp":total_no_of_years_exp,
                            "total_no_of_month_exp":total_no_of_month_exp,
                            "prefered_job_tenuer":prefered_job_tenuer,
                            "prefered_job_type" :prefered_job_type,
                            "prefered_job_mode":prefered_job_mode,
                            "current_ctc":current_ctc,
                            "excepted_ctc_min":excepted_ctc_min,
                            "excepted_ctc_max":excepted_ctc_max,
                            "qualification":qualification,
                            "skill":skill,
                            "notice_period":notice_period,
                            "isProfileCompleted":True,"created_by":_username_, "modified_by": _username_, "modified_on": dt})

                    db.commit()

                finally:
                     if photo_files is not None:
                        photo_files.file.close()

                     if resume_files is not None:
                        resume_files.file.close()

                access_token = tokens.create_access_token(data={"user":{"username": _username_,"userType" : "candidate", "isProfileCompleted":True}})
                
                if val_candidate.isProfileCompleted != True:
                    return {"msg": "Successfully! You are created a new account","access_token": access_token}

                return {"msg": "You are profile is updated","access_token": access_token}

            else:
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")

@router.get("/profile/view-profile")
def viewProfileCandidate(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_candidate = current_user
        _username_ = current_candidate.user["username"]

        val_candidate = db.query(models.Candidate).filter(models.Candidate.username ==_username_).first()

        if not val_candidate:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            if (val_candidate.is_deleted != True):

                my_profile =  db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id,models.Candidate.is_deleted==False).first()
                return my_profile
            
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Your profile is deleted")  
    
@router.delete("/account/deactivate-candidate")
def deleteAccountCandidate(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_employer = current_user
        _username_ = current_employer.user["username"]

        val_candidate = db.query(models.Candidate).filter(models.Candidate.username ==_username_).first()

        if not val_candidate:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated")
        else:
            if (val_candidate.is_deleted != True):
                
                db.query(models.Candidate).filter(models.Candidate.id==val_candidate.id ,models.Candidate.username==_username_).update({"is_deleted":True,"is_active":False,"username":"del_"+str(val_candidate.id)+"_"+_username_})
                db.commit()

                return {"Your account has been deleted."}

            else:
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="already account deleted")
                           