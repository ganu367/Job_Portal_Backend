from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
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
import datetime
from pyfa_converter.depends import QueryDepends, FormDepends, PyFaDepends

now = datetime.datetime.now()
dt = now

router = APIRouter(prefix="/api", tags=["Job Candidate Chat"])

get_db = database.get_db


@router.post("/candidate/chat/{jobID}")
def createChatCandidate(jobID: int, attached_files: Optional[UploadFile] = File(None), message: str = Form(...), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if db.query(models.JobCandidate).count() == 0:
        current_chat_id = 1
    else:
        last_id = db.query(func.max(models.JobPost.id)).first()
        current_chat_id = last_id[0] + 1

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to send a message")
    else:
        if (val_candidate.is_deleted != True):
            # val_job_candidate = db.query(models.JobCandidate).filter(
            #     models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == val_candidate.id).first()

            # if not val_job_candidate:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST, detail="Candidates not found")
            # else:

                path = os.getcwd() + "\\chat\\" + str(jobID)
                if not os.path.exists(path):
                    os.makedirs(path)

                try:

                    if attached_files is not None:
                        _new_chat_file_ = str(
                            current_chat_id) + "_"+"cfile"+"_" + attached_files.filename

                        content = attached_files.file.read()
                        with open(os.path.join(path, _new_chat_file_), 'wb') as f:
                            f.write(content)

                        new_job_chat_file_path = f"{os.getcwd()}\\chat\\{jobID}\\{_new_chat_file_}"

                    else:

                        new_job_chat_file_path = None

                    employer = db.query(models.JobPost).filter(
                        models.JobPost.id == jobID).first()

                    now = datetime.datetime.now()
                    dt = now

                    new_message = models.JobCandidateChat(job_id=jobID, candidate_id=val_candidate.id, employer_id=employer.employer_id, chat_date=dt,
                                                          chat_message=message, attatchment=new_job_chat_file_path, created_by=_username_)
                    db.add(new_message)
                    db.commit()
                    db.refresh(new_message)

                finally:
                    if attached_files is not None:
                        attached_files.file.close()

                return {f"sent a message to HR"}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this candidate is deleted")


@router.post("/employer/chat/{jobID}/{candidateID}")
def createChatEmployer(jobID: int, candidateID: int, attached_files: Optional[UploadFile] = File(None), message: str = Form(...), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if db.query(models.JobCandidate).count() == 0:
        current_chat_id = 1
    else:
        last_id = db.query(func.max(models.JobPost.id)).first()
        current_chat_id = last_id[0] + 1

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to send a message")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):
            # val_job_candidate = db.query(models.JobCandidate).filter(
            #     models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == candidateID).first()

            # if not val_job_candidate:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST, detail="Candidates not found")
            # else:

                path = os.getcwd() + "\\chat\\" + str(jobID)

                if not os.path.exists(path):
                    os.makedirs(path)

                try:
                    if attached_files is not None:

                        _new_chat_file_ = str(
                            current_chat_id) + "_"+"cfile"+"_" + attached_files.filename

                        content = attached_files.file.read()
                        with open(os.path.join(path, _new_chat_file_), 'wb') as f:
                            f.write(content)

                        new_job_chat_file_path = f"{os.getcwd()}\\chat\\{jobID}\\{_new_chat_file_}"

                    else:

                        new_job_chat_file_path = None

                    now = datetime.datetime.now()
                    dt = now

                    new_message = models.JobCandidateChat(job_id=jobID, candidate_id=candidateID, employer_id=val_employer.id, chat_date=dt,
                                                          chat_message=message, attatchment=new_job_chat_file_path, created_by=_username_)
                    db.add(new_message)
                    db.commit()
                    db.refresh(new_message)

                finally:
                    if attached_files is not None:
                        attached_files.file.close()
                return {f"sent a message to candidate"}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")


@router.get("/get-messages/{jobID}")
def getAllMessage(jobID: int, candidateID: int, db: Session = Depends(get_db)):

    employer = db.query(models.JobPost).filter(
        models.JobPost.id == jobID).first()

    message = db.query(models.JobCandidateChat).join(models.Employer.employer_name).filter(models.JobCandidateChat.job_id == jobID,
                                                       models.JobCandidateChat.candidate_id == candidateID, models.JobCandidateChat.employer_id == employer.employer_id, models.Employer.id== employer.employer_id).order_by(models.JobCandidateChat.chat_date).all()

    if message.count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="message not found")
    else:
        return message

@router.get("/get-chats-for-job/{jobID}")
def getChatsForJob(jobID: int, db: Session = Depends(get_db)):

    subq_for_last_msg = db.query(models.JobCandidateChat.candidate_id, func.max(models.JobCandidateChat.chat_date).label('maxdate')).filter(models.JobCandidateChat.job_id == jobID).group_by(models.JobCandidateChat.candidate_id).subquery('t2')

    # candidate_chats = db.query(models.Candidate.name,
    # models.Candidate.username,
    # models.JobCandidateChat.created_by,
    # models.JobCandidateChat.id,
    # models.JobCandidateChat.candidate_id,
    # models.JobCandidateChat.chat_date,
    # models.JobCandidateChat.chat_message,
    # models.JobCandidate.status).join(subq_for_last_msg, and_(models.JobCandidateChat.candidate_id == subq_for_last_msg.c.candidate_id, models.JobCandidateChat.chat_date == subq_for_last_msg.c.maxdate)).filter(models.Candidate.id == models.JobCandidateChat.candidate_id, models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == models.JobCandidateChat.candidate_id).order_by(models.JobCandidateChat.chat_date.desc()).all()
    
    candidate_chats = db.query(models.JobCandidateChat).join(subq_for_last_msg, and_(models.JobCandidateChat.candidate_id == subq_for_last_msg.c.candidate_id, models.JobCandidateChat.chat_date == subq_for_last_msg.c.maxdate)).order_by(models.JobCandidateChat.chat_date.desc()).all()
    
    for i in candidate_chats:
        candidate = db.query(models.Candidate).filter(models.Candidate.id == i.candidate_id).first()
        i.name = candidate.name
        i.username = candidate.username
        jobCandidate = db.query(models.JobCandidate).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.candidate_id == i.candidate_id).first()
        if jobCandidate:
            i.status = jobCandidate.status
        else:
            i.status = None

    return {"candidate_chats" : candidate_chats}

@router.get("/get-chats-for-candidate")
def getChatsForCandidate(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    subq_for_last_msg = db.query(models.JobCandidateChat.job_id, func.max(models.JobCandidateChat.chat_date).label('maxdate')).filter(models.JobCandidateChat.candidate_id == val_candidate.id).group_by(models.JobCandidateChat.job_id).subquery('t2')

    # employer_chats = db.query(models.JobPost.job_title,
    # models.JobPost.employer_id,
    # models.JobPost.id.label("job_id"),
    # models.Employer.company_name,
    # models.Employer.username,
    # models.JobCandidateChat.created_by,
    # models.JobCandidateChat.id,
    # models.JobCandidateChat.candidate_id,
    # models.JobCandidateChat.chat_date,
    # models.JobCandidateChat.chat_message,
    # models.JobCandidate.status).join(subq_for_last_msg, and_(models.JobCandidateChat.job_id == subq_for_last_msg.c.job_id, models.JobCandidateChat.chat_date == subq_for_last_msg.c.maxdate)).filter(models.JobPost.employer_id == models.Employer.id, models.JobPost.id == models.JobCandidateChat.job_id, models.JobCandidate.job_id == models.JobCandidateChat.job_id, models.JobCandidate.candidate_id == val_candidate.id).order_by(models.JobCandidateChat.chat_date.desc()).all()
    
    employer_chats = db.query(models.JobCandidateChat).join(subq_for_last_msg, and_(models.JobCandidateChat.job_id == subq_for_last_msg.c.job_id, models.JobCandidateChat.chat_date == subq_for_last_msg.c.maxdate)).order_by(models.JobCandidateChat.chat_date.desc()).all()
    
    for i in employer_chats:
        job = db.query(models.JobPost).filter(models.JobPost.id == i.job_id).first()
        i.job_title = job.job_title
        i.employer_id = job.employer_id
        i.job_id = job.id
        employer = db.query(models.Employer).filter(job.employer_id == models.Employer.id).first()
        i.company_name = employer.company_name
        i.username = employer.username
        jobCandidate = db.query(models.JobCandidate).filter(models.JobCandidate.job_id == i.job_id, models.JobCandidate.candidate_id == val_candidate.id).first()
        if jobCandidate:
            i.status = jobCandidate.status
        else:
            i.status = None

    return {"employer_chats" : employer_chats}

@router.get("/get-messages-with-cand/{jobID}/{candidateID}")
def getMessagesWithCand(jobID: int, candidateID: int, db: Session = Depends(get_db)):

    messages = db.query(models.Candidate.name,
    models.Candidate.username,
    models.JobCandidateChat.created_by,
    models.JobCandidateChat.id,
    models.JobCandidateChat.candidate_id,
    models.JobCandidateChat.chat_date,
    models.JobCandidateChat.chat_message).filter(models.Candidate.id == models.JobCandidateChat.candidate_id, models.JobCandidateChat.job_id == jobID, models.JobCandidateChat.candidate_id == candidateID).order_by(models.JobCandidateChat.chat_date).all()

    if (len(messages) != 0):
        candidate = db.query(models.Candidate.id, models.Candidate.name, models.Candidate.username, models.Candidate.current_location).filter(models.Candidate.id == models.JobCandidateChat.candidate_id, models.JobCandidateChat.job_id == jobID, models.JobCandidateChat.candidate_id == candidateID).first()
    else:
        candidate = db.query(models.Candidate.id, models.Candidate.name, models.Candidate.username, models.Candidate.current_location).filter(models.Candidate.id == candidateID).first()

    return {"messages" : messages, "candidate" : candidate}

@router.get("/get-messages-with-employer/{jobID}")
def getMessagesWithCand(jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    messages = db.query(models.JobPost.job_title,
    models.JobPost.employer_id,
    models.Employer.company_name,
    models.Employer.username,
    models.JobCandidateChat.created_by,
    models.JobCandidateChat.id,
    models.JobCandidateChat.candidate_id,
    models.JobCandidateChat.chat_date,
    models.JobCandidateChat.chat_message).filter(models.JobPost.employer_id == models.Employer.id, models.JobPost.id == jobID, models.JobCandidateChat.candidate_id == val_candidate.id, models.JobCandidateChat.job_id == jobID).order_by(models.JobCandidateChat.chat_date).all()

    if (len(messages) != 0):
        employer = db.query(models.JobPost.id.label("job_id"),models.Employer.id, models.Employer.company_name, models.Employer.username, models.JobPost.job_title).filter(models.JobPost.id == jobID, models.Employer.id == models.JobPost.employer_id, models.JobCandidateChat.job_id == jobID, models.JobCandidateChat.candidate_id == val_candidate.id).first()
    else:
        employer = db.query(models.JobPost.id.label("job_id"),models.Employer.id, models.Employer.company_name, models.Employer.username, models.JobPost.job_title).filter(models.JobPost.id == jobID, models.Employer.id == models.JobPost.employer_id).first()

    return {"messages" : messages, "employer" : employer}

@router.get("/employer/get-applied-candidates/{jobID}")
def getAppliedCandidatesEmployer(jobID: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
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

            # filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes").subquery()

            # applied_candidates =  db.query(models.Candidate.id,models.Candidate.name).filter(models.JobCandidateChat.candidate_id == models.Candidate.id, models.JobCandidateChat.job_id == jobID, models.Candidate.id.in_(filter_for_candidates)).order_by(models.Candidate.id.desc()).all()
            applied_candidates =  db.query(models.Candidate.id,models.Candidate.name).filter(models.JobCandidateChat.candidate_id == models.Candidate.id, models.JobCandidateChat.job_id == jobID).order_by(models.Candidate.id.desc()).distinct().all()
            
            return {"search_candidates": applied_candidates}
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")

@router.get("/candidate/get-applied-jobs")
def getAppliedJobsCandidate(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:

        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to create a job post")
    else:
        if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.is_deleted == False):

            if db.query(models.JobPost).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="no jobs")

            # filter_for_jobs = db.query(models.JobCandidate.job_id).filter(models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.applied == "Yes").subquery()

            # applied_jobs =  db.query(models.JobPost.id,models.JobPost.job_title).filter(models.JobCandidate.job_id == models.JobPost.id, models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.applied == "Yes", models.JobPost.id.in_(filter_for_jobs)).order_by(models.JobPost.id.desc()).all()
            applied_jobs =  db.query(models.JobPost.id,models.JobPost.job_title).filter(models.JobCandidateChat.job_id == models.JobPost.id, models.JobCandidateChat.candidate_id == val_candidate.id).order_by(models.JobPost.id.desc()).distinct().all()
            
            return {"search_jobs": applied_jobs}
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")
