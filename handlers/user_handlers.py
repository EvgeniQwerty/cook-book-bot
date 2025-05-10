import logging
import aiohttp
import json
from typing import Dict, Any, Optional

from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CATEGORIES, AI_PROMPT_TEMPLATE, OPENROUTER_API_KEY, OPENROUTER_MODEL, MAX_MESSAGE_LENGTH
from database.db import add_recipe, get_recipes_by_category, get_recipe_by_id, update_recipe, delete_recipe
from keyboards.keyboards import (
    get_main_menu_keyboard, 
    get_cancel_keyboard, 
    get_categories_keyboard, 
    get_recipes_keyboard,
    get_confirmation_keyboard,
    get_recipe_details_keyboard,
    get_navigation_keyboard,
    get_done_keyboard
)
from translations import get_text

# Initialize router
router = Router()

# Define FSM states
class RecipeStates(StatesGroup):
    # View recipe states
    viewing_categories = State()
    viewing_recipes = State()
    viewing_recipe_details = State()
    
    # Add recipe states
    adding_category = State()
    adding_title = State()
    adding_ingredients = State()
    adding_instructions = State()
    adding_video_link = State()
    confirming_recipe = State()
    
    # Edit recipe states
    editing_category = State()
    editing_title = State()
    editing_ingredients = State()
    editing_instructions = State()
    editing_video_link = State()
    confirming_edit = State()
    confirming_delete = State()
    
    # AI assistant states
    asking_ai = State()

# Store temporary recipe data
recipe_data: Dict[int, Dict[str, Any]] = {}

# Store pagination data
pagination_data: Dict[int, Dict[str, Any]] = {}

# Main menu handlers
@router.message(F.text == get_text("view_recipe_button"))
async def view_recipe_start(message: Message, state: FSMContext):
    """Handle the 'View Recipe' button click."""
    await state.set_state(RecipeStates.viewing_categories)
    await message.answer(
        get_text("select_category"), 
        reply_markup=get_categories_keyboard()
    )

@router.message(F.text == get_text("add_recipe_button"))
async def add_recipe_start(message: Message, state: FSMContext):
    """Handle the 'Add Recipe' button click."""
    await state.set_state(RecipeStates.adding_category)
    await message.answer(
        get_text("select_category_for_new"), 
        reply_markup=get_categories_keyboard()
    )
    await message.answer(
        get_text("cancel_anytime"), 
        reply_markup=get_cancel_keyboard()
    )

@router.message(F.text == get_text("ask_ai_button"))
async def ask_ai_start(message: Message, state: FSMContext):
    """Handle the 'Ask AI' button click."""
    await state.set_state(RecipeStates.asking_ai)
    await message.answer(
        get_text("ask_ai_prompt"), 
        reply_markup=get_cancel_keyboard()
    )

# Cancel handler - works in any state
@router.message(F.text == get_text("cancel_button"))
async def cancel_handler(message: Message, state: FSMContext):
    """Handle the 'Cancel' button click in any state."""
    current_state = await state.get_state()
    if current_state is None:
        return
    
    # Clear state and return to main menu
    await state.clear()
    await message.answer(
        get_text("action_cancelled"), 
        reply_markup=get_main_menu_keyboard()
    )

# View recipe handlers
@router.callback_query(StateFilter(RecipeStates.viewing_categories), F.data.startswith("category:"))
async def process_category_selection_for_viewing(callback: CallbackQuery, state: FSMContext):
    """Process category selection when viewing recipes."""
    # Extract category from callback data
    # Check if callback.data exists before splitting
    category = callback.data.split(":")[1] if callback.data else None
    if not category:
        await callback.answer(get_text("invalid_category"))
        return
    
    # Get recipes for this category
    recipes = await get_recipes_by_category(category)
    
    if not recipes:
        if callback.message:
            await callback.message.edit_text(
                get_text("no_recipes_in_category", category=category),
                reply_markup=get_categories_keyboard()
            )
        else:
            await callback.answer(get_text("no_recipes_in_category", category=category))
        return
    
    # Store category and recipes in state data
    await state.update_data(category=category, recipes=recipes)
    
    # Set state to viewing recipes
    await state.set_state(RecipeStates.viewing_recipes)
    
    # Show recipes with pagination
    if callback.message:
        await callback.message.edit_text(
            get_text("recipes_in_category", category=category),
            reply_markup=get_recipes_keyboard(recipes, page=0)
        )
    else:
        await callback.answer(get_text("recipes_in_category", category=category))
    await callback.answer()

@router.callback_query(StateFilter(RecipeStates.viewing_recipes), F.data.startswith("page:"))
async def process_recipe_pagination(callback: CallbackQuery, state: FSMContext):
    """Handle pagination when viewing recipe list."""
    # Get page number from callback data
    page = int(callback.data.split(":")[1])
    
    # Get stored recipes from state
    data = await state.get_data()
    recipes = data.get("recipes", [])
    category = data.get("category", "")
    
    # Update message with new page
    if callback.message:
        await callback.message.edit_text(
            get_text("recipes_in_category", category=category),
            reply_markup=get_recipes_keyboard(recipes, page=page)
        )
    else:
        await callback.answer(get_text("page_number", page=page+1))
    await callback.answer()

@router.callback_query(StateFilter(RecipeStates.viewing_recipes), F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    """Handle 'Back to Categories' button click."""
    await state.set_state(RecipeStates.viewing_categories)
    if callback.message:
        await callback.message.edit_text(
            get_text("select_category"), 
            reply_markup=get_categories_keyboard()
        )
    else:
        await callback.answer(get_text("back_to_categories"))
    await callback.answer()

@router.callback_query(StateFilter(RecipeStates.viewing_recipes), F.data.startswith("recipe:"))
async def show_recipe_details(callback: CallbackQuery, state: FSMContext):
    """Show details for a selected recipe."""
    # Get recipe ID from callback data
    recipe_id = int(callback.data.split(":")[1])
    
    # Get recipe details from database
    recipe = await get_recipe_by_id(recipe_id)
    
    if not recipe:
        await callback.answer(get_text("recipe_not_found"))
        return
    
    # Format recipe details
    recipe_text = f"🍽️ {recipe['title']}\n\n"
    recipe_text += f"{get_text('ingredients_label')}\n{recipe['ingredients']}\n\n"
    recipe_text += f"{get_text('instructions_label')}\n{recipe['instructions']}"
    
    if recipe['video_link']:
        recipe_text += f"\n\n{get_text('video_label')} {recipe['video_link']}"
    
    # Store current recipe ID in state
    await state.update_data(current_recipe_id=recipe_id)
    await state.set_state(RecipeStates.viewing_recipe_details)
    
    # Use the recipe details keyboard with edit and delete buttons
    keyboard = get_recipe_details_keyboard(recipe_id)
    
    # Send recipe details
    if callback.message:
        await callback.message.edit_text(
            recipe_text,
            reply_markup=keyboard
        )
    else:
        await callback.answer(get_text("view_recipe"))
    await callback.answer()

@router.callback_query(StateFilter(RecipeStates.viewing_recipe_details), F.data == "back_to_recipe_list")
async def back_to_recipe_list(callback: CallbackQuery, state: FSMContext):
    """Handle 'Back to Recipe List' button click."""
    # Get stored data
    data = await state.get_data()
    recipes = data.get("recipes", [])
    category = data.get("category", "")
    
    # Go back to recipe list
    await state.set_state(RecipeStates.viewing_recipes)
    if callback.message:
        await callback.message.edit_text(
            get_text("recipes_in_category", category=category),
            reply_markup=get_recipes_keyboard(recipes, page=0)
        )
    else:
        await callback.answer(get_text("back_to_recipe_list", category=category))
    await callback.answer()

@router.callback_query(StateFilter(RecipeStates.viewing_recipe_details), F.data.startswith("edit:"))
async def start_recipe_edit(callback: CallbackQuery, state: FSMContext):
    """Handle 'Edit' button click for a recipe."""
    # Get recipe ID from callback data
    recipe_id = int(callback.data.split(":")[1])
    
    # Get recipe details from database
    recipe = await get_recipe_by_id(recipe_id)
    
    if not recipe:
        await callback.answer(get_text("recipe_not_found"))
        return
    
    # Store recipe data in state
    await state.update_data({
        "edit_recipe_id": recipe_id,
        "category": recipe["category"],
        "title": recipe["title"],
        "ingredients": recipe["ingredients"],
        "instructions": recipe["instructions"],
        "video_link": recipe["video_link"]
    })
    
    # Move directly to editing title state
    await state.set_state(RecipeStates.editing_title)
    
    # Show title editing with navigation buttons
    if callback.message:
        await callback.message.edit_text(
            get_text("edit_title", current=recipe["title"]),
            reply_markup=get_navigation_keyboard()
        )
        await callback.message.answer(
            get_text("cancel_edit_anytime")
        )
    else:
        await callback.answer(get_text("edit_recipe"))
    await callback.answer()

@router.callback_query(StateFilter(RecipeStates.viewing_recipe_details), F.data.startswith("delete:"))
async def confirm_recipe_delete(callback: CallbackQuery, state: FSMContext):
    """Handle 'Delete' button click for a recipe."""
    # Get recipe ID from callback data
    recipe_id = int(callback.data.split(":")[1])
    
    # Get recipe details from database
    recipe = await get_recipe_by_id(recipe_id)
    
    if not recipe:
        await callback.answer(get_text("recipe_not_found"))
        return
    
    # Store recipe ID in state
    await state.update_data({"delete_recipe_id": recipe_id})
    
    # Move to confirming delete state
    await state.set_state(RecipeStates.confirming_delete)
    
    # Ask for confirmation
    if callback.message:
        await callback.message.edit_text(
            get_text("confirm_delete", title=recipe["title"]),
            reply_markup=get_confirmation_keyboard()
        )
    else:
        await callback.answer(get_text("confirm_delete_short"))
    await callback.answer()

# Add recipe handlers
@router.callback_query(StateFilter(RecipeStates.adding_category), F.data.startswith("category:"))
async def process_category_selection_for_adding(callback: CallbackQuery, state: FSMContext):
    """Process category selection when adding a recipe."""
    # Extract category from callback data
    category = callback.data.split(":")[1]
    
    # Store category in state data
    await state.update_data(category=category)
    
    # Move to next state - adding title
    await state.set_state(RecipeStates.adding_title)
    
    await callback.message.answer(
        get_text("selected_category", category=category),
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()

@router.message(StateFilter(RecipeStates.adding_title))
async def process_recipe_title(message: Message, state: FSMContext):
    """Process recipe title input."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Store title in state data
    await state.update_data(title=message.text.strip())
    
    # Move to next state - adding ingredients
    await state.set_state(RecipeStates.adding_ingredients)
    
    await message.answer(
        get_text("enter_ingredients"),
        reply_markup=get_cancel_keyboard()
    )

@router.message(StateFilter(RecipeStates.adding_ingredients))
async def process_recipe_ingredients(message: Message, state: FSMContext):
    """Process recipe ingredients input."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Store ingredients in state data
    await state.update_data(ingredients=message.text.strip())
    
    # Move to next state - adding instructions
    await state.set_state(RecipeStates.adding_instructions)
    
    await message.answer(
        get_text("enter_instructions"),
        reply_markup=get_cancel_keyboard()
    )

@router.message(StateFilter(RecipeStates.adding_instructions))
async def process_recipe_instructions(message: Message, state: FSMContext):
    """Process recipe instructions input."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Store instructions in state data
    await state.update_data(instructions=message.text.strip())
    
    # Move to next state - adding video link (optional)
    await state.set_state(RecipeStates.adding_video_link)
    
    await message.answer(
        get_text("enter_video_link"),
        reply_markup=get_cancel_keyboard()
    )

@router.message(StateFilter(RecipeStates.adding_video_link))
async def process_recipe_video_link(message: Message, state: FSMContext):
    """Process recipe video link input."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Store video link in state data (or None if not provided)
    video_link = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(video_link=video_link)
    
    # Get all recipe data
    recipe_data = await state.get_data()
    
    # Format recipe preview
    preview_text = f"🍽️ {recipe_data['title']}\n\n"
    preview_text += f"{get_text('category_label')} {recipe_data['category']}\n\n"
    preview_text += f"{get_text('ingredients_label')}\n{recipe_data['ingredients']}\n\n"
    preview_text += f"{get_text('instructions_label')}\n{recipe_data['instructions']}"
    
    if recipe_data['video_link']:
        preview_text += f"\n\n{get_text('video_label')} {recipe_data['video_link']}"
    
    # Move to confirmation state
    await state.set_state(RecipeStates.confirming_recipe)
    
    await message.answer(
        get_text("check_recipe", preview=preview_text),
        reply_markup=get_confirmation_keyboard()
    )

@router.callback_query(StateFilter(RecipeStates.confirming_recipe), F.data.startswith("confirm:"))
async def confirm_recipe_addition(callback: CallbackQuery, state: FSMContext):
    """Handle recipe confirmation."""
    # Get confirmation choice
    choice = callback.data.split(":")[1]
    
    if choice == "yes":
        # Get recipe data
        recipe_data = await state.get_data()
        
        # Add recipe to database
        recipe_id = await add_recipe(
            category=recipe_data["category"],
            title=recipe_data["title"],
            ingredients=recipe_data["ingredients"],
            instructions=recipe_data["instructions"],
            video_link=recipe_data["video_link"]
        )
        
        if callback.message:
            await callback.message.edit_text(get_text("recipe_saved"))
            # Return to main menu
            await callback.message.answer(
                get_text("what_next"),
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await callback.answer(get_text("recipe_saved"))
        await callback.answer()
    else:  # choice == "no"
        if callback.message:
            await callback.message.edit_text(get_text("recipe_cancelled"))
            # Return to main menu
            await callback.message.answer(
                get_text("what_next"),
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await callback.answer(get_text("recipe_cancelled"))
        await callback.answer()
    
    # Clear state
    await state.clear()

# Edit recipe handlers
@router.callback_query(StateFilter(RecipeStates.editing_category), F.data.startswith("category:"))
async def process_category_selection_for_editing(callback: CallbackQuery, state: FSMContext):
    """Process category selection when editing a recipe."""
    # Extract category from callback data
    category = callback.data.split(":")[1]
    
    # Update category in state data
    await state.update_data(category=category)
    
    # Get current recipe data
    data = await state.get_data()
    title = data.get("title", "")
    
    # Move to next state - editing title
    await state.set_state(RecipeStates.editing_title)
    
    if callback.message:
        await callback.message.edit_text(
            get_text("edit_title", current=title),
            reply_markup=get_cancel_keyboard()
        )
    else:
        await callback.answer(get_text("edit_title_short"))
    await callback.answer()

@router.message(StateFilter(RecipeStates.editing_title))
async def process_recipe_title_edit(message: Message, state: FSMContext):
    """Process recipe title input when editing."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Update title in state data
    await state.update_data(title=message.text.strip())
    
    # Get current recipe data
    data = await state.get_data()
    ingredients = data.get("ingredients", "")
    
    # Move to next state - editing ingredients
    await state.set_state(RecipeStates.editing_ingredients)
    
    await message.answer(
        get_text("edit_ingredients", current=ingredients),
        reply_markup=get_navigation_keyboard()
    )

@router.message(StateFilter(RecipeStates.editing_ingredients))
async def process_recipe_ingredients_edit(message: Message, state: FSMContext):
    """Process recipe ingredients input when editing."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Update ingredients in state data
    await state.update_data(ingredients=message.text.strip())
    
    # Get current recipe data
    data = await state.get_data()
    instructions = data.get("instructions", "")
    
    # Move to next state - editing instructions
    await state.set_state(RecipeStates.editing_instructions)
    
    await message.answer(
        get_text("edit_instructions", current=instructions),
        reply_markup=get_done_keyboard()
    )

@router.message(StateFilter(RecipeStates.editing_instructions))
async def process_recipe_instructions_edit(message: Message, state: FSMContext):
    """Process recipe instructions input when editing."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Update instructions in state data
    await state.update_data(instructions=message.text.strip())
    
    # Get all recipe data
    recipe_data = await state.get_data()
    
    # Format recipe preview
    preview_text = f"🍽️ {recipe_data['title']}\n\n"
    preview_text += f"{get_text('category_label')} {recipe_data['category']}\n\n"
    preview_text += f"{get_text('ingredients_label')}\n{recipe_data['ingredients']}\n\n"
    preview_text += f"{get_text('instructions_label')}\n{recipe_data['instructions']}"
    
    if recipe_data['video_link']:
        preview_text += f"\n\n{get_text('video_label')} {recipe_data['video_link']}"
    
    # Move to confirmation state
    await state.set_state(RecipeStates.confirming_edit)
    
    await message.answer(
        get_text("check_recipe_edit", preview=preview_text),
        reply_markup=get_confirmation_keyboard()
    )

@router.message(StateFilter(RecipeStates.editing_video_link))
async def process_recipe_video_link_edit(message: Message, state: FSMContext):
    """Process recipe video link input when editing."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    # Update video link in state data (or None if not provided)
    video_link = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(video_link=video_link)
    
    # Get all recipe data
    recipe_data = await state.get_data()
    
    # Format recipe preview
    preview_text = f"🍽️ {recipe_data['title']}\n\n"
    preview_text += f"{get_text('category_label')} {recipe_data['category']}\n\n"
    preview_text += f"{get_text('ingredients_label')}\n{recipe_data['ingredients']}\n\n"
    preview_text += f"{get_text('instructions_label')}\n{recipe_data['instructions']}"
    
    if recipe_data['video_link']:
        preview_text += f"\n\n{get_text('video_label')} {recipe_data['video_link']}"
    
    # Move to confirmation state
    await state.set_state(RecipeStates.confirming_edit)
    
    await message.answer(
        get_text("check_recipe_edit", preview=preview_text),
        reply_markup=get_confirmation_keyboard()
    )

# Navigation button handlers
@router.callback_query(F.data.startswith("navigation:"))
async def handle_navigation_buttons(callback: CallbackQuery, state: FSMContext):
    """Handle navigation buttons (Next, Cancel, Done) in recipe editing flow."""
    action = callback.data.split(":")[1]
    current_state = await state.get_state()
    
    if action == "cancel":
        # Cancel editing and return to main menu
        await state.clear()
        if callback.message:
            await callback.message.edit_text(get_text("recipe_edit_cancelled"))
            await callback.message.answer(
                get_text("what_next"),
                reply_markup=get_main_menu_keyboard()
            )
        await callback.answer()
        return
    
    if action == "next":
        # Get current recipe data
        data = await state.get_data()
        
        if current_state == RecipeStates.editing_title:
            # Move to ingredients editing
            ingredients = data.get("ingredients", "")
            await state.set_state(RecipeStates.editing_ingredients)
            if callback.message:
                await callback.message.edit_text(
                    get_text("edit_ingredients", current=ingredients),
                    reply_markup=get_navigation_keyboard()
                )
        
        elif current_state == RecipeStates.editing_ingredients:
            # Move to instructions editing
            instructions = data.get("instructions", "")
            await state.set_state(RecipeStates.editing_instructions)
            if callback.message:
                await callback.message.edit_text(
                    get_text("edit_instructions", current=instructions),
                    reply_markup=get_done_keyboard()
                )
    
    if action == "done":
        # Format recipe preview
        data = await state.get_data()
        preview_text = f"🍽️ {data['title']}\n\n"
        preview_text += f"{get_text('category_label')} {data['category']}\n\n"
        preview_text += f"{get_text('ingredients_label')}\n{data['ingredients']}\n\n"
        preview_text += f"{get_text('instructions_label')}\n{data['instructions']}"
        
        if data.get('video_link'):
            preview_text += f"\n\n{get_text('video_label')} {data['video_link']}"
        
        # Move to confirmation state
        await state.set_state(RecipeStates.confirming_edit)
        
        if callback.message:
            await callback.message.edit_text(
                get_text("check_recipe_edit", preview=preview_text),
                reply_markup=get_confirmation_keyboard()
            )
    
    await callback.answer()

@router.callback_query(StateFilter(RecipeStates.confirming_edit), F.data.startswith("confirm:"))
async def confirm_recipe_edit(callback: CallbackQuery, state: FSMContext):
    """Handle recipe edit confirmation."""
    # Get confirmation choice
    choice = callback.data.split(":")[1]
    
    if choice == "yes":
        # Get recipe data
        recipe_data = await state.get_data()
        recipe_id = recipe_data.get("edit_recipe_id")
        
        # Update recipe in database
        success = await update_recipe(
            recipe_id=recipe_id,
            category=recipe_data["category"],
            title=recipe_data["title"],
            ingredients=recipe_data["ingredients"],
            instructions=recipe_data["instructions"],
            video_link=recipe_data["video_link"]
        )
        
        if success:
            if callback.message:
                await callback.message.edit_text(get_text("recipe_updated"))
                # Return to main menu
                await callback.message.answer(
                    get_text("what_next"),
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await callback.answer(get_text("recipe_updated"))
        else:
            if callback.message:
                await callback.message.edit_text(get_text("recipe_update_failed"))
                # Return to main menu
                await callback.message.answer(
                    get_text("what_next"),
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await callback.answer(get_text("recipe_update_failed"))
    else:  # choice == "no"
        if callback.message:
            await callback.message.edit_text(get_text("recipe_edit_cancelled"))
            # Return to main menu
            await callback.message.answer(
                get_text("what_next"),
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await callback.answer(get_text("recipe_edit_cancelled"))
    
    await callback.answer()
    # Clear state
    await state.clear()

@router.callback_query(StateFilter(RecipeStates.confirming_delete), F.data.startswith("confirm:"))
async def process_recipe_delete(callback: CallbackQuery, state: FSMContext):
    """Handle recipe delete confirmation."""
    # Get confirmation choice
    choice = callback.data.split(":")[1]
    
    if choice == "yes":
        # Get recipe ID from state
        data = await state.get_data()
        recipe_id = data.get("delete_recipe_id")
        
        # Delete recipe from database
        success = await delete_recipe(recipe_id)
        
        if success:
            if callback.message:
                await callback.message.edit_text(get_text("recipe_deleted"))
                # Return to main menu
                await callback.message.answer(
                    get_text("what_next"),
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await callback.answer(get_text("recipe_deleted"))
        else:
            if callback.message:
                await callback.message.edit_text(get_text("recipe_delete_failed"))
                # Return to main menu
                await callback.message.answer(
                    get_text("what_next"),
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await callback.answer(get_text("recipe_delete_failed"))
    else:  # choice == "no"
        # Get stored data to return to recipe details
        data = await state.get_data()
        recipe_id = data.get("delete_recipe_id")
        
        # Get recipe details from database
        recipe = await get_recipe_by_id(recipe_id)
        
        if recipe and callback.message:
            # Format recipe details
            recipe_text = f"🍽️ {recipe['title']}\n\n"
            recipe_text += f"{get_text('ingredients_label')}\n{recipe['ingredients']}\n\n"
            recipe_text += f"{get_text('instructions_label')}\n{recipe['instructions']}"
            
            if recipe['video_link']:
                recipe_text += f"\n\n{get_text('video_label')} {recipe['video_link']}"
            
            # Return to recipe details
            await state.set_state(RecipeStates.viewing_recipe_details)
            await callback.message.edit_text(
                recipe_text,
                reply_markup=get_recipe_details_keyboard(recipe_id)
            )
        else:
            # Return to main menu if recipe not found
            if callback.message:
                await callback.message.edit_text(get_text("recipe_delete_cancelled"))
                await callback.message.answer(
                    get_text("what_next"),
                    reply_markup=get_main_menu_keyboard()
                )
            else:
                await callback.answer(get_text("recipe_delete_cancelled"))
            await state.clear()
    
    await callback.answer()

# AI assistant handlers
@router.message(StateFilter(RecipeStates.asking_ai))
async def process_ai_query(message: Message, state: FSMContext):
    """Process user query to AI assistant."""
    if not message.text or message.text == get_text("cancel_button"):
        return
    
    user_query = message.text.strip()
    
    # Show typing indicator
    await message.answer(get_text("thinking"))
    
    try:
        # Format prompt with user query
        prompt = AI_PROMPT_TEMPLATE.format(user_query=user_query)
        
        # Call OpenRouter API
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logging.error(f"OpenRouter API error: {error_text}")
                    await message.answer(
                        get_text("ai_error"),
                        reply_markup=get_main_menu_keyboard()
                    )
                    await state.clear()
                    return
                
                result = await response.json()
                ai_response = result["choices"][0]["message"]["content"]
        
        # Truncate response if too long
        if len(ai_response) > MAX_MESSAGE_LENGTH:
            ai_response = ai_response[:MAX_MESSAGE_LENGTH] + get_text("response_truncated") 
        
        # Send AI response
        await message.answer(ai_response)
        
        # Return to main menu
        await message.answer(
            get_text("what_next"),
            reply_markup=get_main_menu_keyboard()
        )
        
        # Clear state
        await state.clear()
        
    except Exception as e:
        logging.error(f"Error in AI processing: {e}")
        await message.answer(
            get_text("processing_error"),
            reply_markup=get_main_menu_keyboard()
        )
        await state.clear()