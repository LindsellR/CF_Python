import pickle

with open("recipe_binary.bin", "rb") as my_file:
    recipe = pickle.load(my_file)

print("Recipe details - "),
print("Name:  " + recipe["name"])
print("Ingredients: " + ", ".join(recipe["ingredients"]))
print("Cooking Time:  " + recipe["cooking_time"])
print("Difficulty: " + recipe["difficulty"])
