from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import database, schemas, models,oauth2

router = APIRouter(prefix="/api/qualification",tags=["Qualification"])

get_db = database.get_db

@router.post("/create-qualification")
def createUOM(request:schemas.QualificationBase,db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_employer = current_user
        _username_ = current_employer.user["username"]

        checkQuali = db.query(models.Qualification).filter(models.Qualification.qualification==request.qualification).first()
        
        if checkQuali:
                raise HTTPException(status_code=status.HTTP_302_FOUND,detail="Qualification already exists!")

        new_quali = models.Qualification(qualification=request.qualification)
        db.add(new_quali)
        db.commit()
        db.refresh(new_quali)

        return {f"Added new qualification"}

@router.get("/show-qualifications")
def showsUOM(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_employer = current_user
        _username_ = current_employer.user["username"]

        all_quali = db.query(models.Qualification).all()

        return list(set(all_quali))
