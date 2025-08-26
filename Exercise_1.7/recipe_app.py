from dotenv import load_dotenv

import os
import mysql.connector

from sqlalchemy import create_engine, Column, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import Integer, String
from sqlalchemy.exc import SQLAlchemyError

# Load .env file
load_dotenv()

# Read values from .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
db = os.getenv("DB_NAME")

# create engine
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db}")

# Base variable: Models will inherit from this class
Base = declarative_base()

# Session object to make changes to database
Session = sessionmaker(bind=engine)
session = Session()


class Recipe(Base):
    __tablename__ = "complete_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe ID: {self.id} - {self.name}>"

    def __str__(self):
        # Make sure ingredients are formatted cleanly
        if self.ingredients:
            # split on comma, strip spaces, then rejoin with ", "
            formatted_ingredients = ", ".join(
                [i.strip() for i in self.ingredients.split(",")]
            )
        else:
            formatted_ingredients = "None listed"

        return (
            f"Recipe: {self.name}\n"
            f"ID: {self.id}\n"
            f"Ingredients: {formatted_ingredients}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.difficulty}\n"
            "\n"
        )

    def calculate_difficulty(self):
        # Calculates and updates recipe's difficulty determined by amount of ingredients and cooking time
        if self.ingredients:
            num_ingredients = len(
                [i.strip() for i in self.ingredients.split(",") if i.strip()]
            )
        else:
            num_ingredients = 0

        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"

        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"

        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"

        else:
            self.difficulty = "Hard"

    # Returns the recipes difficulty, calculating if needed
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")


# Creates table on the database based on the defined model.
Base.metadata.create_all(engine)


def create_recipe(session):
    """Collects recipe details from the user and returns a Recipe object."""

    # --- Name ---
    while True:
        name = input("Enter recipe name: ").strip()
        if not name:
            print("Name cannot be empty. Try again.")
        elif len(name) > 50:
            print("Name too long (max 50 characters). Try again.")
        elif not name.replace(" ", "").isalnum():
            print("Name must be alphanumeric (spaces allowed). Try again.")
        else:
            break

    # --- Cooking time ---
    while True:
        cooking_time = input("Enter cooking time (minutes): ").strip()
        if not cooking_time.isnumeric():
            print("Cooking time must be a number. Try again.")
        else:
            cooking_time = int(cooking_time)
            break

    # --- Ingredients ---
    while True:
        ingredients = input("Enter ingredients (comma-separated): ").strip()
        if not ingredients:
            print("Ingredients cannot be empty. Try again.")
        else:
            # Normalize formatting (e.g., "sugar,flour , butter")
            ingredients = ", ".join([i.strip() for i in ingredients.split(",")])
            break

    # Create recipe object
    recipe = Recipe(name=name, cooking_time=cooking_time, ingredients=ingredients)

    # Calculate difficulty
    recipe.calculate_difficulty()

    # Add and commit
    session.add(recipe)

    try:
        session.commit()
        print(f"Recipe added successfully!")
    except SQLAlchemyError as e:
        session.rollback()  # roll back so DB is not left in a bad state
        print("Database error:", e)

    except Exception as e:
        print("Unexpected error:", e)


def view_all_recipes(session):
    """
    Retrieve all recipes from the database and print them.
    If no recipes exist, inform the user and return.
    """
    # Retrieve all recipes
    recipes = session.query(Recipe).all()

    if not recipes:
        print("There are no entries in the database.")
        return None  # exit function and return to main menu

    # Loop through recipes and print each one using __str__
    for recipe in recipes:
        print(recipe)  # __str__ is called automatically


def search_by_ingredients(session):
    """
    Search for recipes based on ingredients chosen by the user.
    """

    # Check if table has any entries
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    # Retrieve only ingredients column
    results = session.query(Recipe.ingredients).all()  # returns list of tuples

    # Initialize all_ingredients list
    all_ingredients = []

    # Go through results and collect unique ingredients
    for (ingredient_str,) in results:  # unpack tuple
        if ingredient_str:  # skip empty strings
            temp_list = [i.strip() for i in ingredient_str.split(",")]
            for ing in temp_list:
                if ing not in all_ingredients:
                    all_ingredients.append(ing)

    # Display ingredients to the user
    print("Available ingredients:")
    for idx, ingredient in enumerate(all_ingredients, start=1):
        print(f"{idx}. {ingredient}")

    # Ask user for selection
    selected_input = input(
        "Enter the ingredient numbers to search for, separated by spaces: "
    ).strip()

    # Validate user input
    if not selected_input:
        print("Please enter valid number.")
        return None

    try:
        selected_numbers = [int(num) for num in selected_input.split()]
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None

    if any(num < 1 or num > len(all_ingredients) for num in selected_numbers):
        print("Input numbers are out of range.")
        return None

    # Map numbers to ingredient strings
    search_ingredients = [all_ingredients[num - 1] for num in selected_numbers]

    # Initialize conditions list
    conditions = []

    # Build like() conditions
    for ing in search_ingredients:
        like_term = f"%{ing}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Query database using OR for all selected ingredients
    recipes = session.query(Recipe).filter(or_(*conditions)).all()

    # Display results
    if recipes:
        print("\nRecipes matching your ingredients:\n")
        for r in recipes:
            print(r)
    else:
        print("No recipes match the selected ingredients.")


def edit_recipe(session):
    """
    Edit a recipe's name, ingredients, or cooking_time.
    Difficulty is automatically recalculated.
    """

    # Check if any recipes exist
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are no recipes in the database.")
        return None

    # Display available recipes (ID and name)
    print("Available recipes:")
    for r in recipes:
        print(f"ID: {r.id} - Name: {r.name}")

    # Ask user for ID to edit
    selected_id_input = input("Enter the ID of the recipe you want to edit: ").strip()
    if not selected_id_input.isnumeric():
        print("Invalid input. Please enter a number.")
        return None
    selected_id = int(selected_id_input)

    # Retrieve recipe object
    recipe_to_edit = session.query(Recipe).filter_by(id=selected_id).first()
    if not recipe_to_edit:
        print(f"No recipe found with ID {selected_id}.")
        return None

    # Display editable attributes
    print("\nCurrent recipe details:")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time (minutes): {recipe_to_edit.cooking_time}")

    # Ask user which attribute to edit
    choice = input("Enter the number of the attribute you want to edit: ").strip()
    if choice not in {"1", "2", "3"}:
        print("Invalid choice.")
        return None

    # Update selected attribute
    if choice == "1":
        new_name = input("Enter new recipe name: ").strip()
        if (
            not new_name
            or len(new_name) > 50
            or not new_name.replace(" ", "").isalnum()
        ):
            print("Invalid name. Must be under 50 characters and alphanumeric.")
            return None
        recipe_to_edit.name = new_name

    elif choice == "2":
        new_ingredients = input("Enter new ingredients (comma-separated): ").strip()
        if not new_ingredients:
            print("Ingredients cannot be empty.")
            return None
        # normalize formatting
        recipe_to_edit.ingredients = ", ".join(
            [i.strip() for i in new_ingredients.split(",")]
        )

    elif choice == "3":
        new_cooking_time = input("Enter new cooking time (minutes): ").strip()
        if not new_cooking_time.isnumeric():
            print("Cooking time must be a number.")
            return None
        recipe_to_edit.cooking_time = int(new_cooking_time)

    # Recalculate difficulty
    recipe_to_edit.calculate_difficulty()

    # Commit changes
    try:
        session.commit()
        print(f"Recipe '{recipe_to_edit.name}' updated successfully.")
    except Exception as e:
        session.rollback()
        print("An error occurred while updating the recipe:", e)


def delete_recipe(session):
    """
    Delete a recipe from the database based on user selection.
    """

    # Check if any recipes exist
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are no entries in the database.")
        return None  # exit function

    # List recipes with id and name
    print("Available recipes:")
    for recipe in recipes:
        print(f"ID: {recipe.id} - Name: {recipe.name}")

    # Ask user for id to delete
    selected_id_input = input("Enter the ID of the recipe you want to delete: ").strip()

    # Validate input
    if not selected_id_input.isnumeric():
        print("Invalid input. Please enter a number.")
        return None

    selected_id = int(selected_id_input)

    # Retrieve corresponding recipe object
    recipe_to_delete = session.query(Recipe).filter_by(id=selected_id).first()
    if not recipe_to_delete:
        print(f"No recipe found with ID {selected_id}.")
        return None

    # Confirm deletion
    confirm = (
        input(f"Are you sure you want to delete '{recipe_to_delete.name}'? (yes/no): ")
        .strip()
        .lower()
    )

    if confirm != "yes":
        print("Deletion cancelled.")
        return None

    # Delete and commit
    try:
        session.delete(recipe_to_delete)
        session.commit()
        print(f"Recipe '{recipe_to_delete.name}' has been deleted successfully.")
    except Exception as e:
        session.rollback()
        print("An error occurred while deleting the recipe:", e)


def main_menu(session):
    """Main menu loop."""
    while True:
        print("\nMain Menu:")
        print("1. Create a recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Update a recipe")
        print("5. Delete a recipe")
        print("6. Exit")

        choice = input("Enter an option (1-6): ").strip()

        if choice == "1":
            create_recipe(session)
        elif choice == "2":
            view_all_recipes(session)
        elif choice == "3":
            search_by_ingredients(session)
        elif choice == "4":
            edit_recipe(session)
        elif choice == "5":
            delete_recipe(session)
        elif choice == "6":
            print("Thanks for using the recipe app. Goodbye!")
            break
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":

    try:
        main_menu(session)
    except KeyboardInterrupt:
        print("\nExiting program.")

    finally:
        # Make sure session and engine are closed/disposed properly
        session.close()
        engine.dispose()
