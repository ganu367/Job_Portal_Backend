from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, case
import database,schemas,models,oauth2
from typing import List, Optional
import psycopg2
import os
from routers.utility import deleteFile
from os import getcwd, remove
import base64
import json

router = APIRouter(prefix="/search", tags=["Job Post Search"])

get_db = database.get_db

@router.get("/candidate/filter-values")
def allCandidateFilterValues(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        locations = db.query(models.JobPost.job_location).filter(
            models.JobPost.status == "Open").distinct().all()
        temp_loc_list = []
        for i in locations:
            new_loc = i.job_location.split(",")
            for j in new_loc:
                temp_loc_list.append(j.strip())

        skills = db.query(models.JobPost.skill).filter(
            models.JobPost.status == "Open").distinct().all()
        temp_skills_list = []
        for i in skills:
            new_loc = i.skill.split(",")
            for j in new_loc:
                temp_skills_list.append(j.strip())

        titles = db.query(models.JobPost.job_title).filter(
            models.JobPost.status == "Open").distinct().all()
        temp_titles_list = []
        for i in titles:
            new_loc = i.job_title.split(",")
            for j in new_loc:
                temp_titles_list.append(j.strip())

        qualifications = db.query(models.JobPost.qualification).filter(
            models.JobPost.status == "Open").distinct().all()
        temp_qualifications_list = []
        for i in qualifications:
            new_loc = i.qualification.split(",")
            for j in new_loc:
                temp_qualifications_list.append(j.strip())

        functions = db.query(models.JobPost.job_function).filter(
            models.JobPost.status == "Open").distinct().all()
        temp_functions_list = []
        for i in functions:
            new_loc = i.job_function.split(",")
            for j in new_loc:
                temp_functions_list.append(j.strip())

        return {"locations": list(set(temp_loc_list)), "skills": list(set(temp_skills_list)), "titles": list(set(temp_titles_list)), "qualifications": list(set(temp_qualifications_list)), "functions": list(set(temp_functions_list))}

@router.post("/candidate/filtered-jobs/{page_number}")
def allFilteredJobs(page_number: int, function: str = Form(None), location: str = Form(None), skill: str = Form(None), title: str = Form(None), qualification: str = Form(None), type: str = Form(None), mode: str = Form(None), tenure: str = Form(None), exp: int = Form(None), sal: int = Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        if (val_candidate.is_deleted != True):
            filter_for_jobs = db.query(models.JobCandidate.job_id).filter(models.JobCandidate.candidate_id == val_candidate.id) #.subquery()

            # total_open_job_posts = db.query(models.JobPost).filter(models.JobPost.status == "Open", ~models.JobPost.id.in_(filter_for_jobs)).count()

            filters = []

            if (location):
                locations = location.split(",")
                if len(locations) > 0 and ("Any" not in locations):
                    # loc_list = []
                    temp_locs = []
                    for i in locations:
                        temp_locs.append(i.strip())
                        # search = "%{}%".format(i.strip())
                        # loc_list.append(search)
                    filters.append(or_(*[models.JobPost.job_location.contains(i) for i in temp_locs], models.JobPost.job_location.contains("Any")))
                    # print("location: ",location)
                    # print("locations: ",locations)
                    # print("temp_locs: ",temp_locs)
                    # print("loc_list: ",loc_list)

                    # for i in locations:
                    #     filters.append(or_(models.JobPost.job_location.contains(i)))

                    # filters.append(or_(models.JobPost.job_location.like(or_(loc_list))))

            if (skill):
                skills = skill.split(",")
                if len(skills) > 0:
                    skill_list = []
                    for i in skills:
                        skill_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.skill.contains(i) for i in skill_list]))

            if (title):
                titles = title.split(",")
                if len(titles) > 0:
                    title_list = []
                    for i in titles:
                        title_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_title.contains(i) for i in title_list]))

            if (qualification):
                qualifications = qualification.split(",")
                if len(qualifications) > 0:
                    qualification_list = []
                    for i in qualifications:
                        qualification_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.qualification.contains(i) for i in qualification_list]))

            if (function):
                functions = function.split(",")
                if len(functions) > 0:
                    function_list = []
                    for i in functions:
                        function_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_function.contains(i) for i in function_list]))

            if (type):
                types = type.split(",")
                if len(types) > 0 and ("Any" not in types):
                    type_list = []
                    for i in types:
                        type_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_type.contains(i) for i in type_list], models.JobPost.job_type.contains("Any")))

            if (mode):
                modes = mode.split(",")
                if len(modes) > 0 and ("Any" not in modes):
                    mode_list = []
                    for i in modes:
                        mode_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_mode.contains(i) for i in mode_list], models.JobPost.job_mode.contains("Any")))

            if (tenure):
                tenures = tenure.split(",")
                if len(tenures) > 0 and ("Any" not in tenures):
                    tenure_list = []
                    for i in tenures:
                        tenure_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_tenuer.contains(i) for i in tenure_list], models.JobPost.job_tenuer.contains("Any")))

            if (exp):
                exp_filter = case([
                                    ((models.JobPost.experience_max != None), and_(models.JobPost.experience_max >= exp, models.JobPost.experience_min <= exp) ),
                                ],
                                else_ = models.JobPost.experience_min <= exp)
                filters.append(exp_filter)
            
            if (sal):
                sal_filter = case([
                                    ((models.JobPost.salary_max != None), (models.JobPost.salary_max >= sal)),
                                ],
                                else_ = models.JobPost.salary_max == None)
                filters.append(sal_filter)

            job_posts = db.query(models.JobPost.id,
            models.JobPost.job_title,
            models.JobPost.skill,
            models.JobPost.job_desc,
            models.JobPost.job_location,
            models.JobPost.started_date,
            models.JobPost.job_tenuer,
            models.JobPost.job_type,
            models.JobPost.job_mode,
            models.JobPost.experience_max,
            models.JobPost.experience_min,
            models.JobPost.salary_max,
            models.JobPost.salary_min,
            models.Employer.company_name).join(models.Employer).filter(models.JobPost.status == "Open", ~models.JobPost.id.in_(filter_for_jobs),*filters).order_by(models.JobPost.id.desc()).limit(5).offset((page_number-1)*5).all()
            # .filter(models.JobPost.employer_id==models.Employer.id, models.JobPost.status == "Open", ~models.JobPost.id.in_(filter_for_jobs)).order_by(models.JobPost.id.desc()).limit(5).offset((page_number-1)*5).all()
            
            total_jobs_count_for_filter = db.query(models.JobPost.id).filter(models.JobPost.status == "Open", ~models.JobPost.id.in_(filter_for_jobs),*filters).order_by(models.JobPost.id.desc()).count()


            return {"job_posts": job_posts, "total_open_job_posts": total_jobs_count_for_filter}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")

@router.post("/candidate/filtered-{status_type}-jobs/{page_number}")
def allStatusFilteredJobs(page_number: int, status_type: str, function: str = Form(None), location: str = Form(None), skill: str = Form(None), title: str = Form(None), qualification: str = Form(None), type: str = Form(None), mode: str = Form(None), tenure: str = Form(None), exp: int = Form(None), sal: int = Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_candidate = current_user
    _username_ = current_candidate.user["username"]

    val_candidate = db.query(models.Candidate).filter(
        models.Candidate.username == _username_).first()

    if not val_candidate:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        if (val_candidate.is_deleted != True):
            if status_type == "applied":
                filter_for_jobs = db.query(models.JobCandidate.job_id).filter(models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.applied == "Yes", models.JobCandidate.status != "withdrawn") #.subquery()
            elif status_type == "withdrawn":
                filter_for_jobs = db.query(models.JobCandidate.job_id).filter(models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.withdrawn == "Yes", models.JobCandidate.status == "withdrawn") #.subquery()

            filters = []

            if (location):
                locations = location.split(",")
                if len(locations) > 0 and ("Any" not in locations):
                    temp_locs = []
                    for i in locations:
                        temp_locs.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_location.contains(i) for i in temp_locs], models.JobPost.job_location.contains("Any")))

            if (skill):
                skills = skill.split(",")
                if len(skills) > 0:
                    skill_list = []
                    for i in skills:
                        skill_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.skill.contains(i) for i in skill_list]))

            if (title):
                titles = title.split(",")
                if len(titles) > 0:
                    title_list = []
                    for i in titles:
                        title_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_title.contains(i) for i in title_list]))

            if (qualification):
                qualifications = qualification.split(",")
                if len(qualifications) > 0:
                    qualification_list = []
                    for i in qualifications:
                        qualification_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.qualification.contains(i) for i in qualification_list]))

            if (function):
                functions = function.split(",")
                if len(functions) > 0:
                    function_list = []
                    for i in functions:
                        function_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_function.contains(i) for i in function_list]))

            if (type):
                types = type.split(",")
                if len(types) > 0 and ("Any" not in types):
                    type_list = []
                    for i in types:
                        type_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_type.contains(i) for i in type_list], models.JobPost.job_type.contains("Any")))

            if (mode):
                modes = mode.split(",")
                if len(modes) > 0 and ("Any" not in modes):
                    mode_list = []
                    for i in modes:
                        mode_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_mode.contains(i) for i in mode_list], models.JobPost.job_mode.contains("Any")))

            if (tenure):
                tenures = tenure.split(",")
                if len(tenures) > 0 and ("Any" not in tenures):
                    tenure_list = []
                    for i in tenures:
                        tenure_list.append(i.strip())
                    filters.append(or_(*[models.JobPost.job_tenuer.contains(i) for i in tenure_list], models.JobPost.job_tenuer.contains("Any")))

            if (exp):
                exp_filter = case([
                                    ((models.JobPost.experience_max != None), and_(models.JobPost.experience_max >= exp, models.JobPost.experience_min <= exp) ),
                                ],
                                else_ = models.JobPost.experience_min <= exp)
                filters.append(exp_filter)
            
            if (sal):
                sal_filter = case([
                                    ((models.JobPost.salary_max != None), (models.JobPost.salary_max >= sal)),
                                ],
                                else_ = models.JobPost.salary_max == None)
                filters.append(sal_filter)

            job_posts = db.query(models.JobPost.id,
            models.JobPost.job_title,
            models.JobPost.skill,
            models.JobPost.job_desc,
            models.JobPost.job_location,
            models.JobPost.started_date,
            models.JobPost.job_tenuer,
            models.JobPost.job_type,
            models.JobPost.job_mode,
            models.JobPost.experience_max,
            models.JobPost.experience_min,
            models.JobPost.salary_max,
            models.JobPost.salary_min,
            models.JobCandidate.id.label("job_candidate_id"),
            models.JobCandidate.status,
            models.JobCandidate.evaluation_score,
            models.JobCandidate.candidate_comment,
            models.Employer.company_name).join(models.Employer, models.JobCandidate).filter(models.JobCandidate.job_id == models.JobPost.id, models.JobCandidate.candidate_id == val_candidate.id, models.JobPost.employer_id==models.Employer.id, models.JobPost.status == "Open", models.JobPost.id.in_(filter_for_jobs),*filters).order_by(models.JobPost.id.desc()).limit(5).offset((page_number-1)*5).all()
            
            total_jobs_count_for_filter = db.query(models.JobPost.id).filter(models.JobPost.status == "Open", models.JobPost.id.in_(filter_for_jobs),*filters).order_by(models.JobPost.id.desc()).count()

            applied_jobs_list = []
            for i in job_posts:
                job = dict(i)
                interview_details = db.query(func.sum(models.JobCandidateInterView.interview_score).label("total_interview_score"), func.count(models.JobCandidateInterView.interview_score).label("total_interviews")).filter(models.JobCandidateInterView.job_candidate_id == i.job_candidate_id).all()[0]
                job["total_interview_score"] = interview_details[0]
                job["total_interviews"] = interview_details[1]
                applied_jobs_list.append(job)

            return {"job_posts": applied_jobs_list, "total_open_job_posts": total_jobs_count_for_filter}
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This user is deleted.")

@router.get("/employer/filter-values")
def allEmployerFilterValues(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        locations = db.query(models.Candidate.prefered_job_location).filter(
            models.Candidate.is_deleted == False).distinct().all()
        temp_loc_list = []
        for i in locations:
            if i.prefered_job_location is not None:
                new_loc = i.prefered_job_location.split(",")
                for j in new_loc:
                    temp_loc_list.append(j.strip())

        skills = db.query(models.Candidate.skill).filter(
            models.Candidate.is_deleted == False).distinct().all()
        temp_skills_list = []
        for i in skills:
            if i.skill is not None:
                new_loc = i.skill.split(",")
                for j in new_loc:
                    temp_skills_list.append(j.strip())

        qualifications = db.query(models.Candidate.qualification).filter(
            models.Candidate.is_deleted == False).distinct().all()
        temp_qualifications_list = []
        for i in qualifications:
            if i.qualification is not None:
                new_loc = i.qualification.split(",")
                for j in new_loc:
                    temp_qualifications_list.append(j.strip())

        return {"locations": list(set(temp_loc_list)), "skills": list(set(temp_skills_list)), "qualifications": list(set(temp_qualifications_list))}

@router.post("/employer/filtered-{status_type}-candidates/{jobID}/{page_number}")
def allStatusFilteredCandidates(page_number: int, jobID: int, status_type: str, location: str = Form(None), skill: str = Form(None), qualification: str = Form(None), type: str = Form(None), mode: str = Form(None), tenure: str = Form(None), exp: int = Form(None), sal: int = Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.is_active == True):
            if not db.query(models.JobPost).filter(models.JobPost.id == jobID, models.JobPost.created_by == _username_).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="JobPost not found")

            if db.query(models.Candidate).count() == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="candidates not found for this jobs")

            if status_type == "applied":
                filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.applied == "Yes", models.JobCandidate.status == "applied") #.subquery()
            elif status_type == "shortlisted":
                filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.shortlisted == "Yes", models.JobCandidate.status == "shortlisted") #.subquery()
            elif status_type == "hired":
                filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.hired == "Yes", models.JobCandidate.status == "hired") #.subquery()
            elif status_type == "rejected":
                filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.rejected == "Yes", models.JobCandidate.status == "rejected") #.subquery()
            elif status_type == "withdrawn":
                filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID, models.JobCandidate.withdrawn == "Yes", models.JobCandidate.status == "withdrawn") #.subquery()

            filters = []

            if (location):
                locations = location.split(",")
                if len(locations) > 0 and ("Any" not in locations):
                    temp_locs = []
                    for i in locations:
                        temp_locs.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_location.contains(i) for i in temp_locs], models.Candidate.prefered_job_location.contains("Any")))

            if (skill):
                skills = skill.split(",")
                if len(skills) > 0:
                    skill_list = []
                    for i in skills:
                        skill_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.skill.contains(i) for i in skill_list]))

            if (qualification):
                qualifications = qualification.split(",")
                if len(qualifications) > 0:
                    qualification_list = []
                    for i in qualifications:
                        qualification_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.qualification.contains(i) for i in qualification_list]))

            if (type):
                types = type.split(",")
                if len(types) > 0 and ("Any" not in types):
                    type_list = []
                    for i in types:
                        type_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_type.contains(i) for i in type_list], models.Candidate.prefered_job_type.contains("Any")))

            if (mode):
                modes = mode.split(",")
                if len(modes) > 0 and ("Any" not in modes):
                    mode_list = []
                    for i in modes:
                        mode_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_mode.contains(i) for i in mode_list], models.Candidate.prefered_job_mode.contains("Any")))

            if (tenure):
                tenures = tenure.split(",")
                if len(tenures) > 0 and ("Any" not in tenures):
                    tenure_list = []
                    for i in tenures:
                        tenure_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_tenuer.contains(i) for i in tenure_list], models.Candidate.prefered_job_tenuer.contains("Any")))

            if (exp):
                filters.append(models.Candidate.total_no_of_years_exp >= exp)
            
            if (sal):
                filters.append(models.Candidate.excepted_ctc_min <= sal)

            #first code!!!

            # applied_candidates =  db.query(models.Candidate.id,
            # models.Candidate.name,
            # models.Candidate.current_location,
            # models.Candidate.qualification,
            # models.Candidate.skill,
            # models.Candidate.total_no_of_years_exp,
            # models.Candidate.total_no_of_month_exp,
            # models.Candidate.profile_summery,
            # models.JobCandidate.id.label("job_candidate_id"),
            # models.JobCandidate.status,
            # models.JobCandidate.employer_comment,
            # models.JobCandidate.evaluation_score,
            # models.JobCandidate.applied_on).join(models.JobCandidate).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.Candidate.id.in_(filter_for_candidates),*filters).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()

            # applied_candidates_list = []
            # for i in applied_candidates:
            #     cand = dict(i)
            #     interview_details = db.query(func.sum(models.JobCandidateInterView.interview_score).label("total_interview_score"), func.count(models.JobCandidateInterView.interview_score).label("total_interviews")).filter(models.JobCandidateInterView.job_candidate_id == i.job_candidate_id).all()[0]
            #     # print(interview_details)
            #     cand["total_interview_score"] = interview_details[0]
            #     cand["total_interviews"] = interview_details[1]
            #     applied_candidates_list.append(cand)

            # second code!!!
            # int_subquery = db.query(models.JobCandidateInterView.job_candidate_id,
            #                         func.sum(models.JobCandidateInterView.interview_score).label("total_interview_score"),
            #                         func.count(models.JobCandidateInterView.interview_score).label("total_interviews")).group_by(models.JobCandidateInterView.job_candidate_id).subquery()

            # jobcand_subquery = db.query(models.JobCandidate.id.label("job_candidate_id"),
            #                             models.JobCandidate.candidate_id,
            #                             models.JobCandidate.job_id,
            #                             models.JobCandidate.status,
            #                             models.JobCandidate.employer_comment,
            #                             models.JobCandidate.evaluation_score,
            #                             int_subquery.c.total_interview_score,
            #                             int_subquery.c.total_interviews,
            #                             models.JobCandidate.applied_on).outerjoin(int_subquery, models.JobCandidate.id == int_subquery.c.job_candidate_id).subquery()

            # applied_candidates =  db.query(models.Candidate.id,
            # models.Candidate.name,
            # models.Candidate.current_location,
            # models.Candidate.qualification,
            # models.Candidate.skill,
            # models.Candidate.total_no_of_years_exp,
            # models.Candidate.total_no_of_month_exp,
            # models.Candidate.profile_summery,
            # jobcand_subquery.c.job_candidate_id,
            # jobcand_subquery.c.job_id,
            # jobcand_subquery.c.status,
            # jobcand_subquery.c.employer_comment,
            # jobcand_subquery.c.evaluation_score,
            # jobcand_subquery.c.total_interview_score,
            # jobcand_subquery.c.total_interviews,
            # jobcand_subquery.c.applied_on).outerjoin(jobcand_subquery, jobcand_subquery.c.candidate_id == models.Candidate.id).filter(jobcand_subquery.c.job_id == jobID,models.Candidate.id.in_(filter_for_candidates),*filters).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()
            
            # third code!!!
            applied_candidates =  db.query(models.Candidate.id,
            models.Candidate.name,
            models.Candidate.current_location,
            models.Candidate.qualification,
            models.Candidate.skill,
            models.Candidate.total_no_of_years_exp,
            models.Candidate.total_no_of_month_exp,
            models.Candidate.profile_summery,
            models.JobCandidate.status,
            models.JobCandidate.employer_comment,
            models.JobCandidate.evaluation_score,
            func.sum(models.JobCandidateInterView.interview_score).label("total_interview_score"),
            func.count(models.JobCandidateInterView.interview_score).label("total_interviews"),
            models.JobCandidate.applied_on).select_from(models.Candidate).outerjoin(models.JobCandidate).outerjoin(models.JobCandidateInterView).group_by(models.JobCandidate.candidate_id).group_by(models.JobCandidateInterView.job_candidate_id).filter(models.JobCandidate.job_id == jobID, models.Candidate.id.in_(filter_for_candidates),*filters).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()


            # for i in (applied_candidates):
            #     print(i.total_interview_score)
                # print("for candid ",i.id, " for job ",i.job_id,", totint score ",i.total_interview_score)

            total_applied_candidates = db.query(models.Candidate.id).filter(models.JobCandidate.candidate_id == models.Candidate.id, models.JobCandidate.job_id == jobID, models.Candidate.id.in_(filter_for_candidates),*filters).order_by(models.Candidate.id.desc()).count() #, models.JobCandidate.applied == "Yes"

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")

@router.post("/employer/filtered-candidates/{jobID}/{page_number}")
def allFilteredCandidates(page_number: int, jobID: int, location: str = Form(None), skill: str = Form(None), qualification: str = Form(None), type: str = Form(None), mode: str = Form(None), tenure: str = Form(None), exp: int = Form(None), sal: int = Form(None), db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
    current_employer = current_user
    _username_ = current_employer.user["username"]

    val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

    candidates_to_view = val_employer.no_of_candidates_to_view
    last_page = (candidates_to_view // 5) + 1
    if  (page_number == last_page):
        limit_result = candidates_to_view % 5
    else:
        limit_result = 5

    if not val_employer:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Not authenticated to view a job post")
    else:
        if (val_employer.is_deleted != True):
            filter_for_candidates = db.query(models.JobCandidate.candidate_id).filter(models.JobCandidate.job_id == jobID) #.subquery()

            filters = []

            if (location):
                locations = location.split(",")
                if len(locations) > 0 and ("Any" not in locations):
                    temp_locs = []
                    for i in locations:
                        temp_locs.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_location.contains(i) for i in temp_locs], models.Candidate.prefered_job_location.contains("Any")))

            if (skill):
                skills = skill.split(",")
                if len(skills) > 0:
                    skill_list = []
                    for i in skills:
                        skill_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.skill.contains(i) for i in skill_list]))

            if (qualification):
                qualifications = qualification.split(",")
                if len(qualifications) > 0:
                    qualification_list = []
                    for i in qualifications:
                        qualification_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.qualification.contains(i) for i in qualification_list]))

            if (type):
                types = type.split(",")
                if len(types) > 0 and ("Any" not in types):
                    type_list = []
                    for i in types:
                        type_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_type.contains(i) for i in type_list], models.Candidate.prefered_job_type.contains("Any")))

            if (mode):
                modes = mode.split(",")
                if len(modes) > 0 and ("Any" not in modes):
                    mode_list = []
                    for i in modes:
                        mode_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_mode.contains(i) for i in mode_list], models.Candidate.prefered_job_mode.contains("Any")))

            if (tenure):
                tenures = tenure.split(",")
                if len(tenures) > 0 and ("Any" not in tenures):
                    tenure_list = []
                    for i in tenures:
                        tenure_list.append(i.strip())
                    filters.append(or_(*[models.Candidate.prefered_job_tenuer.contains(i) for i in tenure_list], models.Candidate.prefered_job_tenuer.contains("Any")))

            if (exp):
                filters.append(models.Candidate.total_no_of_years_exp >= exp)
            
            if (sal):
                filters.append(models.Candidate.excepted_ctc_min <= sal)

            applied_candidates =  db.query(models.Candidate.id,
            models.Candidate.name,
            models.Candidate.current_location,
            models.Candidate.qualification,
            models.Candidate.skill,
            models.Candidate.total_no_of_years_exp,
            models.Candidate.total_no_of_month_exp,
            models.Candidate.profile_summery).filter(~models.Candidate.id.in_(filter_for_candidates),*filters).order_by(models.Candidate.id.desc()).limit(limit_result).offset((page_number-1)*5).all()
            
            total_applied_candidates = db.query(models.Candidate.id).filter(~models.Candidate.id.in_(filter_for_candidates),*filters).order_by(models.Candidate.id.desc()).limit(candidates_to_view).count()

            return {"candidates": applied_candidates, "total_applied_candidates": total_applied_candidates}
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="this employer is deleted")

