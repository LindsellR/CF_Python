recipe_list = []
ingredients_list = []

def take_recipe():
    name = str(input("Recipe name: "))
    cooking_time = int(input("Enter cooking time in minutes: "))
    ingredients = list(input("Enter the ingredients, separated by a comma: ").split(","))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
    }
    return recipe

n = int(input("How many recipes would you like to enter?: "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

    recipe_list.append(recipe)

for recipe in recipe_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"

    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
        
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

for recipe in recipe_list:
    print("Recipe: ", recipe["name"])
    print("Cooking_Time: ", recipe["cooking_time"])
    print("Ingredients: ", recipe["ingredients"])
    print("Difficulty: ", recipe["difficulty"])

        
def all_ingredients():
    print("Ingredients Available Across All Recipes")
    print("________________________________________")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()

