import pickle


def display_recipe(data):

    if not data["recipes_list"]:
        print("Recipes not found.")
        return

    for idx, r in enumerate(data["recipes_list"], start=1):
        print(f"\nRecipe {idx}:")
        print(f"Name: {r['name']}")
        print(f"Difficulty: {r['difficulty']}")
        print(f"Cooking Time: {r['cooking_time']} minutes")
        print(f"Ingredients: {', '.join(r['ingredients'])}")


def search_ingredients(data):
    all_ingredients = data.get("all_ingredients", [])

    if not all_ingredients:
        print("Ingredients not found")
        return

    print("Ingredients Available Across All Recipes")
    print("________________________________________")

    for idx, ingredient in enumerate(all_ingredients, start=1):
        print(f"{idx}. {ingredient}")

    try:
        choice = int(input("\nEnter the number of the ingredient to search for: "))
        if choice < 1 or choice > len(all_ingredients):
            raise ValueError("Number out of range")
        ingredient_searched = all_ingredients[choice - 1]
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter a valid number.")
    else:
        print(f"\nRecipes containing '{ingredient_searched}':")
        found = False
        for idx, recipe in enumerate(data["recipes_list"], start=1):
            # Check if ingredient is in recipe (case-insensitive)
            if ingredient_searched.lower() in (
                ing.lower() for ing in recipe["ingredients"]
            ):
                found = True
                print(f"\nRecipe {idx}:")
                print(f"Name: {recipe['name']}")
                print(f"Difficulty: {recipe['difficulty']}")
                print(f"Cooking Time: {recipe['cooking_time']} minutes")
                print(f"Ingredients: {', '.join(recipe['ingredients'])}")
        if not found:
            print("No recipes found containing that ingredient.")


def main():
    filename = input("Enter the filename to load recipes from: ")

    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found. Please check the filename.")
    else:
        display_recipe(data)
        search_ingredients(data)
    # run program
main()
