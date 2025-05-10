from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import List

from config import CATEGORIES
from translations import get_text

# Main menu keyboard
def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Return the main menu keyboard with three options."""
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text=get_text("view_recipe_button")),
        KeyboardButton(text=get_text("add_recipe_button")),
        KeyboardButton(text=get_text("ask_ai_button"))
    )
    builder.adjust(1)  # One button per row
    return builder.as_markup(resize_keyboard=True)

# Cancel button keyboard
def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Return a keyboard with just a cancel button."""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=get_text("cancel_button")))
    return builder.as_markup(resize_keyboard=True)

# Categories keyboard (inline)
def get_categories_keyboard() -> InlineKeyboardMarkup:
    """Return an inline keyboard with all recipe categories."""
    builder = InlineKeyboardBuilder()
    for category in CATEGORIES:
        builder.add(InlineKeyboardButton(text=category, callback_data=f"category:{category}"))
    builder.adjust(2)  # Two buttons per row
    return builder.as_markup()

# Recipe list keyboard with pagination
def get_recipes_keyboard(recipes: List[dict], page: int = 0, page_size: int = 10) -> InlineKeyboardMarkup:
    """Return an inline keyboard with recipe titles and pagination controls.
    
    Args:
        recipes: List of recipe dictionaries with 'id' and 'title' keys
        page: Current page number (0-indexed)
        page_size: Number of recipes per page
    """
    builder = InlineKeyboardBuilder()
    
    # Calculate pagination
    total_pages = (len(recipes) + page_size - 1) // page_size
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, len(recipes))
    
    # Add recipe buttons
    for recipe in recipes[start_idx:end_idx]:
        builder.add(InlineKeyboardButton(
            text=recipe['title'], 
            callback_data=f"recipe:{recipe['id']}"
        ))
    
    # Add pagination controls if needed
    if total_pages > 1:
        row = []
        if page > 0:
            row.append(InlineKeyboardButton(text=get_text("back_button"), callback_data=f"page:{page-1}"))
        if page < total_pages - 1:
            row.append(InlineKeyboardButton(text=get_text("next_button"), callback_data=f"page:{page+1}"))
        builder.row(*row)
    
    # Add back button
    builder.row(InlineKeyboardButton(text=get_text("back_to_categories_button"), callback_data="back_to_categories"))
    
    # Adjust layout - one recipe per row
    builder.adjust(1)
    return builder.as_markup()

# Confirmation keyboard
def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Return a confirmation keyboard with Yes/No buttons."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=get_text("yes_button"), callback_data="confirm:yes"),
        InlineKeyboardButton(text=get_text("no_button"), callback_data="confirm:no")
    )
    return builder.as_markup()

# Recipe details keyboard with edit and delete buttons
def get_recipe_details_keyboard(recipe_id: int) -> InlineKeyboardMarkup:
    """Return an inline keyboard for recipe details with edit and delete buttons.
    
    Args:
        recipe_id: The ID of the recipe
    """
    builder = InlineKeyboardBuilder()
    
    # Add edit and delete buttons
    builder.row(
        InlineKeyboardButton(text=get_text("edit_button"), callback_data=f"edit:{recipe_id}"),
        InlineKeyboardButton(text=get_text("delete_button"), callback_data=f"delete:{recipe_id}")
    )
    
    # Add back button
    builder.row(InlineKeyboardButton(text=get_text("back_to_recipe_list_button"), callback_data="back_to_recipe_list"))
    
    return builder.as_markup()

# Navigation keyboard with Next and Cancel buttons
def get_navigation_keyboard() -> InlineKeyboardMarkup:
    """Return an inline keyboard with Next and Cancel buttons for recipe editing."""
    builder = InlineKeyboardBuilder()
    
    # Add Next and Cancel buttons
    builder.row(
        InlineKeyboardButton(text=get_text("next_button"), callback_data="navigation:next"),
        InlineKeyboardButton(text=get_text("cancel_button"), callback_data="navigation:cancel")
    )
    
    return builder.as_markup()

# Done keyboard with Done and Cancel buttons
def get_done_keyboard() -> InlineKeyboardMarkup:
    """Return an inline keyboard with Done and Cancel buttons for recipe editing."""
    builder = InlineKeyboardBuilder()
    
    # Add Done and Cancel buttons
    builder.row(
        InlineKeyboardButton(text=get_text("yes_button"), callback_data="navigation:done"),
        InlineKeyboardButton(text=get_text("cancel_button"), callback_data="navigation:cancel")
    )
    
    return builder.as_markup()