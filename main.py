from fastapi import FastAPI
from internal import authentication, registration
import models
from database import engine
from routers import utility, employer, candidate, job_post, job_candidate, job_candidate_chat, job_candidate_interview, search, job_functions, qualifications, skills, admin, whtsms
from fastapi.middleware.cors import CORSMiddleware

# creating tables in the database
models.Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(registration.router)
app.include_router(employer.router)
app.include_router(candidate.router)
app.include_router(job_post.router)
app.include_router(search.router)
app.include_router(job_candidate.router)
app.include_router(job_candidate_chat.router)
app.include_router(job_candidate_interview.router)
app.include_router(utility.router)
app.include_router(job_functions.router)
app.include_router(qualifications.router)
app.include_router(skills.router)
app.include_router(admin.router)
app.include_router(whtsms.router)
