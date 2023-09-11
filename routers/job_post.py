from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import database
import schemas
import models
import oauth2
from typing import List, Optional
import psycopg2
import os
from routers.utility import deleteFile
from os import getcwd, remove
import base64
import datetime

router = APIRouter(prefix="/api/employer/job", tags=["Job Post Employer"])

get_db = database.get_db


@router.post("/create-job")
def createJob(job_files: UploadFile = File(...), assignment_files: Optional[UploadFile] = File(None), title=Form(...), description=Form(...), qualification=Form(...), skill=Form(...), experience_min=Form(...), experience_max=Form(None), salary_min=Form(...), salary_max=Form(None), perks=Form(None), started_date=Form(None), job_function=Form(...), job_location=Form(...), job_tenuer=Form(...), job_type=Form(...), job_mode=Form(...), no_of_openings=Form(...), other_details=Form(None), required_details=Form(None), assignment=Form(None), assignment_link=Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if db.query(models.JobPost).count() == 0:
        current_jobPost_id = 1
    else:
        last_id = db.query(func.max(models.JobPost.id)).first()
        current_jobPost_id = last_id[0] + 1

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")

    else:

        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            employer_ids = val_employer.id
            path = os.getcwd() + "\\employer\\" + str(employer_ids) + "\\job_post"

            if not os.path.exists(path):
                os.makedirs(path)

            try:

                if job_files is not None:

                    _new_job_file_ = str(
                        current_jobPost_id) + "_"+"jfile"+"_" + job_files.filename

                    job_file_path = os.getcwd()+"\\employer\\"+str(employer_ids) + \
                        "\\job_post\\"+_new_job_file_

                    contents = job_files.file.read()

                    with open(os.path.join(path, _new_job_file_), 'wb') as f:
                        f.write(contents)

                    if assignment_files is not None:

                        _new_assignment_file_ = str(
                            current_jobPost_id) + "_"+"afile"+"_" + assignment_files.filename

                        contents = assignment_files.file.read()
                        with open(os.path.join(path, _new_assignment_file_), 'wb') as f:
                            f.write(contents)

                        assignment_files_path = f"{os.getcwd()}\\employer\\{employer_ids}\\job_post\\{_new_assignment_file_}"

                    else:

                        assignment_files_path = None
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="files is required")

                if started_date:
                    sdate=datetime.datetime.strptime(started_date,'%Y-%m-%d').date()
                else:
                    sdate=None

                new_job_post = models.JobPost(employer_id=employer_ids, job_title=title, job_desc=description,
                                              qualification=qualification, skill=skill, experience_min=experience_min,
                                              experience_max=experience_max, salary_min=salary_min, salary_max=salary_max, perks=perks,
                                              job_function=job_function, job_location=job_location, job_tenuer=job_tenuer, job_type=job_type, started_date=sdate, no_of_openings=no_of_openings,
                                              job_mode=job_mode, other_details=other_details, required_details=required_details,
                                              job_file=job_file_path, assignment=assignment, assignment_file=assignment_files_path, assignment_link=assignment_link, created_by=_username_, modified_by=_username_)

                db.add(new_job_post)
                db.commit()
                db.refresh(new_job_post)

            finally:
                if job_files is not None:
                    job_files.file.close()

                if assignment_files is not None:
                    assignment_files.file.close()

            return {"Successfully..! New job created."}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/all-jobs")
def allJobsEmployerPosted(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        all_job = db.query(models.JobPost).filter(
            models.JobPost.employer_id == val_employer.id).order_by(models.JobPost.created_on.desc()).all()

        for i in all_job:
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

        return all_job


@router.get("/get-jobs/{id}")
def getJobEmployerPosted(id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        get_job = db.query(models.JobPost).filter(
            models.JobPost.employer_id == val_employer.id, models.JobPost.id == id).first()

        if not get_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="job post not found")
        return get_job

@router.get("/get-job-status/{id}")
def getJobStatusEmployerPosted(id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        get_job = db.query(models.JobPost.status, models.JobPost.job_title).filter(
            models.JobPost.employer_id == val_employer.id, models.JobPost.id == id).first()

        if not get_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="job post not found")
        return get_job

@router.put("/update-job-post/{id}")
def updateJobPostEmployer(id: int, job_files: UploadFile = File(...), assignment_files: Optional[UploadFile] = File(None), title=Form(...), description=Form(...), qualification=Form(...), skill=Form(...), experience_min=Form(...), experience_max=Form(None), salary_min=Form(...), salary_max=Form(None), perks=Form(None), started_date=Form(None), job_function=Form(...), job_location=Form(...), job_tenuer=Form(...), job_type=Form(...), job_mode=Form(...), no_of_openings=Form(...), other_details=Form(None), required_details=Form(None), assignment=Form(None), assignment_link=Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to update a job post")
    else:
        val_job_post = db.query(models.JobPost).filter(
            models.JobPost.employer_id == val_employer.id, models.JobPost.id == id).first()

        if not val_job_post:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found job post")

        else:
            get_job = db.query(models.JobPost).filter(models.JobPost.employer_id == val_employer.id,
                                                      models.JobPost.id == id, models.JobPost.status == "Open").first()

            if not get_job:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="This job-jost closed")

            else:
                employer_ids = val_employer.id

                path = os.getcwd() + "\\employer\\" + str(employer_ids) + "\\job_post"

                if not os.path.exists(path):
                    get_path = os.makedirs(path)
                
                try:
                    
                    if job_files is not None:
                        get_job_file_path = val_job_post.job_file
                        
                        if os.path.exists(str(get_job_file_path)):
                            deleteFile(str(get_job_file_path))
                        
                        _new_job_file_ = str(
                            employer_ids) + "_"+"jfile"+"_" + job_files.filename
                        
                        job_file_path = os.getcwd()+"\\employer\\"+str(employer_ids) + \
                            "\\job_post\\"+_new_job_file_
                        
                        contents = job_files.file.read()
                        
                        with open(os.path.join(path, _new_job_file_), 'wb') as f:
                            f.write(contents)
                        
                        if assignment_files is not None:
                            get_assignment_file_path = val_job_post.assignment_file
                            if os.path.exists(str(get_assignment_file_path)):
                                deleteFile(str(get_assignment_file_path))

                            _new_assignment_file_ = str(
                                employer_ids) + "_"+"afile"+"_" + assignment_files.filename

                            contents = assignment_files.file.read()
                            with open(os.path.join(path, _new_assignment_file_), 'wb') as f:
                                f.write(contents)

                            assignment_files_path = f"{os.getcwd()}\\employer\\{employer_ids}\\job_post\\{_new_assignment_file_}"
                            
                        else:
                            assignment_files_path = None
                    
                    if started_date:
                        sdate=datetime.datetime.strptime(started_date,'%Y-%m-%d').date()
                    else:
                        sdate=None
                            
                    db.query(models.JobPost).filter(models.JobPost.id == id).update({"employer_id": employer_ids, "job_title": title, "job_desc": description,
                                                                                        "qualification": qualification, "skill": skill, "experience_min": experience_min,
                                                                                        "experience_max": experience_max, "salary_min": salary_min, "salary_max": salary_max, "perks": perks,
                                                                                        "job_function": job_function, "job_location": job_location, "job_tenuer": job_tenuer, "job_type": job_type, "started_date": sdate, "no_of_openings": no_of_openings,
                                                                                        "job_mode": job_mode, "other_details": other_details, "required_details": required_details, "assignment": assignment,
                                                                                        "job_file": job_file_path, "assignment_file": assignment_files_path, "assignment_link": assignment_link, "modified_by": _username_})
                    
                    db.commit()
                finally:

                    if job_files is not None:
                        job_files.file.close()

                    if assignment_files is not None:
                        assignment_files.file.close()

                    return {"Updated job post...!"}


@router.put("/closed-job/{id}")
def closedJobPostEmployer(id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:

        val_job_post = db.query(models.JobPost).filter(
            models.JobPost.employer_id == val_employer.id, models.JobPost.id == id).first()

        if not val_job_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="job post not found")
        else:

            get_job = db.query(models.JobPost).filter(models.JobPost.employer_id == val_employer.id,
                                                      models.JobPost.id == id, models.JobPost.status == "Open").first()
            if not get_job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="This job post closed")

            else:
                db.query(models.JobPost).filter(models.JobPost.employer_id == val_employer.id,
                                                models.JobPost.id == id, models.JobPost.status == "Open").update({"status": "Closed"})
                db.commit()

                return {f"Successsfullu..! You are closed this job post"}

# @router.get("/all-job-functions")
# def allJobsEmployerPosted(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
#     current_employer = current_user
#     _username_ = current_employer.user["username"]

#     val_employer = db.query(models.Employer).filter(
#         models.Employer.username == _username_).first()

#     if not val_employer:
#         raise HTTPException(status_code=status.HTTP_302_FOUND,
#                             detail="Not authenticated to view job functions")
#     else:
#         all_job_func = db.query(models.JobPost.job_function).filter(
#             models.JobPost.employer_id == val_employer.id).all()

#         return list(set(all_job_func))