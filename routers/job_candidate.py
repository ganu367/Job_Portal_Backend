from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import database
import schemas
import models
import oauth2
import tokens
from typing import List, Optional
import psycopg2
import os
from routers.utility import deleteFile
from routers.email import SendEmailJobToEmployer, SendEmailJobToCandidate
from routers.whtsms import sendSms
from os import getcwd
import base64
import datetime
from pyfa_converter.depends import QueryDepends, FormDepends, PyFaDepends

now = datetime.datetime.now()
dt = now

router = APIRouter(prefix="/api", tags=["Job Candidate"])

get_db = database.get_db


# Candidate Operation On jobs-apply,withdrawn,view-all-job-applied,get-job-applied
@router.post("/candidate/job/apply-job/{jobID}")
def jobApplayCandidate(jobID: int, assignment_files: Optional[UploadFile] = File(None), answer_details_required: str = Form(None), cover_letter: str = Form(None), assignement_reply: str = Form(None), my_comment: str = Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if db.query(models.JobCandidate).count() == 0:
        current_jobApply_id = 1
    else:
        last_id = db.query(func.max(models.JobPost.id)).first()
        current_jobApply_id = last_id[0] + 1

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):
            if not db.query(models.JobPost).filter(models.JobPost.id == jobID).first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="jobs not found")
            else:
                employer_deatails = db.query(models.Employer.employer_name, models.Employer.username, models.Employer.mobile_number, models.JobPost.id, models.JobPost.job_title).select_from(
                    models.Employer).outerjoin(models.JobPost).filter(models.JobPost.id == jobID)

                if db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.job_id == jobID).first():
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail="already applied for a job")
                else:
                    path = os.getcwd() + "\\candidate\\" + str(val_candidate.id) + "\\job_apply"
                    if not os.path.exists(path):
                        os.makedirs(path)

                    try:

                        if assignment_files is not None:
                            _new_job_apply_file_ = str(
                                current_jobApply_id) + "_"+"japply"+"_" + assignment_files.filename

                            content = assignment_files.file.read()
                            with open(os.path.join(path, _new_job_apply_file_), 'wb') as f:
                                f.write(content)

                            new_job_apply_path = f"{os.getcwd()}\\candidate\\{val_candidate.id}\\job_apply\\{_new_job_apply_file_}"

                        else:
                            new_job_apply_path = None

                        new_apply = models.JobCandidate(job_id=jobID, candidate_id=val_candidate.id, ans_to_required_deatail=answer_details_required, cover_letter=cover_letter, assignment_reply=assignement_reply,
                                                        applied="Yes", status="applied", applied_on=dt, candidate_comment=my_comment, assignment_submission_file=new_job_apply_path, created_by=_username_)
                        db.add(new_apply)
                        db.commit()
                        db.refresh(new_apply)

                        SendEmailJobToEmployer(employer_deatails.first(
                        ).username, employer_deatails.first().employer_name, employer_deatails.first().job_title)
                        # SendEmailJobToEmployer(employer_deatails.first())
                        
                        #send what'sapp sms 
                        sendSms(employer_deatails.first().mobile_number, "new_application")

                    finally:
                        if assignment_files is not None:
                            assignment_files.file.close()

                    return {f"Successfully..! Your applied for a job"}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.put("/candidate/job/update-assessment/{jobID}")
def jobUpdatAassessmentCandidate(jobID: int, assignment_files: Optional[UploadFile] = File(None), answer_details_required: str = Form(None), cover_letter: str = Form(None), assignement_reply: str = Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if db.query(models.JobCandidate).count() == 0:
        current_jobApply_id = 1
    else:
        last_id = db.query(func.max(models.JobPost.id)).first()
        current_jobApply_id = last_id[0] + 1

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):
            if not db.query(models.JobPost).filter(models.JobPost.id == jobID).first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="jobs not found")
            else:

                # if db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.job_id == jobID).first():
                #     raise HTTPException(status_code=status.HTTP_302_FOUND,
                #                         detail="already applied for a job")
                # else:

                path = os.getcwd() + "\\candidate\\" + str(val_candidate.id) + "\\job_apply"
                if not os.path.exists(path):
                    get_path = os.makedirs(path)

                try:

                    if assignment_files is not None:
                        _new_job_apply_file_ = str(
                            current_jobApply_id) + "_"+"japply"+"_" + assignment_files.filename

                        content = assignment_files.file.read()
                        with open(os.path.join(path, _new_job_apply_file_), 'wb') as f:
                            f.write(content)

                        new_job_apply_path = f"{os.getcwd()}\\candidate\\{val_candidate.id}\\job_apply\\{_new_job_apply_file_}"

                    else:

                        new_job_apply_path = None

                    db.query(models.JobCandidate).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == val_candidate.id).update({"ans_to_required_deatail": answer_details_required, "cover_letter": cover_letter, "assignment_reply": assignement_reply,
                                                                                                                                                            "applied": "Yes", "status": "applied", "applied_on": dt, "assignment_submission_file": new_job_apply_path, "modified_by": _username_})
                    db.commit()

                finally:
                    if assignment_files is not None:
                        assignment_files.file.close()

                return {f"Successfully..! Assignment Updated"}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.put("/candidate/job/withdrawn-job/{jobID}")
def jobWithdrawnCandidate(jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):

            if not db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.job_id == jobID).first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="jobs not found")
            else:

                db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id,
                                                     models.JobCandidate.job_id == jobID).update({"withdrawn": "Yes", "status": "withdrawn", "withdrawn_on": dt, "modified_by": _username_})
                db.commit()

                return {f"You are application withdrawn for this job"}

        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.put("/candidate/job/reapply-job/{jobID}")
def jobWithdrawnReAppylCandidate(jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):

            if not db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.job_id == jobID).first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="jobs not found")
            else:

                db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id,
                                                     models.JobCandidate.job_id == jobID).update({"withdrawn": "No", "status": "applied", "applied_on": dt, "modified_by": _username_})
                db.commit()

                return {f"You are application withdrawn for this job"}

        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/candidate/job/all-applied-jobs-dashboard")
def viewJobsCandidate(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):

            show_aplied_jobs = db.query(models.JobCandidate.applied_on, models.JobCandidate.status, models.JobCandidate.job_id).filter(
                models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.applied == "Yes").order_by(models.JobCandidate.applied_on.desc()).all()

            all_applied_jobs = []

            for i in show_aplied_jobs:
                new_jobs = {"job_title": "", "company_name": "",
                            "applied_on": "", "status": "", "job_status": "", "id": ""}

                job_ids = i.job_id

                jobs = db.query(models.JobPost).filter(
                    models.JobPost.id == job_ids).first()

                total_applications = db.query(models.JobCandidate).filter(
                    models.JobCandidate.job_id == jobs.id).count()

                emp_ids = jobs.employer_id

                employer = db.query(models.Employer).filter(
                    models.Employer.id == emp_ids).first()

                new_jobs["job_title"] = jobs.job_title
                new_jobs["job_status"] = jobs.status
                new_jobs["id"] = jobs.id
                new_jobs["company_name"] = employer.company_name
                new_jobs["applied_on"] = i.applied_on
                new_jobs["status"] = i.status
                new_jobs["total_applications"] = total_applications

                all_applied_jobs.append(new_jobs)

            return all_applied_jobs

        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/candidate/job/get-applied-job/{jobID}")
def getJobsCandidate(jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):

            show_aplied_jobs = db.query(models.JobCandidate.applied_on, models.JobCandidate.status, models.JobCandidate.job_id).filter(
                models.JobCandidate.id == jobID, models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.applied == "Yes").all()

            all_applied_jobs = []
            for i in show_aplied_jobs:
                new_job = {"company_name": "",
                           "applied_on": "", "status": ""}

                job_ids = i.job_id
                job = db.query(models.JobPost).filter(
                    models.JobPost.id == job_ids).first()
                emp_id = job.employer_id
                employer = db.query(models.Employer).filter(
                    models.Employer.id == emp_id).first()

                new_job["job"] = job
                new_job["company_name"] = employer.company_name
                new_job["applied_on"] = i.applied_on
                new_job["status"] = i.status
                all_applied_jobs.append(new_job)

            return all_applied_jobs

        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/candidate/job/view-jobs/{page_number}")
def viewJobsCandidate(page_number: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):
            filter_for_jobs = db.query(models.JobCandidate.job_id).filter(
                models.JobCandidate.candidate_id == val_candidate.id)  # .subquery()

            total_open_job_posts = db.query(models.JobPost).filter(
                models.JobPost.status == "Open", ~models.JobPost.id.in_(filter_for_jobs)).count()

            job_posts = db.query(models.JobPost.id,
                                 models.JobPost.job_title,
                                 models.JobPost.job_desc,
                                 models.JobPost.job_location,
                                 models.JobPost.started_date,
                                 models.JobPost.job_tenuer,
                                 models.JobPost.job_type,
                                 models.JobPost.job_mode,
                                 models.Employer.company_name).filter(models.JobPost.employer_id == models.Employer.id, models.JobPost.status == "Open", ~models.JobPost.id.in_(filter_for_jobs)).order_by(models.JobPost.id.desc()).limit(5).offset((page_number-1)*5).all()

            # models.Employer.company_name).filter(models.JobPost.employer_id==models.Employer.id).order_by(models.JobPost.id.desc()).limit(5).offset((page_number-1)*5).all()

            return {"job_posts": job_posts, "total_open_job_posts": total_open_job_posts}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/candidate/job/view-applied-jobs/{page_number}")
def viewAppliedJobsCandidate(page_number: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):
            filter_for_jobs = db.query(models.JobCandidate.job_id).filter(models.JobCandidate.candidate_id == val_candidate.id,
                                                                          models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn").subquery()

            total_applied_job_posts = db.query(models.JobPost).filter(
                models.JobPost.status == "Open", models.JobPost.id.in_(filter_for_jobs)).count()

            job_posts = db.query(models.JobPost.id,
                                 models.JobPost.job_title,
                                 models.JobPost.job_desc,
                                 models.JobPost.job_location,
                                 models.JobPost.started_date,
                                 models.JobPost.job_tenuer,
                                 models.JobPost.job_type,
                                 models.JobPost.job_mode,
                                 models.JobCandidate.status,
                                 models.Employer.company_name).filter(models.JobCandidate.job_id == models.JobPost.id, models.JobCandidate.candidate_id == val_candidate.id, models.JobPost.employer_id == models.Employer.id, models.JobPost.status == "Open", models.JobPost.id.in_(filter_for_jobs)).order_by(models.JobPost.id.desc()).limit(5).offset((page_number-1)*5).all()

            return {"job_posts": job_posts, "total_applied_job_posts": total_applied_job_posts}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/candidate/job/view-withdrawn-jobs/{page_number}")
def viewWithdrawnJobsCandidate(page_number: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):
            filter_for_jobs = db.query(models.JobCandidate.job_id).filter(models.JobCandidate.candidate_id == val_candidate.id,
                                                                          models.JobCandidate.withdrawn == "Yes", models.JobCandidate.status == "withdrawn").subquery()

            total_applied_job_posts = db.query(models.JobPost).filter(
                models.JobPost.status == "Open", models.JobPost.id.in_(filter_for_jobs)).count()

            job_posts = db.query(models.JobPost.id,
                                 models.JobPost.job_title,
                                 models.JobPost.job_desc,
                                 models.JobPost.job_location,
                                 models.JobPost.started_date,
                                 models.JobPost.job_tenuer,
                                 models.JobPost.job_type,
                                 models.JobPost.job_mode,
                                 models.JobCandidate.status,
                                 models.Employer.company_name).filter(models.JobCandidate.job_id == models.JobPost.id, models.JobCandidate.candidate_id == val_candidate.id, models.JobPost.employer_id == models.Employer.id, models.JobPost.status == "Open", models.JobPost.id.in_(filter_for_jobs)).order_by(models.JobPost.id.desc()).limit(5).offset((page_number-1)*5).all()

            return {"job_posts": job_posts, "total_applied_job_posts": total_applied_job_posts}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/candidate/job/view-job-details/{status}/{id}")
def viewJobDetailsCandidate(id: int, status: str, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        get_job = db.query(models.JobPost).filter(
            models.JobPost.id == id).first()
        get_emp = db.query(models.Employer).filter(
            models.Employer.id == get_job.employer_id).first()

        if status == "applied":
            sub_application = db.query(models.JobCandidate).filter(
                models.JobCandidate.job_id == id, models.JobCandidate.candidate_id == val_candidate.id).first()
        elif status == "notApplied":
            sub_application = None

        if not get_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="job post not found")

        return {"JobPost": get_job, "JobEmployer": get_emp, "JobCandidate": sub_application}


# employer opereation like search-candidates,

@router.get("/employer/job/search-candidate/get-candidate-details/{candidateID}")
def getCandidateDetailsEmployer(candidateID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            candidate = db.query(models.Candidate).filter(
                models.Candidate.id == candidateID).first()

            if not candidate:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Candidates not found")
            else:
                return candidate

        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.get("/employer/job/search-candidate/candidates/{jobID}")
def candidateListEmployer(jobID: int, page_number: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            return db.query(models.Candidate).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.post("/employer/job/job-intrest/{jobID}/{candidateID}")
def jobInterestCandidate(jobID: int, candidateID: int, request: schemas.JobCandidateActions, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")

    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            # for i in candidateID:

            val_candiadte = db.query(models.JobCandidate).filter(
                models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candidateID).first()

            job_candidate_details = db.query(models.Candidate.username, models.Candidate.name, models.Candidate.mobile_number, models.JobPost.job_title, models.JobCandidate.status).select_from(
                models.JobCandidate).outerjoin(models.JobPost).outerjoin(models.Candidate).filter(models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID)
            if val_candiadte:

                db.query(models.JobCandidate).filter(
                    models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candidateID).update(
                    {"interested": "Yes", "interested_on": dt, "status": "intrested", "employer_comment": request.employer_comment, "modified_by": _username_})

                db.commit()

            else:

                new_intreste_candidate = models.JobCandidate(
                    job_id=jobID, candidate_id=candidateID, interested="Yes", interested_on=dt, status="interested", employer_comment=request.employer_comment, created_by=_username_)

                db.add(new_intreste_candidate)
            db.commit()
            db.refresh(new_intreste_candidate)

            SendEmailJobToCandidate(job_candidate_details.first().username, job_candidate_details.first(
            ).name, job_candidate_details.first().job_title, job_candidate_details.first().status)

            #send what'sapp sms 
            sendSms(job_candidate_details.first().mobile_number, "test1")

            return {"Intrested this candidates"}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.post("/employer/job/job-shortlist/{jobID}/{candidateID}")
def jobShortlistCandidate(jobID: int, candidateID: int, request: schemas.JobCandidateActions, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            # for i in candidateID:

            val_candiadte = db.query(models.JobCandidate).filter(
                models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).first()

            job_candidate_details = db.query(models.Candidate.username, models.Candidate.name, models.Candidate.mobile_number, models.JobPost.job_title, models.JobCandidate.status).select_from(
                models.JobCandidate).outerjoin(models.JobPost).outerjoin(models.Candidate).filter(models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID)

            if val_candiadte:
                db.query(models.JobCandidate).filter(
                    models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).update(
                    {"shortlisted": "Yes", "shortlisted_on": dt, "status": "shortlisted", "employer_comment": request.employer_comment, "modified_by": _username_})

            else:
                new_intreste_candidate = models.JobCandidate(
                    job_id=jobID, candidate_id=candidateID, shortlisted="Yes", shortlisted_on=dt, status="shortlisted", employer_comment=request.employer_comment, created_by=_username_)

                db.add(new_intreste_candidate)

            db.commit()
            SendEmailJobToCandidate(job_candidate_details.first().username, job_candidate_details.first(
            ).name, job_candidate_details.first().job_title, job_candidate_details.first().status)

            #send what'sapp sms 
            sendSms(job_candidate_details.first().mobile_number, "test1")

            return {"Shortlisted this candidate"}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.post("/employer/job/job-hire/{jobID}/{candidateID}")
def jobHireCandidate(jobID: int, candidateID: int, request: schemas.JobCandidateActions, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            # for i in candidateID:

            val_candiadte = db.query(models.JobCandidate).filter(
                models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).first()

            job_candidate_details = db.query(models.Candidate.username, models.Candidate.name, models.Candidate.mobile_number, models.JobPost.job_title, models.JobCandidate.status).select_from(
                models.JobCandidate).outerjoin(models.JobPost).outerjoin(models.Candidate).filter(models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID)

            if val_candiadte:
                db.query(models.JobCandidate).filter(
                    models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).update(
                    {"hired": "Yes", "hired_on": dt, "status": "hired", "employer_comment": request.employer_comment, "modified_by": _username_})

            else:
                new_intreste_candidate = models.JobCandidate(
                    job_id=jobID, candidate_id=candidateID, hired="Yes", hired_on=dt, status="hired", employer_comment=request.employer_comment, created_by=_username_)

                db.add(new_intreste_candidate)

            db.commit()
            SendEmailJobToCandidate(job_candidate_details.first().username, job_candidate_details.first(
            ).name, job_candidate_details.first().job_title, job_candidate_details.first().status)

            #send what'sapp sms 
            sendSms(job_candidate_details.first().mobile_number, "test1")

            return {"Hired this candidates"}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.post("/employer/job/job-reject/{jobID}/{candidateID}")
def jobRejectCandidate(jobID: int, candidateID: int, request: schemas.JobCandidateActions, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            # for i in candidateID:

            val_candiadte = db.query(models.JobCandidate).filter(
                models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).first()
            job_candidate_details = db.query(models.Candidate.username, models.Candidate.name, models.Candidate.mobile_number, models.JobPost.job_title, models.JobCandidate.status).select_from(
                models.JobCandidate).outerjoin(models.JobPost).outerjoin(models.Candidate).filter(models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID)
            if val_candiadte:
                db.query(models.JobCandidate).filter(
                    models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).update(
                    {"rejected": "Yes", "rejected_on": dt, "status": "rejected", "employer_comment": request.employer_comment, "modified_by": _username_})
                db.commit()

            else:
                new_intreste_candidate = models.JobCandidate(
                    job_id=jobID, candidate_id=candidateID, rejected="Yes", rejected_on=dt, status="rejected", employer_comment=request.employer_comment, created_by=_username_)

                db.add(new_intreste_candidate)
            db.commit()
            SendEmailJobToCandidate(job_candidate_details.first().username, job_candidate_details.first(
            ).name, job_candidate_details.first().job_title, job_candidate_details.first().status)

            #send what'sapp sms 
            sendSms(job_candidate_details.first().mobile_number, "test1")

            return {"Sent a request as Intrested"}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.put("/employer/job/candidate-evaluation/{jobID}/{candidateID}")
def jobCandidateEvaluation(jobID: int, candidateID: int, evalution_files: Optional[UploadFile] = File(None), evaluation_score: int = Form(...), evaluation_remark: str = Form(...), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")

    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            val_candiadte = db.query(models.JobCandidate).filter(
                models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).first()

            if val_candiadte:

                path = os.getcwd() + "\\employer\\" + str(val_employer.id) + "\\"+str(jobID)

                if not os.path.exists(path):
                    get_path = os.makedirs(path)

                try:

                    if evalution_files is not None:
                        _new_job_evaluation_file_ = str(
                            candidateID) + "_"+"evols"+"_" + evalution_files.filename

                        content = evalution_files.file.read()
                        with open(os.path.join(path,  _new_job_evaluation_file_), 'wb') as f:
                            f.write(content)

                        job_evaluation_file_path = f"{os.getcwd()}\\employer\\{str(val_employer.id)}\\{str(jobID)}\\{ _new_job_evaluation_file_}"

                    else:

                        job_evaluation_file_path = None

                    db.query(models.JobCandidate).filter(
                        models.JobCandidate.candidate_id == candidateID, models.JobCandidate.job_id == jobID).update(
                            {"evaluation_score": evaluation_score, "evaluation_mark": evaluation_remark, "evaluation_document": job_evaluation_file_path, "modified_by": _username_})

                    db.commit()
                finally:
                    if evalution_files is not None:
                        evalution_files.file.close()

                return {"updated for evaluations"}

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Candidates not found")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/all-applied-candidates/{jobID}/{page_number}")
def jobAppliedCandidatesEmployer(page_number: int, jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(
                models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status == "applied").subquery()
            # filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn").subquery()

            total_applied_candidates = db.query(models.JobCandidate).filter(
                models.JobCandidate.id.in_(filter_for_candidates)).count()

            applied_candidates = db.query(models.Candidate.id,
                                          models.Candidate.name,
                                          models.Candidate.current_location,
                                          models.Candidate.qualification,
                                          models.Candidate.skill,
                                          models.Candidate.total_no_of_years_exp,
                                          models.Candidate.total_no_of_month_exp,
                                          models.Candidate.profile_summery,
                                          models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.Candidate.id.in_(filter_for_candidates)).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()
            # models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes").all()

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/all-interested-candidates/{jobID}/{page_number}")
def jobInterestedCandidatesEmployer(page_number: int, jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(
                models.JobCandidate.job_id == jobID, models.JobCandidate.interested == "Yes", models.JobCandidate.status == "intrested").subquery()
            # filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn").subquery()

            total_applied_candidates = db.query(models.JobCandidate).filter(
                models.JobCandidate.id.in_(filter_for_candidates)).count()

            applied_candidates = db.query(models.Candidate.id,
                                          models.Candidate.name,
                                          models.Candidate.current_location,
                                          models.Candidate.qualification,
                                          models.Candidate.skill,
                                          models.Candidate.total_no_of_years_exp,
                                          models.Candidate.total_no_of_month_exp,
                                          models.Candidate.profile_summery,
                                          models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.Candidate.id.in_(filter_for_candidates)).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()
            # models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes").all()

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/all-shortlisted-candidates/{jobID}/{page_number}")
def jobShortlistedCandidatesEmployer(page_number: int, jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(
                models.JobCandidate.job_id == jobID, models.JobCandidate.shortlisted == "Yes", models.JobCandidate.status == "shortlisted").subquery()
            # filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn").subquery()

            total_applied_candidates = db.query(models.JobCandidate).filter(
                models.JobCandidate.id.in_(filter_for_candidates)).count()

            applied_candidates = db.query(models.Candidate.id,
                                          models.Candidate.name,
                                          models.Candidate.current_location,
                                          models.Candidate.qualification,
                                          models.Candidate.skill,
                                          models.Candidate.total_no_of_years_exp,
                                          models.Candidate.total_no_of_month_exp,
                                          models.Candidate.profile_summery,
                                          models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.Candidate.id.in_(filter_for_candidates)).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()
            # models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes").all()

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/all-hired-candidates/{jobID}/{page_number}")
def joblHiredCandidatesEmployer(page_number: int, jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(
                models.JobCandidate.job_id == jobID, models.JobCandidate.hired == "Yes", models.JobCandidate.status == "hired").subquery()
            # filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn").subquery()

            total_applied_candidates = db.query(models.JobCandidate).filter(
                models.JobCandidate.id.in_(filter_for_candidates)).count()

            applied_candidates = db.query(models.Candidate.id,
                                          models.Candidate.name,
                                          models.Candidate.current_location,
                                          models.Candidate.qualification,
                                          models.Candidate.skill,
                                          models.Candidate.total_no_of_years_exp,
                                          models.Candidate.total_no_of_month_exp,
                                          models.Candidate.profile_summery,
                                          models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.Candidate.id.in_(filter_for_candidates)).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()
            # models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes").all()

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/all-rejected-candidates/{jobID}/{page_number}")
def jobRejectedCandidatesEmployer(page_number: int, jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(
                models.JobCandidate.job_id == jobID, models.JobCandidate.rejected == "Yes", models.JobCandidate.status == "rejected").subquery()
            # filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn").subquery()

            total_applied_candidates = db.query(models.JobCandidate).filter(
                models.JobCandidate.id.in_(filter_for_candidates)).count()

            applied_candidates = db.query(models.Candidate.id,
                                          models.Candidate.name,
                                          models.Candidate.current_location,
                                          models.Candidate.qualification,
                                          models.Candidate.skill,
                                          models.Candidate.total_no_of_years_exp,
                                          models.Candidate.total_no_of_month_exp,
                                          models.Candidate.profile_summery,
                                          models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.Candidate.id.in_(filter_for_candidates)).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()
            # models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes").all()

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/all-withdrawn-candidates/{jobID}/{page_number}")
def jobWithdrawnCandidatesEmployer(page_number: int, jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(
                models.JobCandidate.job_id == jobID, models.JobCandidate.withdrawn == "Yes", models.JobCandidate.status == "withdrawn").subquery()
            # filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn").subquery()

            total_applied_candidates = db.query(models.JobCandidate).filter(
                models.JobCandidate.id.in_(filter_for_candidates)).count()

            applied_candidates = db.query(models.Candidate.id,
                                          models.Candidate.name,
                                          models.Candidate.current_location,
                                          models.Candidate.qualification,
                                          models.Candidate.skill,
                                          models.Candidate.total_no_of_years_exp,
                                          models.Candidate.total_no_of_month_exp,
                                          models.Candidate.profile_summery,
                                          models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.Candidate.id.in_(filter_for_candidates)).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()
            # models.JobCandidate.status).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes").all()

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/get-selected-candidates/{status}/{jobID}/{candidateID}")
def jobHiredCandidatesEmployer(status: str, jobID: int, candidateID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            get_candidate = db.query(models.Candidate).filter(
                models.Candidate.id == candidateID).first()

            if status == "applied":
                sub_application = db.query(models.JobCandidate,
                                           func.sum(models.JobCandidateInterView.interview_score).label(
                                               "total_interview_score"),
                                           func.count(models.JobCandidateInterView.interview_score).label("total_interviews")).outerjoin(models.JobCandidateInterView).group_by(models.JobCandidateInterView.job_candidate_id).filter(
                    models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candidateID).first()
            elif status == "notApplied":
                sub_application = None

            if not get_candidate:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidate not found")

            return {"Candidate": get_candidate, "JobCandidate": sub_application}

            # return db.query(models.JobCandidate, models.Candidate).filter(models.JobCandidate.candidate_id == models.Candidate.id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candidateID).first()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/get-evaluation/{jobID}/{candidateID}")
def jobGetEvaluationEmployer(jobID: int, candidateID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            return db.query(models.JobCandidate.evaluation_score,
                            models.JobCandidate.evaluation_document,
                            models.JobCandidate.evaluation_mark).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candidateID).first()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/candidate/job/view-assignment/{jobID}")
def jobViewAssignmentCandidate(jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view assignment")
    else:
        if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            return db.query(models.JobCandidate.ans_to_required_deatail,
                            models.JobCandidate.cover_letter,
                            models.JobCandidate.assignment_reply,
                            models.JobCandidate.assignment_submission_file,
                            models.JobCandidate.candidate_comment).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == val_candidate.id).first()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this candidate is deleted")


@router.get("/candidate/job/view-assignment-questions/{jobID}")
def jobViewAssignmentQuestionsCandidate(jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view assignment")
    else:
        if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.is_active == True):

            if not db.query(models.JobPost).filter(models.JobPost.id == jobID).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            return db.query(models.JobPost.required_details,
                            models.JobPost.assignment,
                            models.JobPost.assignment_link,
                            models.JobPost.assignment_file).filter(models.JobPost.id == jobID).first()

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this candidate is deleted")


@router.put("/employer/job/update-comment/{jobID}/{candID}")
def jobUpdateCommentEmployer(jobID: int, candID: int, comment=Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_employer.is_deleted != True):
            if not db.query(models.JobPost).filter(models.JobPost.id == jobID).first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="jobs not found")
            else:

                db.query(models.JobCandidate).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candID).update(
                    {"employer_comment": comment, "modified_by": _username_})
                db.commit()

                return {f"Successfully..! Comment Updated"}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")


@router.put("/candidate/job/update-comment/{jobID}")
def jobUpdateCommentCandidate(jobID: int, comment=Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated")
    else:
        if (val_candidate.is_deleted != True):
            if not db.query(models.JobPost).filter(models.JobPost.id == jobID).first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="jobs not found")
            else:

                db.query(models.JobCandidate).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id ==
                                                     val_candidate.id).update({"candidate_comment": comment, "modified_by": _username_})
                db.commit()

                return {f"Successfully..! Comment Updated"}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")
