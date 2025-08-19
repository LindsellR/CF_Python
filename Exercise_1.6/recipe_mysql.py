import mysql.connector

# Create the database (if it doesn't exist yet)
def create_database():
    conn = mysql.connector.connect(
        host="localhost", user="cf-python", passwd="password"
    )
    cursor = conn.cursor()
    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
    # Switch to that database
    cursor.execute("USE task_database")

    # Create the recipes table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        ingredients VARCHAR(250) NOT NULL,
        cooking_time INT,
        difficulty VARCHAR(20)
        )
    """
    )

    conn.commit()
    return conn

# Function to calculate difficulty
def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"


# Function to create a recipe
def create_recipe(conn, cursor):
    name = input("Enter recipe name: ")
    ingredients = input("Enter ingredients (comma separated): ").split(",")
    ingredients = [ing.strip() for ing in ingredients]  # clean spaces
    cooking_time = int(input("Enter cooking time in minutes: "))

    difficulty = calculate_difficulty(cooking_time, ingredients)

    # Store as comma-separated string in DB
    ingredients_str = ", ".join(ingredients)

    cursor.execute(
        "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)",
        (name, ingredients_str, cooking_time, difficulty),
    )
    conn.commit()
    print(f"Recipe '{name}' added with difficulty: {difficulty}")

def recipe_search(conn, cursor):
    # Step 1: get all ingredients across all recipes
    cursor.execute("SELECT ingredients FROM recipes")
    rows = cursor.fetchall()

    all_ingredients = set()
    for row in rows:
        ingredients_list = row[0].split(",")
        for ing in ingredients_list:
            all_ingredients.add(ing.strip())

    all_ingredients = sorted(all_ingredients)

    if not all_ingredients:
        print("No ingredients found in the database.")
        return []

    print("\nIngredients Available Across All Recipes")
    print("________________________________________")
    for idx, ingredient in enumerate(all_ingredients, start=1):
        print(f"{idx}. {ingredient}")

    # Step 2: let user pick one ingredient
    try:
        choice = int(input("\nEnter the number of the ingredient to search for: "))
        if choice < 1 or choice > len(all_ingredients):
            raise ValueError("Number out of range")
        ingredient_searched = all_ingredients[choice - 1]
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter a valid number.")
        return []

    # Step 3: search recipes containing that ingredient
    query = "SELECT name, ingredients, cooking_time, difficulty FROM recipes WHERE ingredients LIKE %s"
    cursor.execute(query, (f"%{ingredient_searched}%",))
    results = cursor.fetchall()

    # Step 4: display results
    if results:
        print(f"\nRecipes containing '{ingredient_searched}':")
        for idx, (name, ingredients, cooking_time, difficulty) in enumerate(results, start=1):
            print(f"\nRecipe {idx}:")
            print(f"Name: {name}")
            print(f"Difficulty: {difficulty}")
            print(f"Cooking Time: {cooking_time} minutes")
            print(f"Ingredients: {ingredients}")
    else:
        print(f"No recipes found containing '{ingredient_searched}'.")

    return results


def main_menu(conn, cursor):
    while True:
        print("\Main Menu:")
        print("Please choose an option.")
        print("Option 1: Add a recipe.")
        print("Option 2: Search for a recipe.")
        print("Option 3: Change a recipe.")
        print("Option 4: Delete a recipe")
        print(" Option 5: Exit the app.")

        choice = input("Please enter an option (1-5):")

        if choice == '1':
            create_recipe(conn, cursor)

        elif choice == '2':
            recipe_search(conn, cursor)

        elif choice == '3':
            update_recipe(conn, cursor)

        elif choice == '4':
            delete_recipe(conn, cursor)

        elif choice == '5':
            print("Goodbye")
            cursor.close()
            conn.close()
        
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    conn = create_database()

    print("Database and table ready!")
   
    # now you can run queries without reconnecting
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for table in cursor.fetchall():
        print(table)
    
