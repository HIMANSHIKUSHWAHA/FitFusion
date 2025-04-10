from database.db import SessionLocal
from database.models import User, Plan
from datetime import datetime
from core.calculators import calculate_bmr, calculate_tdee
from agents.behavior_agent import get_behavior_feedback  # inter-agent communication
from crewai import Agent  # agent framework (pluggable later with Ollama)

class CalorieCoachAgent:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.db = SessionLocal()

    def fetch_user(self):
        return self.db.query(User).filter(User.id == self.user_id).first()

    def analyze_behavior(self, user):
        return get_behavior_feedback(user.id)  # 👈 agent-to-agent communication

    def decide_calories(self, bmr, tdee, goal, feedback):
        # Smart decision based on goal and feedback
        if goal == "cut":
            if feedback == "inconsistent":
                return int(tdee - 300)  # small cut to avoid burnout
            return int(tdee - 500)
        elif goal == "bulk":
            if feedback == "low energy":
                return int(tdee + 600)
            return int(tdee + 400)
        else:
            return int(tdee)

    def generate_plan(self):
        user = self.fetch_user()
        if not user:
            return {"error": "User not found"}

        bmr = calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
        tdee = calculate_tdee(bmr, user.activity_level)
        feedback = self.analyze_behavior(user)

        final_calories = self.decide_calories(bmr, tdee, user.goal, feedback)

        plan = Plan(
            user_id=user.id,
            date=datetime.utcnow(),
            calories_target=final_calories,
            meal_plan="",  # will be filled by nutrition agent
            workout_plan=""
        )
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)

        return {
            "agent": "CalorieCoach",
            "status": "Plan created",
            "calories": final_calories,
            "feedback_used": feedback,
            "goal": user.goal
        }
