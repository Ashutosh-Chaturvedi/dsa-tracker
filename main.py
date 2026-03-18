from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from database import engine, SessionLocal
import models
from sqlalchemy import func

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DSA Tracker")

class Problem(BaseModel):
    title: str
    platform: str
    difficulty: str
    topics: List[str]
    notes: str
    
class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    platform: Optional[str] = None
    difficulty: Optional[str] = None
    topics: Optional[List[str]] = None
    notes: Optional[str] = None
    
@app.get("/stats")
def stats():
    db = SessionLocal()
    query = db.query(models.Problem)
    
    problems = query.all()
    counts = len(problems)

    easy_problems_count = db.query(func.count()).filter(func.lower(models.Problem.difficulty) == "easy").scalar()
 
    medium_problems_count = db.query(func.count()).filter(func.lower(models.Problem.difficulty) == "medium").scalar()

    hard_problems_count = db.query(func.count()).filter(func.lower(models.Problem.difficulty) == "hard").scalar()
 
    leetcode_problems_count = db.query(func.count()).filter(func.lower(models.Problem.platform) == "leetcode").scalar()
    
    hackerrank_problems_count = db.query(func.count()).filter(func.lower(models.Problem.difficulty) == "hackerrank").scalar()

    other_count = db.query(func.count()).filter(
        ~func.lower(models.Problem.platform).in_(["leetcode", "hackerrank"])
    ).scalar()
    
    db.close()
    
    return {
        "status": "success",
        "data": {
            "total" : counts,
            "difficulty": {
                "easy": easy_problems_count,
                "medium": medium_problems_count,
                "hard": hard_problems_count
            },
            "platform": {
                "leetcode": leetcode_problems_count,
                "hackerrank": hackerrank_problems_count,
                "others": other_count 
            }
        }
    }

@app.post('/problems')
def add_problem(problem: Problem):
    db = SessionLocal()
    
    db_problem = models.Problem(
        title=problem.title,
        platform=problem.platform,
        difficulty=problem.difficulty,
        topics=",".join(problem.topics),
        notes=problem.notes
    )
    
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    db.close()
    
    return {"status": "success", "id": db_problem.id}

@app.get("/problems/{problem_id}")
def get_by_id(problem_id: int):
    db = SessionLocal()
    p = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    db.close()
    
    if p is None:
        return {"status":"error", "message":"Problem not found"}

    return {
        "status": "success",
        "data": {
            "id": p.id,
            "title": p.title,
            "platform": p.platform,
            "difficulty": p.difficulty,
            "topics": p.topics.split(",") if p.topics else [],
            "notes": p.notes
        }
    }
    
@app.patch("/problems/{problem_id}")
def update_problem(problem_id: int, updated_data: ProblemUpdate):
    db = SessionLocal()
    
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first() 
    
    if problem is None:
        db.close()
        return {"status":"error", "message":"Problem not found"}
    
    if updated_data.title is not None: 
        problem.title = updated_data.title
    if updated_data.difficulty is not None: 
        problem.difficulty = updated_data.difficulty
    if updated_data.platform is not None: 
        problem.platform = updated_data.platform
    if updated_data.topics is not None: 
        problem.topics = ",".join(updated_data.topics)
    if updated_data.notes is not None: 
        problem.notes = updated_data.notes
    
    db.commit()
    db.refresh(problem)
    db.close()
    
    return problem
    
@app.delete("/problems/{problem_id}")
def delete_problem(problem_id: int):
    db = SessionLocal()
    
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    
    if problem is None:
        db.close()
        return {"status":"error", "message":"Problem not found"}
    
    db.delete(problem)
    db.commit()
    db.close()
    
    return {"status":"success", "message": f"Problem of id: {problem_id} deleted successfully", "deleted_data": problem}
    
    
@app.get("/problems")
def get_problems(difficulty: Optional[str] = None, topic: Optional[str] = None):
    db = SessionLocal()
    
    query = db.query(models.Problem)
    
    if difficulty is not None: 
        query = query.filter(func.lower(models.Problem.difficulty) == func.lower(difficulty))
        
    if topic is not None: 
        query = query.filter(func.lower(models.Problem.topics).contains(func.lower(topic)))
        
    problems = query.all()
    db.close()
    
    result = []
    
    for p in problems:
        result.append({
            "id": p.id,
            "title": p.title,
            "platform": p.platform,
            "difficulty": p.difficulty,
            "topics": p.topics.split(",") if p.topics else [],
            "notes": p.notes,
            # "created_at": p.created_at
        })
        
    return {"status": "success", "data": result}
