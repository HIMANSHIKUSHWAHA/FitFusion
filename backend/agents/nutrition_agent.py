def generate_meal_plan(user_input):
    goal = user_input.get("goal", "maintain")
    preference = user_input.get("diet", "vegetarian")
    calories = user_input.get("calories", 2000)

    if goal == "cut":
        meals = ["Oats + banana", "Grilled tofu salad", "Lentil soup"]
    elif goal == "bulk":
        meals = ["Avocado toast", "Chickpea curry + rice", "Peanut butter smoothie"]
    else:
        meals = ["Veg sandwich", "Rice + dal", "Paneer salad"]

    return {
        "target_calories": calories,
        "goal": goal,
        "diet": preference,
        "meals": meals
    }
