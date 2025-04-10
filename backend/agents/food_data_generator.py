import pandas as pd
import subprocess
import os

# Configuration
cuisines = ["Japanese", "Korean", "Indian", "Italian", "French", "Continental", "Mediterranean"]
meal_types = ["Breakfast", "Lunch", "Dinner"]
diet_types = ["Veg", "Non-Veg"]

# Ollama model to use (must be pulled already, e.g., `ollama pull tinyllama`)
OLLAMA_MODEL = "tinyllama"

# Prompt for dish generation with nutrition and allergen info
def generate_dish_prompt(cuisine: str, meal_type: str, diet: str) -> str:
    return (
        f"Suggest a {diet.lower()} {meal_type.lower()} dish from {cuisine} cuisine. "
        f"Include:\n"
        f"1. Dish Name\n"
        f"2. Short Description\n"
        f"3. Tags\n"
        f"4. Calories (kcal)\n"
        f"5. Protein (g)\n"
        f"6. Fat (g)\n"
        f"7. Carbohydrates (g)\n"
        f"8. Common Allergens (if any, e.g., dairy, gluten, nuts, soy, eggs, shellfish)"
    )

# Call Ollama model using subprocess
def call_ollama(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"Error: {e}"

# Parse the model's response into structured data
def parse_response(response: str, cuisine: str, meal_type: str, diet: str) -> dict:
    lines = [line.strip() for line in response.split('\n') if line.strip()]
    data = {
        "Dish Name": "",
        "Description": "",
        "Cuisine": cuisine,
        "Meal Type": meal_type,
        "Diet": diet,
        "Tags": f"{cuisine}, {meal_type}, {diet}",
        "Calories (kcal)": "",
        "Protein (g)": "",
        "Fat (g)": "",
        "Carbohydrates (g)": "",
        "Allergens": ""
    }

    for line in lines:
        if "Dish Name" in line:
            data["Dish Name"] = line.split(":", 1)[-1].strip()
        elif "Description" in line:
            data["Description"] = line.split(":", 1)[-1].strip()
        elif "Tags" in line:
            data["Tags"] += ", " + line.split(":", 1)[-1].strip()
        elif "Calories" in line:
            data["Calories (kcal)"] = line.split(":", 1)[-1].strip()
        elif "Protein" in line:
            data["Protein (g)"] = line.split(":", 1)[-1].strip()
        elif "Fat" in line:
            data["Fat (g)"] = line.split(":", 1)[-1].strip()
        elif "Carbohydrates" in line:
            data["Carbohydrates (g)"] = line.split(":", 1)[-1].strip()
        elif "Allergens" in line:
            data["Allergens"] = line.split(":", 1)[-1].strip()

    return data

# Generate data across all combinations
def generate_dishes_per_category(num_per_category=10) -> pd.DataFrame:
    all_dishes = []
    for cuisine in cuisines:
        for meal_type in meal_types:
            for diet in diet_types:
                print(f"🍽️ Generating {num_per_category} dishes for {cuisine} | {meal_type} | {diet}")
                for _ in range(num_per_category):
                    prompt = generate_dish_prompt(cuisine, meal_type, diet)
                    response = call_ollama(prompt)
                    dish = parse_response(response, cuisine, meal_type, diet)
                    all_dishes.append(dish)
    return pd.DataFrame(all_dishes)

# Save the generated dataset
def save_dataset(filepath="backend/data/nutrition.csv", num_per_category=10):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    dataset = generate_dishes_per_category(num_per_category)
    dataset.to_csv(filepath, index=False)
    print(f"✅ Dataset saved to {filepath}")

# Main execution
if __name__ == "__main__":
    save_dataset()
