from datetime import datetime, timedelta
from sqlalchemy import Boolean, Column, Integer, String, BIGINT, ForeignKey, DateTime, TIMESTAMP, UniqueConstraint, TEXT
from database import Base
from sqlalchemy.orm import relationship

current_datetime = datetime.now()
expdt = current_datetime + timedelta(days=10)
dt = current_datetime
defexpdt = expdt


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    organisation_name = Column(String)
    logo = Column(String)


class Employer(Base):
    __tablename__ = "employer"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = Column(String)
    employer_name = Column(String)
    country_code = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)
    isProfileCompleted = Column(Boolean, default=False)
    gst_number = Column(String)
    pan_number = Column(String)
    profile = Column(String)
    # sub_domain = Column(String)
    web_url = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime, default=dt)
    modified_by = Column(String)
    modified_on = Column(DateTime, default=dt)
    expiry_date = Column(DateTime, default=(defexpdt))
    no_of_candidates_to_view = Column(Integer, default=25)
    verification_code = Column(String)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    # Constraints
    # __table_args__ = (UniqueConstraint(
    #     'sub_domain', 'username', name='unq_1'),)

    # Relationship           #child
    jobpost = relationship(
        "JobPost", back_populates="job_post_owner", uselist=False)


class JobPost(Base):
    __tablename__ = "jobpost"

    id = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey(
        "employer.id"))  # refer from Employer table

    job_title = Column(String)
    job_desc = Column(TEXT)
    job_file = Column(String)
    job_function = Column(String)
    qualification = Column(String)
    skill = Column(String)
    experience_min = Column(Integer, default=0)
    experience_max = Column(Integer)
    salary_min = Column(Integer, default=0)
    salary_max = Column(Integer)
    perks = Column(String)
    job_location = Column(String)
    job_tenuer = Column(String, default="Permenent")
    job_type = Column(String, default="Full time")
    job_mode = Column(String, default="Office")
    status = Column(String, default="Open")
    started_date = Column(DateTime)
    no_of_openings = Column(Integer)
    other_details = Column(TEXT)
    required_details = Column(String)
    assignment = Column(TEXT)
    assignment_file = Column(String)
    assignment_link = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime, default=dt)
    modified_by = Column(String)
    modified_on = Column(DateTime, default=dt)

    # is_deleted = Column(Boolean, default=False)

    # relationship between Employer and jobpost
    job_post_owner = relationship(
        "Employer", back_populates="jobpost", uselist=False)

    job_post_owner1 = relationship(
        "JobCandidate", back_populates="job_candidate_owner1", uselist=False)

    job_post_chat = relationship(
        "JobCandidateChat", back_populates="chat_owner1", uselist=False)

    # job_post_interview = relationship(
    #     "JobCandidateInterView", back_populates="interview_jobpost", uselist=False)


class Candidate(Base):
    __tablename__ = "candidate"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # expiry_date = Column(DateTime, default=dt)
    address = Column(String)
    current_location = Column(String)
    country_code = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)
    isProfileCompleted = Column(Boolean, default=False)
    photo = Column(String)
    resume = Column(String)
    profile_summery = Column(TEXT)
    video_profile = Column(String)
    total_no_of_years_exp = Column(Integer)
    total_no_of_month_exp = Column(Integer)
    prefered_job_location = Column(String, default="Any")
    prefered_job_type = Column(String, default="Any",)
    prefered_job_tenuer = Column(String, default="Any",)
    prefered_job_mode = Column(String, default="Any",)
    current_ctc = Column(Integer, default=0)
    excepted_ctc_min = Column(Integer, default=0)
    excepted_ctc_max = Column(Integer)
    qualification = Column(String)
    skill = Column(String)
    notice_period = Column(String)
    # sub_domain = Column(String)

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    verification_code = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime, default=dt)
    modified_by = Column(String)
    modified_on = Column(DateTime, default=dt)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    # # Constraints
    # __table_args__ = (UniqueConstraint(
    #     'username', 'sub_domain', name='unq_2'),)

    candidates = relationship(
        "JobCandidate", back_populates="job_candidate_owner2", uselist=False)

    candidates_chat = relationship(
        "JobCandidateChat", back_populates="chat_owner2", uselist=False)

    # candidates_interivew = relationship(
    #     "JobCandidateInterView", back_populates="interview_candidate", uselist=False)


class JobCandidate(Base):
    __tablename__ = "job_candidate"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey(
        "jobpost.id"))  # refer from JobPost table

    candidate_id = Column(Integer, ForeignKey(
        "candidate.id"))  # refer from Candidate table

    ans_to_required_deatail = Column(TEXT)
    cover_letter = Column(TEXT)
    assignment_reply = Column(TEXT)
    assignment_submission_file = Column(String)
    assignement_submited_on = Column(DateTime, default=dt)
    evaluation_score = Column(Integer, default=0)
    evaluation_mark = Column(String)
    evaluation_document = Column(String)
    candidate_comment = Column(String)
    employer_comment = Column(String)

    applied = Column(String, default="No")
    applied_on = Column(DateTime)

    interested = Column(String, default="No")
    interested_on = Column(DateTime)

    shortlisted = Column(String, default="No")
    shortlisted_on = Column(DateTime)

    rejected = Column(String, default="No")
    rejected_on = Column(DateTime)

    hired = Column(String, default="No")
    hired_on = Column(DateTime)

    withdrawn = Column(String, default="No")
    withdrawn_on = Column(DateTime)

    status = Column(String)

    created_by = Column(String)
    created_on = Column(DateTime, default=dt)
    modified_by = Column(String)
    modified_on = Column(DateTime, default=dt)

    # Constraints
    __table_args__ = (UniqueConstraint(
        'job_id', 'candidate_id', name='unq_3'),)

    job_candidate_owner1 = relationship(
        "JobPost", back_populates="job_post_owner1", uselist=False)

    job_candidate_owner2 = relationship(
        "Candidate", back_populates="candidates", uselist=False)

    job_candidate_interview = relationship(
        "JobCandidateInterView", back_populates="interview_job_candidate", uselist=False)


class JobCandidateChat(Base):
    __tablename__ = "job_candidate_chat"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey(
        "jobpost.id"))  # refer from JobPost table

    candidate_id = Column(Integer, ForeignKey(
        "candidate.id"))  # refer from Candidate table

    employer_id = Column(Integer, ForeignKey(
        "employer.id"))  # refer from Employer table

    chat_message = Column(String)
    attatchment = Column(String)
    chat_date = Column(DateTime, default=dt)

    created_by = Column(String)
    created_on = Column(DateTime, default=dt)

    # # Constraints
    # not need below fields/constriants
    # __table_args__ = (UniqueConstraint(
    #     'job_id', 'candidate_id', 'id', name='unq_4'),)

    # __table_args__ = (UniqueConstraint(
    #     'job_id', 'employer_id', 'id', name='unq_5'),)

    chat_owner1 = relationship(
        "JobPost", back_populates="job_post_chat", uselist=False)

    chat_owner2 = relationship(
        "Candidate", back_populates="candidates_chat", uselist=False)


class JobCandidateInterView(Base):
    __tablename__ = "job_candidate_interview"
    id = Column(Integer, primary_key=True, index=True)

    job_candidate_id = Column(Integer, ForeignKey(
        "job_candidate.id"))  # refer from Candidate table

    # interview_round_no = Column(Integer, index=True, autoincrement=1)
    interview_title = Column(String)
    interview_date = Column(DateTime)
    interview_time = Column(String)
    interview_score = Column(Integer)
    interview_remarks = Column(String)
    interview_document = Column(String)

    is_deleted = Column(Boolean, default=False)
    created_by = Column(String)

    created_on = Column(DateTime, default=dt)
    modified_by = Column(String)
    modified_on = Column(DateTime, default=dt)

    interview_job_candidate = relationship(
        "JobCandidate", back_populates="job_candidate_interview", uselist=False)


class JobFunction (Base):
    __tablename__ = "job_function"
    id = Column(Integer, primary_key=True, index=True)
    job_function = Column(String, nullable=False)
    employer_id = Column(Integer, ForeignKey("employer.id"))

    __table_args__ = (UniqueConstraint(
        'job_function', 'employer_id', name='unq_6'),)

    # relationship between UOM(Unit of Measurement) and Company
    job_function_owner = relationship("Employer", backref="owner_job_function")


class Qualification (Base):
    __tablename__ = "qualification"
    id = Column(Integer, primary_key=True, index=True)
    qualification = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('qualification', 'id', name='unq_7'),)


class Skill (Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True, index=True)
    skill = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('skill', 'id', name='unq_8'),)
