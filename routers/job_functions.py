from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import database, schemas, models,oauth2

router = APIRouter(prefix="/api/job-function",tags=["Job Functions"])

get_db = database.get_db

@router.post("/create-job-function")
def createUOM(request:schemas.JobFunctionBase,db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_employer = current_user
        _username_ = current_employer.user["username"]

        val_employer = db.query(models.Employer).filter(
        models.Employer.username == _username_).first()

        if val_employer:
                checkJobFunc = db.query(models.JobFunction).filter(models.JobFunction.job_function==request.job_function).first()
                
                if checkJobFunc:
                        raise HTTPException(status_code=status.HTTP_302_FOUND,detail="Job function already exists!")
        
                new_job_func = models.JobFunction(job_function=request.job_function,employer_id=val_employer.id)
                db.add(new_job_func)
                db.commit()
                db.refresh(new_job_func)

                return {f"Added new job function"}
        
        else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="sorry! You can not create Job function")

@router.get("/show-job-functions")
def showsUOM(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_employer = current_user
        _username_ = current_employer.user["username"]

        val_employer = db.query(models.Employer).filter(
                models.Employer.username == _username_).first()

        if not val_employer:
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Not authenticated to view job functions")
        else:
                all_job_func = db.query(models.JobFunction).all()

                return list(set(all_job_func))
