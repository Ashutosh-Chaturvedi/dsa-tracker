from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from database import engine, SessionLocal
import models

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
    
    easy_problems = query.filter(models.Problem.difficulty == "easy").all()
    easy_problems_count = len(easy_problems)
    
    medium_problems = query.filter(models.Problem.difficulty == "medium").all()
    medium_problems_count = len(medium_problems)
    
    hard_problems = query.filter(models.Problem.difficulty == "hard").all()
    hard_problems_count = len(hard_problems)
    
    leetcode_problems = query.filter(models.Problem.platform == "leetcode").all()
    leetcode_problems_count = len(leetcode_problems)
    
    hackerrank_problems = query.filter(models.Problem.platform == "hackerrank").all()
    hackerrank_problems_count = len(hackerrank_problems)
    
    other_platform_problems = query.filter(models.Problem.platform != "leetcode" or models.Problem.platform != "hackerrank").all()
    other_platform_problems_count = len(other_platform_problems)
    
    db.close()
    
    return {
        "status": "success",
        "total_problems_count" : counts, 
        "easy_problems_count" : easy_problems_count, 
        "medium_problems_count" : medium_problems_count,
        "hard_problems_count" : hard_problems_count,
        "problems_based_on_difficulty":{
            "easy": easy_problems,
            "medium": medium_problems,
            "hard": hard_problems
        },
        "leetcode_problems_count" : leetcode_problems_count,
        "hackerrank_problems_count" : hackerrank_problems_count,
        "other_platform_count" : other_platform_problems_count,
        "problems_based_on_platform":{
            "leetcode": leetcode_problems,
            "hackerrank": hackerrank_problems,
            "other": other_platform_problems
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
        query = query.filter(models.Problem.difficulty == difficulty)
        
    if topic is not None: 
        query = query.filter(models.Problem.topics.contains(topic))
        
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
            "notes": p.notes
        })
        
    return {"status": "success", "data": result}
