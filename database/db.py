import aiosqlite
import logging
from typing import List, Dict, Optional, Any

from config import DATABASE_NAME

async def init_db():
    """Initialize the database and create tables if they don't exist."""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            video_link TEXT
        )
        """)
        await db.commit()
    logging.info("Database initialized")

async def add_recipe(category: str, title: str, ingredients: str, instructions: str, video_link: Optional[str] = None) -> int:
    """Add a new recipe to the database.
    
    Args:
        category: Recipe category
        title: Recipe title
        ingredients: Recipe ingredients
        instructions: Cooking instructions
        video_link: Optional link to a video
        
    Returns:
        The ID of the newly created recipe
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute(
            "INSERT INTO recipes (category, title, ingredients, instructions, video_link) VALUES (?, ?, ?, ?, ?)",
            (category, title, ingredients, instructions, video_link)
        )
        await db.commit()
        return cursor.lastrowid

async def get_recipes_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all recipes for a specific category.
    
    Args:
        category: The category to filter by
        
    Returns:
        A list of recipe dictionaries
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, title FROM recipes WHERE category = ? ORDER BY title",
            (category,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_recipe_by_id(recipe_id: int) -> Optional[Dict[str, Any]]:
    """Get a recipe by its ID.
    
    Args:
        recipe_id: The ID of the recipe to retrieve
        
    Returns:
        A dictionary with recipe details or None if not found
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def update_recipe(recipe_id: int, category: str, title: str, ingredients: str, instructions: str, video_link: Optional[str] = None) -> bool:
    """Update an existing recipe in the database.
    
    Args:
        recipe_id: The ID of the recipe to update
        category: Updated recipe category
        title: Updated recipe title
        ingredients: Updated recipe ingredients
        instructions: Updated cooking instructions
        video_link: Updated link to a video
        
    Returns:
        True if the recipe was updated successfully, False otherwise
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute(
            """UPDATE recipes 
               SET category = ?, title = ?, ingredients = ?, instructions = ?, video_link = ? 
               WHERE id = ?""",
            (category, title, ingredients, instructions, video_link, recipe_id)
        )
        await db.commit()
        return cursor.rowcount > 0

async def delete_recipe(recipe_id: int) -> bool:
    """Delete a recipe from the database.
    
    Args:
        recipe_id: The ID of the recipe to delete
        
    Returns:
        True if the recipe was deleted successfully, False otherwise
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute(
            "DELETE FROM recipes WHERE id = ?",
            (recipe_id,)
        )
        await db.commit()
        return cursor.rowcount > 0