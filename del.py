# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# new_job_post = models.JobPost(employer_id=employer_ids, job_title=title, job_desc=description,
#                             qualification=qualification, skill=skill, experience_min=experience_min,
#                             experience_max=experience_max, salary_min=salary_min, salary_max=salary_max, perks=perks,
#                             job_location=job_location, job_tenuer=job_tenuer, job_type=job_type,
#                             job_mode=job_mode, other_details=other_details, required_details=required_details, no_of_openings=no_of_openings, assignment=assignment, assignment_file=os.getcwd() + "\\employer\\" + str(employer_ids) + "\\job_post\\"+_new_assignment_file_, assignment_link=assignment_link, created_by=_username_, modified_by=_username_)

# new_job_post = models.JobPost(employer_id=employer_ids, job_title=title, job_desc=description,
#                             qualification=qualification, skill=skill, experience_min=experience_min,
#                             experience_max=experience_max, salary_min=salary_min, salary_max=salary_max, perks=perks,
#                             job_location=job_location, job_tenuer=job_tenuer, job_type=job_type,
#                             job_mode=job_mode, other_details=other_details, no_of_openings=no_of_openings, required_details=required_details, created_by=_username_, modified_by=_username_)


# @router.put("delete-job-post/{id}")
# def deleteJobPost(id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
#     current_employer = current_user
#     _username_ = current_employer.user["username"]

#     val_employer = db.query(models.Employer).filter(
#         models.Employer.username == _username_).first()

#     if not val_employer:
#         raise HTTPException(status_code=status.HTTP_302_FOUND,
#                             detail="Not authenticated to view a job post")
#     else:

#         val_job_post = db.query(models.JobPost).filter(
#             models.JobPost.employer_id == val_employer.id).first()

#         if not val_job_post:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="job post not found")
#         else:

#             get_job = db.query(models.JobPost).filter(models.JobPost.employer_id == val_employer.id,
#                                                       models.JobPost.id == id, models.JobPost.is_deleted == False).first()
#             if not get_job:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="job post not found")
#             else:
#                 db.query(models.JobPost).filter(models.JobPost.employer_id == val_employer.id,
#                                                 models.JobPost.id == id, models.JobPost.is_deleted == False).update({"is_deleted": True})
#                 db.commit()

# if photo_files is not None:

#     db.query(models.Candidate).filter(models.Candidate.username==_username_).update({"country_code":country_code,"mobile_number":mobile_number,"address":address,"current_location":current_location,"photo":os.getcwd() + "\\candidate\\" + str(val_candidate.id)  +"\\docs\\"+_new_photo_file_,
#         # "resume":resume,
#         "profile_summery":profile_summery,
#         "prefered_job_location":prefered_job_location,
#         "video_profile" :video_profile,
#         "total_no_of_years_exp":total_no_of_years_exp,
#         "total_no_of_month_exp":total_no_of_month_exp,
#         "prefered_job_tenuer":prefered_job_tenuer,
#         "prefered_job_type" :prefered_job_type,
#         "prefered_job_mode":prefered_job_mode,
#         "current_ctc":current_ctc,
#         "notice_period":notice_period,
#         "excepted_ctc_min":excepted_ctc_min,
#         "excepted_ctc_max":excepted_ctc_max,
#         "qualification":qualification,
#         "skill":skill,
#         "isProfileCompleted":True,"created_by":_username_})

# else:

#     db.query(models.Candidate).filter(models.Candidate.username==_username_).update({"country_code":country_code,"mobile_number":mobile_number,"address":address,"current_location":current_location,
#         # "resume":resume,
#         "profile_summery":profile_summery,
#         "prefered_job_location":prefered_job_location,
#         "video_profile" :video_profile,
#         "total_no_of_years_exp":total_no_of_years_exp,
#         "total_no_of_month_exp":total_no_of_month_exp,
#         "prefered_job_tenuer":prefered_job_tenuer,
#         "prefered_job_type" :prefered_job_type,
#         "prefered_job_mode":prefered_job_mode,
#         "current_ctc":current_ctc,
#         "notice_period":notice_period,
#         "excepted_ctc_min":excepted_ctc_min,
#         "excepted_ctc_max":excepted_ctc_max,
#         "qualification":qualification,
#         "skill":skill,
#         "isProfileCompleted":True,"created_by":_username_})

# if resume_files is not None:
#     db.query(models.Candidate).filter(models.Candidate.username==_username_).update({"country_code":country_code,"mobile_number":mobile_number,"address":address,"current_location":current_location,
#         "resume":os.getcwd() + "\\candidate\\" + str(val_candidate.id)  +"\\docs\\"+_new_resume_file_,
#         "profile_summery":profile_summery,
#         "prefered_job_location":prefered_job_location,
#         "video_profile" :video_profile,
#         "total_no_of_years_exp":total_no_of_years_exp,
#         "total_no_of_month_exp":total_no_of_month_exp,
#         "prefered_job_tenuer":prefered_job_tenuer,
#         "prefered_job_type" :prefered_job_type,
#         "prefered_job_mode":prefered_job_mode,
#         "current_ctc":current_ctc,
#         "notice_period":notice_period,
#         "excepted_ctc_min":excepted_ctc_min,
#         "excepted_ctc_max":excepted_ctc_max,
#         "qualification":qualification,
#         "skill":skill,
#         "isProfileCompleted":True,"created_by":_username_})

# db.query(models.Candidate).filter(models.Candidate.username==_username_).update({"country_code":country_code,"mobile_number":mobile_number,"address":address,"current_location":current_location,
# # "resume":resume,
# "profile_summery":profile_summery,
# "prefered_job_location":prefered_job_location,
# "video_profile" :video_profile,
# "total_no_of_years_exp":total_no_of_years_exp,
# "total_no_of_month_exp":total_no_of_month_exp,
# "prefered_job_tenuer":prefered_job_tenuer,
# "prefered_job_type" :prefered_job_type,
# "prefered_job_mode":prefered_job_mode,
# "current_ctc":current_ctc,
# "notice_period":notice_period,
# "excepted_ctc_min":excepted_ctc_min,
# "excepted_ctc_max":excepted_ctc_max,
# "qualification":qualification,
# "skill":skill,
# "isProfileCompleted":True,"created_by":_username_})

# db.query(models.Candidate).filter(models.Candidate.username==_username_).update({"country_code":country_code,"mobile_number":mobile_number,"address":address,"current_location":current_location,"photo":os.getcwd() + "\\candidate\\" + str(val_candidate.id)  +"\\docs\\"+_new_photo_file_,
#     # "resume":resume,
#     "profile_summery":profile_summery,
#     "prefered_job_location":prefered_job_location,
#     "video_profile" :video_profile,
#     "total_no_of_years_exp":total_no_of_years_exp,
#     "total_no_of_month_exp":total_no_of_month_exp,
#     "prefered_job_tenuer":prefered_job_tenuer,
#     "prefered_job_type" :prefered_job_type,
#     "prefered_job_mode":prefered_job_mode,
#     "current_ctc":current_ctc,
#     "notice_period":notice_period,
#     "excepted_ctc_min":excepted_ctc_min,
#     "excepted_ctc_max":excepted_ctc_max,
#     "qualification":qualification,
#     "skill":skill,
#     "isProfileCompleted":True,"created_by":_username_})

# if db.query(models.Candidate).count()==0:
#     current_candidate_id = 1
# else:
#     last_id = db.query(func.max(models.Candidate.id)).first()
#     current_candidate_id = last_id[0] + 1

# @router.get("/view-all-applied-jobs")
# def viewJobsCandidate(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
#     current_candidate = current_user
#     _username_ = current_candidate.user["username"]

#     val_candidate = db.query(models.Candidate).filter(
#         models.Candidate.username == _username_).first()

#     if not val_candidate:

#         raise HTTPException(status_code=status.HTTP_302_FOUND,
#                             detail="Not authenticated")
#     else:
#         if (val_candidate.is_deleted != True):

#             show_aplied_jobs = db.query(models.JobCandidate.applied_on, models.JobCandidate.status, models.JobCandidate.job_id).filter(
#                 models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.applied == "Yes").all()

#             # all_applied_jobs = []

#             for i in show_aplied_jobs:
#                 jobs_list = {}

#                 job_ids = i.job_id
#                 jobs = db.query(models.JobPost).filter(models.JobPost.id == job_ids).first()
#                 print(jobs)
#             return show_aplied_jobs

#         else:
#             raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                 detail="This user is deleted.")

# @router.get("/validate-profile")
# def validateProfile(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(oauth2.get_current_user)):
#     current_employer = current_user
#     _username_ = current_employer.user["username"]

#     val_employer = db.query(models.Employer).filter(
#         models.Employer.username == _username_).first()

#     if not val_employer:
#         raise HTTPException(status_code=status.HTTP_302_FOUND,
#                             detail="Not authenticated")
#     else:

#         if (val_employer.is_deleted != True):

#             my_profile = db.query(models.Employer).filter(

#                 models.Employer.id == val_employer.id, models.Employer.is_deleted == False).first()

#             return my_profile

#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Your profile is deleted")

# if not job_candidate:
#     new_candidate_list["status"] = None
# else:
#     new_candidate_list["status"] = job_candidate.status
# print("candidate id that will not be displayed: ",job_candidate)

# candidates_for_job = []

# for i in candidate_lists:

#     new_candidate_list = {"name": None, "profile_summery": None,
#                           "qualification": None, "skill": None, "status": None, "exp_years": None, "exp_months": None, "location": None, "id": None, "apply": None}

#     job_candidate = db.query(models.Candidate).filter(
#         models.Candidate.id == i.candidate_id).first()

#     # if not job_candidate:
#     new_candidate_list["apply"] = candidate_lists
#     new_candidate_list["name"] = job_candidate.name
#     new_candidate_list["profile_summery"] = job_candidate.profile_summery
#     new_candidate_list["qualification"] = job_candidate.qualification
#     new_candidate_list["skill"] = job_candidate.skill
#     new_candidate_list["exp_years"] = job_candidate.total_no_of_years_exp
#     new_candidate_list["exp_months"] = job_candidate.total_no_of_month_exp
#     new_candidate_list["location"] = job_candidate.current_location
#     new_candidate_list["id"] = job_candidate.id
#     candidates_for_job.append(new_candidate_list)

# candidate_lists = db.query(models.JobCandidate).filter(
#     models.JobCandidate.job_id == jobid, models.JobCandidate.applied == "Yes").all()

# # job_candidate= db.query(models.JobCandidate).filter(models.JobCandidate.==username).first()
# sub_query = db.query(models.Candidate).filter(models.Candidate.id== candidate_lists.).subquery()
# cmps = db.query(models.Companys).filter(~models.Companys.id.in_(sub_query),models.Companys.licence_id==licence_id,models.Companys.is_deleted==False).all()


# employer_oauth2_schema = OAuth2PasswordBearer(
#     tokenUrl="/auth/employer/sign-in",
#     scheme_name="admin_oauth2_schema"
# )
# candidate_oauth2_schema = OAuth2PasswordBearer(
#     tokenUrl="/auth/candidate/sign-in",
#     scheme_name="candidate_oauth2_schema"
# )

# if not val_job_post:

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail="not found job post")
# else:

# val_job_post = db.query(models.JobPost).filter(
#     models.JobPost.employer_id == val_employer.id).first()


# @router.post("/employer/sign-in")
# def employerLogin(request: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
#     val_employer = db.query(models.Employer).filter(models.Employer.username == request.username).first()

#     if not val_employer:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="The user does not exists")
#     else:
#             if not (db.query(models.Employer).filter(val_employer.is_active==True,val_employer.is_deleted==False).first()):
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                     detail="This account is deleted")
#             else:
#                 # verify password between requesting by a user & database password
#                 if not hashing.Hash.verify(val_employer.password, request.password):
#                     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                         detail="Incorrect Passwords")


#                 if db.query(models.Employer).filter(models.Employer.id == val_employer.id, models.Employer.address == None, models.Employer.employer_name == None, models.Employer.pan_number == None, models.Employer.profile == None).first():

#                     access_token = tokens.create_access_token(data={"user":{"username": request.username, "userType" : "employer", "isProfileCompleted": False}})
#                     return {"access_token": access_token, "token_type": "bearer"}

#                 else:

#                     access_token = tokens.create_access_token(data={"user":{"username": request.username, "userType" : "employer", "isProfileCompleted": True}})
#                     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/candidate/sign-in")
# def candidateLogin(request: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
#     val_candidate = db.query(models.Candidate).filter(models.Candidate.username == request.username).first()

#     if not val_candidate:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="The user does not exists")
#     else:
#             if not (db.query(models.Candidate).filter(val_candidate.is_active==True,val_candidate.is_deleted==False).first()):
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                     detail="This account is deleted")
#             else:
#                 # verify password between requesting by a user & database password
#                 if not hashing.Hash.verify(val_candidate.password, request.password):
#                     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                         detail="Incorrect Passwords")


#                 if db.query(models.Candidate).filter(models.Candidate.id == val_candidate.id, models.Candidate.address == None, models.Candidate.current_ctc == None, models.Candidate.current_location == None, models.Candidate.excepted_ctc_min == None,
#                                         models.Candidate.profile_summery==None,models.Candidate.prefered_job_location==None,models.Candidate.prefered_job_mode==None,models.Candidate.prefered_job_tenuer == None,models.Candidate.prefered_job_type == None,models.Candidate.total_no_of_month_exp==None,
#                                         models.Candidate.total_no_of_years_exp==None,models.Candidate.skill == None,models.Candidate.qualification == None).first():

#                     access_token = tokens.create_access_token(data={"user":{"username": request.username, "userType" : "candidate", "isProfileCompleted": False}})
#                     return {"access_token": access_token, "token_type": "bearer"}

#                 else:

#                     access_token = tokens.create_access_token(data={"user":{"username": request.username, "userType" : "candidate", "isProfileComplete": True}})
#                     return {"access_token": access_token, "token_type": "bearer"}

#                 # access_token = tokens.create_access_token(data={"user":{"username": request.username}})

#                 # return {"access_token": access_token, "token_type": "bearer"}

# db.query(models.JobCandidate, models.Candidate).filter(models.JobCandidate.candidate_id == models.Candidate.id).filter(models.JobCandidate.applied == "Yes", models.JobCandidate.job_id == jobID).all()
# candidate_lists = db.query(models.Candidate).limit(25).offset(
#     page_number*25).order_by(models.Candidate.id.desc()).all()
#  -- OR --
# candidates_for_job = []

# for i in candidate_lists:

#     new_candidate_list = {"name": None, "profile_summery": None,
#                           "qualification": None, "skill": None, "status": None, "exp_years": None, "exp_months": None, "location": None, "id": None}

#     job_candidate = db.query(models.JobCandidate).filter(
#         models.JobCandidate.candidate_id == i.id, models.JobCandidate.job_id == jobID).first()

#     if not job_candidate:
#         new_candidate_list["name"] = i.name
#         new_candidate_list["profile_summery"] = i.profile_summery
#         new_candidate_list["qualification"] = i.qualification
#         new_candidate_list["skill"] = i.skill
#         new_candidate_list["exp_years"] = i.total_no_of_years_exp
#         new_candidate_list["exp_months"] = i.total_no_of_month_exp
#         new_candidate_list["location"] = i.current_location
#         new_candidate_list["id"] = i.id
#         candidates_for_job.append(new_candidate_list)

# show_aplied_jobs = db.query(models.JobCandidate.applied_on, models.JobCandidate.status, models.JobCandidate.job_id).filter(
#     models.JobCandidate.id == jobID, models.JobCandidate.candidate_id == val_candidate.id, models.JobCandidate.applied == "Yes").all()

# all_applied_jobs = []
# for i in show_aplied_jobs:
#     new_job = {"company_name": "",
#                "applied_on": "", "status": ""}

#     job_ids = i.job_id
#     job = db.query(models.JobPost).filter(
#         models.JobPost.id == job_ids).first()
#     emp_id = job.employer_id
#     employer = db.query(models.Employer).filter(
#         models.Employer.id == emp_id).first()

#     new_job["job"] = job
#     new_job["company_name"] = employer.company_name
#     new_job["applied_on"] = i.applied_on
#     new_job["status"] = i.status
#     all_applied_jobs.append(new_job)

#  val_job_post = db.query(models.JobPost).filter(
# models.JobPost.employer_id == val_employer.id).first()
# if not val_job_post:
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail="job post not found")

# else:






# second code with interview scores but with errorin functionality

# applied_candidates =  db.query(models.Candidate.id,
# models.Candidate.name,
# models.Candidate.current_location,
# models.Candidate.qualification,
# models.Candidate.skill,
# models.Candidate.total_no_of_years_exp,
# models.Candidate.total_no_of_month_exp,
# models.Candidate.profile_summery,
# models.JobCandidate.status,
# models.JobCandidate.employer_comment,
# models.JobCandidate.evaluation_score,
# func.sum(models.JobCandidateInterView.interview_score).label("total_interview_score"),
# func.count(models.JobCandidateInterView.interview_score).label("total_interviews"),
# models.JobCandidate.applied_on).join(models.JobCandidate, models.JobCandidate.candidate_id == models.Candidate.id).join(models.JobCandidateInterView, models.JobCandidateInterView.job_candidate_id == models.JobCandidate.id).filter(models.JobCandidate.job_id == jobID, models.Candidate.id.in_(filter_for_candidates),*filters).order_by(models.Candidate.id.desc()).limit(5).offset((page_number-1)*5).all()

#email_fastapi
# from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
# from dotenv import dotenv_values
# from pydantic import BaseModel, EmailStr
# from typing import List
# # from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
# import oauth2
# from models import User
# import os
# from dotenv import dotenv_values
# from dotenv import load_dotenv

# config = dotenv_values(".env")
# connect = load_dotenv()



# conf = ConnectionConfig(
#     MAIL_USERNAME =os.getenv('SENDER_EMAIL'),
#     MAIL_PASSWORD =os.getenv('SENDER_EMAIL_PASSWORD'),
#     MAIL_FROM = os.getenv('SENDER_EMAIL'),
#     MAIL_PORT = os.getenv('PORT'),
#     MAIL_SERVER = os.getenv('HOST'),
#     MAIL_TLS = True,
#     MAIL_SSL = False,
#     USE_CREDENTIALS = True
# )

# class EmailSchema(BaseModel):
#     email: List[EmailStr]

# async def send_email(email : list, instance: User):

#     token_data = {
#         "id" : instance.id,
#         "username" : instance.username
#     }

#     token = jwt.encode(token_data,os.getenv("SECRET_KEY"))

#     template = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#         </head>
#         <body>
#             <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
#                 <h3> Account Verification </h3>
#                 <br>
#                 <p>Thanks for choosing EasyShopas, please 
#                 click on the link below to verify your account</p> 
#                 <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
#                  href="http://localhost:8000/verification/?token={token}">
#                     Verify your email
#                 <a>
#                 <p style="margin-top:1rem;">If you did not register for EasyShopas, 
#                 please kindly ignore this email and nothing will happen. Thanks<p>
#             </div>
#         </body>
#         </html>
#     """

#     message = MessageSchema(
#         subject="EasyShopas Account Verification Mail",
#         recipients=email,  # List of recipients, as many as you can pass 
#         body=template,
#         subtype="html"
#         )

#     fm = FastMail(conf)
#     await fm.send_message(message) 

# @router.post("/verify-users/{user_type}/{email}")
# @router.post("/verify-users/{email}")
# # def VerifyUser(user_type:str,email:str, db: Session = Depends(get_db)):
# def VerifyUser(email: str, db: Session = Depends(get_db)):
#     if user_type == "employer":
#         user = db.query(models.Employer).filter(
#             models.Employer.username == email).first()

#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="User does not exits")
#         else:
#             if not (db.query(models.Employer).filter(
#                     user.is_deleted == False).first()):

#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                     detail="User's account deleted")
#             else:
#                 db.query(models.Candidate).filter(
#                     models.Candidate.username == email).update({"is_active": True})
#                 db.commit()
#                 return {f"Verified"}
#     else:
#         user = db.query(models.Candidate).filter(
#             models.Candidate.username == email).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="User does not exits")
#         else:
#             if not (db.query(models.Candidate).filter(
#                     user.is_deleted == False).first()):

#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                     detail="User's account deleted")
#             else:
#                 db.query(models.Employer).filter(
#                     models.Employer.username == email).update({"is_active": True})
#                 db.commit()
#                 return {f"Verified"}




 # # alerts.SendEmail(request.username, "candidate")
        # token = randbytes(10)
        # hashedCode = hashlib.sha256()
        # hashedCode.update(token)
        # verification_code = hashedCode.hexdigest()

        # # alerts.SendEmail(request.username)
        # new_candidate = models.Candidate(name=request_fields.name, country_code=request_fields.country_code,
        #                                  mobile_number=request_fields.mobile_number, username=request_fields.username, password=hashing.Hash.bcrypt(request_fields.password), verification_code=verification_code)
        # db.add(new_candidate)
        # # db.commit()
        # # db.refresh(new_candidate)

        # access_token = tokens.create_access_token(data={"user": {
        #                                           "username": request_fields.username, "userType": "candidate", "isProfileCompleted": False, "isActive": False}})
        # # return access_token

        # # email sending
        # # try:
        # # token = randbytes(10)
        # # hashedCode = hashlib.sha256()
        # # hashedCode.update(token)
        # # verification_code = hashedCode.hexdigest()
        # # models.Candidate.update({
        # #     "$set": {"verification_code": verification_code, "modified_on": datetime.utcnow()}})
        # db.commit()

        # url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/api/auth/verifyemail/{token.hex()}"
        # print(url)
        # print(new_candidate.__dict__)
        
        # Email(utility.userEntity(new_candidate.__dict__), url, [
        #     EmailStr(request_fields.username)]).sendVerificationCode()
        
        # # except Exception as error:
        # #     # models.Candidate.update({
        # #     #     "$set": {"verification_code": verification_code, "modified_on": datetime.utcnow()}})
        # #     # db.commit()

        # #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        # #                         detail='There was an error sending email')



# @router.put("/changed-password/{user_type}/{username}")
# # async def ForgetPassword(user_type:str,username: str, request: schemas.ForgetPassword, db: Session = Depends(get_db)):
# async def ChangedPassword(username: str, request: schemas.ForgetPassword, db: Session = Depends(get_db)):
#     try:
#         if (request.new_password != request.confirm_password):

#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="Password doest not match")
#         else:
#             if user_type == "employer":
#                 db.query(models.Employer).filter(models.Employer.username == request.username).update(
#                     {"password": hashing.Hash.bcrypt(request.new_password)})
#             else:
#                 db.query(models.Candidate).filter(models.Candidate.username == request.username).update(
#                     {"password": hashing.Hash.bcrypt(request.new_password)})
#             db.commit()

#             return {f"Password successfully updated"}
#     except Exception as e:
#         print(e)

# @router.put("/verify-users-candidate/{email}{user_type}")
# def VerifyCandidate(email: str, db: Session = Depends(get_db)):
#     user = db.query(models.Candidate).filter(
#         models.Candidate.username == email).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="User does not exits")
#     else:
#         if not (db.query(models.Candidate).filter(models.Candidate.is_active == True).first()):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="User's does not exists")
#         else:
#             # alerts.SendEmail(email)
#             db.query(models.Candidate).filter(
#                 models.Candidate.username == email).update({"is_active": True})
#             db.commit()
#             return {f"Verified"}


# @router.put("/verify-users-employer/{email}/{user_type}")
# def VerifyEmployer(email: str, db: Session = Depends(get_db)):
#     user = db.query(models.Employer).filter(
#         models.Employer.username == email)

#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="User does not exits")
#     else:
#         if not (user.filter(models.Candidate.is_active == True).first()):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="User's does not exists")
#         else:
#             db.query(models.Employer).filter(
#                 models.Employer.username == email).update({"is_active": True})
#             db.commit()
#             return {f"Verified"}


# def userEntity(user) -> dict:
#     return {
#         "name": user["name"],
#         "username": user["username"],
#         "is_active": user["is_active"],
#         "password": user["password"],
#         # "created_at": user["created_at"],
#         # "updated_at": user["updated_at"]
#     }

