from fastapi import APIRouter
from agents.nutrition_agent import generate_meal_plan
from agents.calorie_agent import CalorieCoachAgent

router = APIRouter(prefix="/planner", tags=["Planner"]) 

@router.post("/diet")
def get_diet_plan(user_input: dict):
    """
    Generate a diet plan based on user input.
    """
    plan = generate_meal_plan(user_input)
    return {"status": "success", "plan": plan}

@router.get("/calories/{user_id}")
def get_calorie_plan(user_id: int):
    agent = CalorieCoachAgent(user_id)
    return agent.generate_plan()