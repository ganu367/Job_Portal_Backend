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
from os import getcwd
import base64
# import datetime
from datetime import datetime
from pyfa_converter.depends import QueryDepends, FormDepends, PyFaDepends

current_datetime = datetime.now()
dt = current_datetime
schedule_time = str(current_datetime)

router = APIRouter(prefix="/api", tags=["Candidate Interview"])

get_db = database.get_db


@router.post("/employer/job/schedule-interview/{jobID}/{candID}")
def interviewSchedule(jobID: int, candID: int, request: schemas.InterviewBase, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    jobCandidate = db.query(models.JobCandidate).filter(
        models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candID).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):
            if db.query(models.JobCandidate).filter(models.JobCandidate.id == jobCandidate.id).first():
                
                intdate=datetime.strptime(request.interview_date,'%Y-%m-%d').date()

                new_schedeule_interview = models.JobCandidateInterView(
                    job_candidate_id=jobCandidate.id,interview_title=request.interview_title, interview_date=intdate, interview_time=request.interview_time, created_by=_username_)
                db.add(new_schedeule_interview)
                db.commit()
                db.refresh(new_schedeule_interview)

                return {f"Created Interview Schedule"}

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Candidate not found")

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")

@router.post("/employer/job/update-schedule-interview/{interviewID}")
def updadateInterviewSchedule(interviewID: int, request: schemas.InterviewBase, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):
            if db.query(models.JobCandidateInterView).filter(models.JobCandidateInterView.id == interviewID).first():

                intdate=datetime.strptime(request.interview_date,'%Y-%m-%d').date()

                db.query(models.JobCandidateInterView).filter(models.JobCandidateInterView.id == interviewID,
                                                              models.JobCandidateInterView.created_by == _username_).update({"interview_title": request.interview_title, "interview_date": intdate, "interview_time": request.interview_time, "created_by": _username_})
                db.commit()
                return {f"updated for Interview Scheduled"}

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Not found any interview schedule")

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/employer/job/get-interview/{interviewID}")
def getInterviewScheduleEmployer(interviewID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):
            if db.query(models.JobCandidateInterView).filter(models.JobCandidateInterView.id == interviewID).first():

                get_interview_schedule = db.query(models.JobCandidateInterView).filter(models.JobCandidateInterView.id == interviewID,
                                                                                       models.JobCandidateInterView.created_by == _username_).first()
                return get_interview_schedule

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Not found any interview schedule")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/candidate/job/get-interview/{interviewID}")
def getInterviewScheduleCandidate(interviewID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.is_active == True):

            if db.query(models.JobCandidateInterView).filter(models.JobCandidateInterView.id == interviewID).first():

                get_interview_schedule = db.query(models.JobCandidateInterView.interview_title, models.JobCandidateInterView.interview_date, models.JobCandidateInterView.interview_time).filter(models.JobCandidateInterView.id == interviewID,
                                                                                                                                                                                                 models.JobCandidateInterView.created_by == _username_).first()
                return get_interview_schedule

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Not found any interview schedule")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this candidate account not found")


@router.get("/employer/job/all-interview-schedules/{jobID}/{candID}")
def allInterviewSchedules(jobID: int, candID: int,db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    job_cand = db.query(models.JobCandidate).filter(
        models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candID).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):
            all_schedule = db.query(models.JobCandidateInterView).filter(
                models.JobCandidateInterView.created_by == _username_,
                models.JobCandidateInterView.job_candidate_id == job_cand.id).order_by(models.JobCandidateInterView.id.desc()).all()
            return all_schedule
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/candidate/all-interview-schedules-upcoming")
def allInterviewSchedulesCandidateUpcoming(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    job_cand = db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id).all()
    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.is_active == True):
            all_schedules = []
            for i in job_cand:
                interview_schedule = db.query(models.JobCandidateInterView.id,
                    models.JobCandidateInterView.interview_title,
                    models.JobCandidateInterView.interview_date,
                    models.JobCandidateInterView.interview_time,
                    models.JobCandidateInterView.interview_score,
                    models.JobPost.job_title,
                    models.Employer.company_name).filter(
                    models.JobCandidateInterView.job_candidate_id == i.id,
                    models.JobCandidateInterView.interview_score == None).filter(
                        models.JobPost.id == i.job_id,
                        models.Employer.id == models.JobPost.employer_id
                        ).order_by(models.JobCandidateInterView.interview_date).all()
                for j in interview_schedule:
                    all_schedules.append(j)
            return {"interviews": all_schedules}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this candidate is deleted")


@router.get("/candidate/all-interview-schedules-evaluated")
def allInterviewSchedulesCandidateEvaluated(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    job_cand = db.query(models.JobCandidate).filter(models.JobCandidate.candidate_id == val_candidate.id).all()

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.is_active == True):
            all_schedules = []
            for i in job_cand:
                interview_schedule = db.query(models.JobCandidateInterView.id,
                    models.JobCandidateInterView.interview_title,
                    models.JobCandidateInterView.interview_date,
                    models.JobCandidateInterView.interview_time,
                    models.JobCandidateInterView.interview_score,
                    models.JobPost.job_title,
                    models.Employer.company_name).filter(
                    models.JobCandidateInterView.job_candidate_id == i.id,
                    models.JobCandidateInterView.interview_score != None).filter(
                        models.JobPost.id == i.job_id,
                        models.Employer.id == models.JobPost.employer_id
                        ).order_by(models.JobCandidateInterView.interview_date.desc()).all()
                for j in interview_schedule:
                    all_schedules.append(j)
            return {"interviews": all_schedules}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.post("/employer/job/interview-evaluation/{interviewID}")
def InterviewEvaluation(interviewID: int, evalution_files: Optional[UploadFile] = File(None), interview_score: int = Form(...), interview_remarks: str = Form(...), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    print("evaluation files:", evalution_files)

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to schedule interview")

    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):
            if db.query(models.JobCandidateInterView).filter(models.JobCandidateInterView.id == interviewID).first():

                path = os.getcwd() + "\\employer\\" + str(val_employer.id) + "\\"+str(interviewID)

                if not os.path.exists(path):
                    os.makedirs(path)

                try:

                    if evalution_files is not None:
                        _new_interview_evaluation_file_ = str(
                            interviewID) + "_"+"ifile"+"_" + evalution_files.filename

                        content = evalution_files.file.read()
                        with open(os.path.join(path,  _new_interview_evaluation_file_), 'wb') as f:
                            f.write(content)

                        interview_evaluation_file_path = f"{os.getcwd()}\\employer\\{str(val_employer.id)}\\{str(interviewID)}\\{ _new_interview_evaluation_file_}"

                    else:

                        interview_evaluation_file_path = None

                    db.query(models.JobCandidateInterView).filter(models.JobCandidateInterView.id == interviewID,
                                                                  models.JobCandidateInterView.created_by == _username_).update({"interview_score": interview_score, "interview_remarks": interview_remarks, "interview_document": interview_evaluation_file_path, "created_by": _username_})
                    db.commit()

                finally:
                    if evalution_files is not None:
                        evalution_files.file.close()

                return {"updated for Interview evaluations"}

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Not found any interview schedule")

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")
