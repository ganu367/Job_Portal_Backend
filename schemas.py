from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field
from typing import List

# employer related schemas here


class EmployerBase(BaseModel):
    username: str


class EmployerRegister(EmployerBase):
    company_name: str
    country_code: str
    mobile_number: str
    password: str

    class config:
        orm_mode = True


class EmployerCreate(EmployerBase):
    password: str

    class config:
        orm_mode = True


class EmployerProfileCreate(BaseModel):
    company_name: str
    address: str
    country_code: str
    mobile_number: str
    employer_name: str
    gst_number: str
    pan_number: str
    profile: str
    # sub_domain: str
    web_url: str


class EmployerViewProfile(BaseModel):
    company_name: str
    username: str
    address: str
    employer_name: str
    gst_number: str
    pan_number: str
    profile: str
    mobile_number: str

# candidate related schemas here


class CandidateBase(BaseModel):
    username: str


class CandidateRegister(EmployerBase):
    name: str
    country_code: str
    mobile_number: str
    password: str

    class config:
        orm_mode = True


class CandidateCreate(EmployerBase):
    password: str

    class config:
        orm_mode = True


class CandidateProfileCreate(BaseModel):
    address: str
    country_code: str
    mobile_number: str
    current_location: str
    photo: str
    resume: str
    profile_summery: str
    video_profile: str
    total_no_of_years_exp: int
    total_no_of_month_exp: int
    prefered_job_location: int
    prefered_job_type: str
    prefered_job_tenuer: str
    prefered_job_mode: str
    current_ctc: int
    excepted_ctc_min: int
    excepted_ctc_max: int
    qualification: str
    skill: str
    # sub_domain: str


class CandidateViewProfile(BaseModel):
    name: str
    mobile_number: str
    address: str
    current_location: str
    photo: str
    resume: str
    profile_summery: str
    video_profile: str
    total_no_of_years_exp: int
    total_no_of_month_exp: int
    prefered_job_location: int
    prefered_job_type: str
    prefered_job_tenuer: str
    prefered_job_mode: str
    current_ctc: int
    excepted_ctc_min: int
    excepted_ctc_max: int
    qualification: str
    skill: str


class jobPostCreate(BaseModel):
    job_title: str
    description: str
    # job_file :str
    qualification: str
    skill: str
    experience_min: int
    experience_max: int
    salary_min: int
    salary_max: int
    perks: int
    job_location: str
    job_tenuer: str
    job_type: str
    job_mode: str
    status: str
    other_details: str
    required_details: str
    # assignment :str
    # assignment_file :str
    # assignment_link :str


class InterviewBase(BaseModel):
    interview_title: str
    interview_date: str
    interview_time: str


class UserPassword(BaseModel):
    # password updation
    current_password: str
    new_password: str
    confirm_password: str


class UsersRead(BaseModel):
    id: int
    username: str
    is_active: bool
    is_admin: bool
    licence_id: int

    class config:
        orm_mode = True


class ForgetPassword(BaseModel):
    new_password: str
    confirm_password: str

# jobCandidate


class JobCandidateActions(BaseModel):
    employer_comment: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: Union[dict, None] = None

class JobFunctionBase(BaseModel):
    job_function: str

class QualificationBase(BaseModel):
    qualification: str

class SkillBase(BaseModel):
    skill: str

class LicenseBase(BaseModel):
    company_name: str
    no_of_candidates_to_view: int
    expiry_date: str

class LicenseValues(BaseModel):
    company_name: str
