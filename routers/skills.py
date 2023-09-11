from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import database, schemas, models,oauth2

router = APIRouter(prefix="/api/skill",tags=["Skills"])

get_db = database.get_db

@router.post("/create-skill")
def createUOM(request:schemas.SkillBase,db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_employer = current_user
        _username_ = current_employer.user["username"]

        checkJobFunc = db.query(models.Skill).filter(models.Skill.skill==request.skill).first()
        
        if checkJobFunc:
                raise HTTPException(status_code=status.HTTP_302_FOUND,detail="Skill already exists!")

        new_skill = models.Skill(skill=request.skill)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)

        return {f"Added new skill"}

@router.get("/show-skills")
def showsUOM(db:Session = Depends(get_db),current_user:schemas.UsersRead = Depends(oauth2.get_current_user)):
        current_employer = current_user
        _username_ = current_employer.user["username"]

        all_skill = db.query(models.Skill).all()

        return list(set(all_skill))
