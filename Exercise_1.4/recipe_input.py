import pickle


def take_recipe():
    # Get recipe name, ensuring it's not empty
    while True:
        name = input("Recipe name: ").strip()
        if name:
            break
        print("Recipe name cannot be empty. Please enter a valid name.")

    # Get cooking time, ensuring it's a positive integer
    while True:
        cooking_time_input = input("Enter cooking time in minutes: ").strip()
        if cooking_time_input.isdigit():
            cooking_time = int(cooking_time_input)
            if cooking_time > 0:
                break
        print("Please enter a valid positive number for cooking time.")

    # Get ingredients, ensuring at least one valid ingredient
    while True:
        ingredients_input = input(
            "Enter the ingredients, separated by a comma: "
        ).strip()
        ingredients = [
            item.strip().lower()
            for item in ingredients_input.split(",")
            if item.strip()
        ]
        if ingredients:
            break
        print("Please enter at least one ingredient.")

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
    }
    return recipe


def calc_difficulty(cooking_time, ingredients):

    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"

    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"

    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"

    else:
        return "Hard"


filename = input("Enter the filename to load recipes from: ")

data = None  # default if loading fails

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print(f"File '{filename}' not found. Starting with empty data.")
except pickle.UnpicklingError:
    print(f"File '{filename}' is not a valid pickle file or is corrupted.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print(f"Data loaded successfully from '{filename}'")
finally:
    if data is None:
        # Initialize with empty structure if loading failed
        data = {"recipes_list": [], "all_ingredients": []}

# Now you can safely use data['recipes_list'] and data['all_ingredients']
print(f"Number of recipes loaded: {len(data['recipes_list'])}")
print(f"Number of unique ingredients loaded: {len(data['all_ingredients'])}")

n = int(input("How many recipes would you like to enter?: "))

for i in range(n):
    recipe = take_recipe()
    # Calculate and add difficulty
    difficulty = calc_difficulty(recipe["cooking_time"], recipe["ingredients"])
    recipe["difficulty"] = difficulty

    for ingredient in recipe["ingredients"]:
        ingredient = ingredient.strip()  # clean whitespace
        if ingredient not in data["all_ingredients"]:
            data["all_ingredients"].append(ingredient)

    data["recipes_list"].append(recipe)

with open(filename, "wb") as file:
    pickle.dump(data, file)

print(f"{n} recipes saved to {filename}")
