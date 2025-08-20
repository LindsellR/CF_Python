import mysql.connector


def create_database():
    """Create the database and recipes table if they don't exist, then return connection and cursor."""
    conn = mysql.connector.connect(
        host="localhost", user="root", password="password"
    )
    cursor = conn.cursor()

    # Create and use database
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database;")
    cursor.execute("USE task_database;")

    # Create recipes table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            ingredients VARCHAR(255),
            cooking_time INT,
            difficulty VARCHAR(20)
        )
    """
    )

    conn.commit()
    return conn


def calculate_difficulty(cooking_time, ingredients):
    """Determine recipe difficulty based on cooking_time and number of ingredients."""
    num_ingredients = len(ingredients.split(","))
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"


def create_recipe(conn, cursor):
    """Add a new recipe to the database."""
    name = input("Enter recipe name: ")
    cooking_time = int(input("Enter cooking time (minutes): "))
    ingredients = input("Enter ingredients (comma-separated): ")

    difficulty = calculate_difficulty(cooking_time, ingredients)

    cursor.execute(
        "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)",
        (name, ingredients, cooking_time, difficulty),
    )
    conn.commit()
    print(f"Recipe '{name}' added successfully!")


def recipe_search(conn, cursor):
    """Search recipes by ingredient."""
   
    cursor.execute("SELECT ingredients FROM recipes")
    all_ingredients = [row[0] for row in cursor.fetchall()]
    unique_ingredients = sorted(set(",".join(all_ingredients).split(",")))

    print("\nAvailable Ingredients:")
    for idx, ingredient in enumerate(unique_ingredients, start=1):
        print(f"{idx}. {ingredient.strip()}")

    try:
        choice = int(input("Choose ingredient by number: ")) - 1
        selected_ingredient = unique_ingredients[choice].strip()
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    cursor.execute(
        "SELECT * FROM recipes WHERE ingredients LIKE %s", (f"%{selected_ingredient}%",)
    )
    results = cursor.fetchall()

    print(f"\nRecipes with '{selected_ingredient}':")
    for recipe in results:
        print(recipe)


def update_recipe(conn, cursor):
    """Update an existing recipe by ID."""
    cursor.execute("SELECT * FROM recipes")
    recipes = cursor.fetchall()

    print("\nAvailable Recipes:")
    for recipe in recipes:
        print(recipe)

    try:
        recipe_id = int(input("Enter the recipe ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Cooking Time")
    print("3. Ingredients")
    choice = input("Enter choice (1-3): ")

    if choice == "1":
        new_value = input("Enter new name: ")
        cursor.execute("UPDATE recipes SET name=%s WHERE id=%s", (new_value, recipe_id))

    elif choice == "2":
        new_value = int(input("Enter new cooking time: "))
        cursor.execute("SELECT ingredients FROM recipes WHERE id=%s", (recipe_id,))
        ingredients = cursor.fetchone()[0]
        difficulty = calculate_difficulty(new_value, ingredients)
        cursor.execute(
            "UPDATE recipes SET cooking_time=%s, difficulty=%s WHERE id=%s",
            (new_value, difficulty, recipe_id),
        )

    elif choice == "3":
        new_value = input("Enter new ingredients (comma-separated): ")
        cursor.execute("SELECT cooking_time FROM recipes WHERE id=%s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]
        difficulty = calculate_difficulty(cooking_time, new_value)
        cursor.execute(
            "UPDATE recipes SET ingredients=%s, difficulty=%s WHERE id=%s",
            (new_value, difficulty, recipe_id),
        )
    else:
        print("Invalid option.")
        return

    conn.commit()
    print("Recipe updated successfully!")


def delete_recipe(conn, cursor):
    """Delete a recipe by ID."""
    cursor.execute("SELECT id, name FROM recipes")
    recipes = cursor.fetchall()

    print("\nAvailable Recipes to Delete:")
    for recipe in recipes:
        print(f"ID: {recipe[0]} | Name: {recipe[1]}")

    try:
        recipe_id = int(input("Enter the recipe ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    cursor.execute("DELETE FROM recipes WHERE id=%s", (recipe_id,))
    conn.commit()
    print("Recipe deleted successfully!")


def main_menu(conn, cursor):
    """Main menu loop."""
    while True:
        print("\nMain Menu:")
        print("1. Add a recipe")
        print("2. Search for a recipe")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        print("5. Exit")

        choice = input("Enter an option (1-5): ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            recipe_search(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            print(" Goodbye!")
            cursor.close()
            conn.close()
            break
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    conn = create_database()
    cursor = conn.cursor()
    main_menu(conn, cursor)
