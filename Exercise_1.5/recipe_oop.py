class Recipe(object):

    all_ingredients = []

    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None
        self.update_all_ingredients()

    def get_name(self):
        return self._name

    def set_name(self, name):
        self.name = name

    def get_ingredients(self):
        return self.ingredients

    def set_ingredients(self, ingredients):
        self.ingredients = ingredients
        self.update_all_ingredients()
        self.difficulty = None  # Reset difficulty if ingredients change

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cookingtime = cooking_time

    def calculate_difficulty(self):
        # Calculates and updates recipe's difficulty
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"

        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"

        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"

        else:
            self.difficulty = "Hard"

    # Returns the recipes difficulty, calculating if needed
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        # Return True if ingredient is in the recipe (case-insensitive).
        return ingredient.lower() in (ing.lower() for ing in self.ingredients)

    def update_all_ingredients(self):
        # Add the recipe's ingredients to the class-level all_ingredients list if not already present
        for ing in self.ingredients:
            if ing.lower() not in (i.lower() for i in Recipe.all_ingredients):
                Recipe.all_ingredients.append(ing)

    def __str__(self):
        return (
            f"Recipe Name: {self.name}\n"
            f"Ingredients: {', '.join(self.ingredients)}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.get_difficulty()}"
        )

def recipe_search(data, search_term):
        # Search for recipes containing a given ingredient.
    found = False
    for recipe in data:
         if recipe.search_ingredient(search_term):
            found = True
            print(recipe)
            print("-" * 40)  #separator for readability
    if not found:
        print(f"No recipes found containing '{search_term}'.")

        # Initialize the object


tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
coffee = Recipe("Coffee", ["Coffee powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
banana_smoothie = Recipe("Banana Smoothie", ["Banana", "Milk", "Sugar", "Ice Cubes"], 5)

recipes_list = [tea, coffee, cake, banana_smoothie]

for recipe in recipes_list:
    print(recipe)
    print("-" * 40)

for ingredient in ["Water", "Sugar", "Banana"]:
    recipe_search(recipes_list, ingredient)