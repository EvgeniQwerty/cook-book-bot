from typing import Dict, Any
from config import LANGUAGE

# Define translations for all UI text
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Main menu buttons
    "view_recipe_button": {
        "en": "📖 View Recipe",
        "ru": "📖 Посмотреть рецепт"
    },
    "add_recipe_button": {
        "en": "➕ Add Recipe",
        "ru": "➕ Добавить рецепт"
    },
    "ask_ai_button": {
        "en": "🤖 Ask AI",
        "ru": "🤖 Спросить ИИ"
    },
    "cancel_button": {
        "en": "❌ Cancel",
        "ru": "❌ Отмена"
    },
    
    # Navigation buttons
    "back_button": {
        "en": "⬅️ Back",
        "ru": "⬅️ Назад"
    },
    "next_button": {
        "en": "➡️ Next",
        "ru": "➡️ Вперед"
    },
    "back_to_categories_button": {
        "en": "🔙 Back to Categories",
        "ru": "🔙 К категориям"
    },
    "back_to_list_button": {
        "en": "🔙 Back to List",
        "ru": "🔙 Назад к списку"
    },
    "edit_button": {
        "en": "✏️ Edit",
        "ru": "✏️ Редактировать"
    },
    "delete_button": {
        "en": "🗑️ Delete",
        "ru": "🗑️ Удалить"
    },
    "back_to_recipe_list_button": {
        "en": "🔙 Back to Recipe List",
        "ru": "🔙 Назад к списку рецептов"
    },
    
    # Confirmation buttons
    "yes_button": {
        "en": "✅ Yes",
        "ru": "✅ Да"
    },
    "no_button": {
        "en": "❌ No",
        "ru": "❌ Нет"
    },
    
    # Messages
    "select_category": {
        "en": "Select a recipe category:",
        "ru": "Выберите категорию рецептов:"
    },
    "select_category_for_new": {
        "en": "Select a category for the new recipe:",
        "ru": "Выберите категорию для нового рецепта:"
    },
    "select_category_for_edit": {
        "en": "Select a category for the recipe:",
        "ru": "Выберите категорию для рецепта:"
    },
    "cancel_anytime": {
        "en": "You can cancel adding a recipe at any time.",
        "ru": "Вы можете отменить добавление рецепта в любой момент."
    },
    "cancel_edit_anytime": {
        "en": "You can cancel editing a recipe at any time.",
        "ru": "Вы можете отменить редактирование рецепта в любой момент."
    },
    "ask_ai_prompt": {
        "en": "Ask a question about cooking or describe ingredients you have, and I'll suggest what you can cook.",
        "ru": "Задайте вопрос о кулинарии или опишите ингредиенты, которые у вас есть, и я подскажу, что можно приготовить."
    },
    "action_cancelled": {
        "en": "Action cancelled. What would you like to do?",
        "ru": "Действие отменено. Что бы вы хотели сделать?"
    },
    "invalid_category": {
        "en": "Invalid category selection",
        "ru": "Неверный выбор категории"
    },
    "no_recipes_in_category": {
        "en": "There are no recipes in the '{category}' category yet.",
        "ru": "В категории '{category}' пока нет рецептов."
    },
    "recipes_in_category": {
        "en": "Recipes in '{category}' category:",
        "ru": "Рецепты в категории '{category}':"
    },
    "page_number": {
        "en": "Page {page}",
        "ru": "Страница {page}"
    },
    "back_to_categories": {
        "en": "Back to categories",
        "ru": "Возврат к категориям"
    },
    "recipe_not_found": {
        "en": "Recipe not found.",
        "ru": "Рецепт не найден."
    },
    "view_recipe": {
        "en": "View recipe",
        "ru": "Просмотр рецепта"
    },
    "back_to_recipe_list": {
        "en": "Back to recipe list for '{category}'",
        "ru": "Возврат к списку рецептов категории '{category}'"
    },
    "selected_category": {
        "en": "Selected category: {category}\n\nEnter recipe title:",
        "ru": "Выбрана категория: {category}\n\nВведите название рецепта:"
    },
    "enter_ingredients": {
        "en": "Enter ingredients (each on a new line):",
        "ru": "Введите ингредиенты (каждый с новой строки):"
    },
    "enter_instructions": {
        "en": "Enter cooking instructions:",
        "ru": "Введите способ приготовления:"
    },
    "enter_video_link": {
        "en": "Enter video link (optional):\n\nIf there is no link, just send '-'.",
        "ru": "Введите ссылку на видео (необязательно):\n\nЕсли ссылки нет, просто отправьте '-'."
    },
    "check_recipe": {
        "en": "Check the recipe before saving:\n\n{preview}\n\nSave the recipe?",
        "ru": "Проверьте рецепт перед сохранением:\n\n{preview}\n\nСохранить рецепт?"
    },
    "recipe_saved": {
        "en": "✅ Recipe successfully saved!",
        "ru": "✅ Рецепт успешно сохранен!"
    },
    "recipe_cancelled": {
        "en": "❌ Recipe addition cancelled.",
        "ru": "❌ Добавление рецепта отменено."
    },
    "what_next": {
        "en": "What would you like to do next?",
        "ru": "Что бы вы хотели сделать дальше?"
    },
    "edit_title": {
        "en": "Edit recipe title:\n\nCurrent: {current}",
        "ru": "Редактировать название рецепта:\n\nТекущее: {current}"
    },
    "edit_title_short": {
        "en": "Edit title",
        "ru": "Редактировать название"
    },
    "edit_ingredients": {
        "en": "Edit ingredients (each on a new line):\n\nCurrent:\n{current}",
        "ru": "Редактировать ингредиенты (каждый с новой строки):\n\nТекущие:\n{current}"
    },
    "edit_instructions": {
        "en": "Edit cooking instructions:\n\nCurrent:\n{current}",
        "ru": "Редактировать способ приготовления:\n\nТекущий:\n{current}"
    },
    "edit_video_link": {
        "en": "Edit video link (optional):\n\nCurrent: {current}\n\nIf there is no link, just send '-'.",
        "ru": "Редактировать ссылку на видео (необязательно):\n\nТекущая: {current}\n\nЕсли ссылки нет, просто отправьте '-'."
    },
    "check_recipe_edit": {
        "en": "Check the edited recipe before saving:\n\n{preview}\n\nSave the changes?",
        "ru": "Проверьте отредактированный рецепт перед сохранением:\n\n{preview}\n\nСохранить изменения?"
    },
    "recipe_updated": {
        "en": "✅ Recipe successfully updated!",
        "ru": "✅ Рецепт успешно обновлен!"
    },
    "recipe_update_failed": {
        "en": "❌ Failed to update recipe.",
        "ru": "❌ Не удалось обновить рецепт."
    },
    "recipe_edit_cancelled": {
        "en": "❌ Recipe editing cancelled.",
        "ru": "❌ Редактирование рецепта отменено."
    },
    "confirm_delete": {
        "en": "Are you sure you want to delete the recipe '{title}'?",
        "ru": "Вы уверены, что хотите удалить рецепт '{title}'?"
    },
    "confirm_delete_short": {
        "en": "Confirm deletion",
        "ru": "Подтвердите удаление"
    },
    "recipe_deleted": {
        "en": "✅ Recipe successfully deleted!",
        "ru": "✅ Рецепт успешно удален!"
    },
    "recipe_delete_failed": {
        "en": "❌ Failed to delete recipe.",
        "ru": "❌ Не удалось удалить рецепт."
    },
    "recipe_delete_cancelled": {
        "en": "❌ Recipe deletion cancelled.",
        "ru": "❌ Удаление рецепта отменено."
    },
    "edit_recipe": {
        "en": "Edit recipe",
        "ru": "Редактировать рецепт"
    },
    "thinking": {
        "en": "🤖 Thinking about the answer...",
        "ru": "🤖 Думаю над ответом..."
    },
    "ai_error": {
        "en": "Sorry, there was an error when contacting the AI. Please try again later.",
        "ru": "Извините, произошла ошибка при обращении к ИИ. Попробуйте позже."
    },
    "response_truncated": {
        "en": "\n\n[The response was shortened due to message length limitations]",
        "ru": "\n\n[Ответ был сокращен из-за ограничений длины сообщения]"
    },
    "processing_error": {
        "en": "Sorry, there was an error processing your request. Please try again later.",
        "ru": "Извините, произошла ошибка при обработке запроса. Попробуйте позже."
    },
    # Recipe details
    "ingredients_label": {
        "en": "🧂 Ingredients:",
        "ru": "🧂 Ингредиенты:"
    },
    "instructions_label": {
        "en": "🔥 Cooking method:",
        "ru": "🔥 Способ приготовления:"
    },
    "video_label": {
        "en": "🎥 Video:",
        "ru": "🎥 Видео:"
    },
    "category_label": {
        "en": "📂 Category:",
        "ru": "📂 Категория:"
    },
    # Start message
    "welcome_message": {
        "en": "Hello, {name}!\n\nWelcome to Cooking Recipe Bot! 🍳\nHere you can view, add recipes and ask AI about cooking food",
        "ru": "Привет, {name}!\n\nДобро пожаловать в Cooking Recipe Bot! 🍳\nЗдесь ты можешь смотреть, добавлять рецепты и спрашивать ИИ про готовку еды"
    },
    "choose_menu_item": {
        "en": "Choose a menu item:",
        "ru": "Выбери пункт меню:"
    }
}

# Helper function to get translation
def get_text(key: str, **kwargs) -> str:
    """Get translated text for the given key and format with kwargs if needed."""
    if key not in TRANSLATIONS:
        return f"Missing translation: {key}"
    
    text = TRANSLATIONS[key].get(LANGUAGE, TRANSLATIONS[key].get("en", f"Missing translation: {key}"))
    
    # Format the text with kwargs if provided
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError as e:
            return f"Error formatting translation: {e}"
    
    return text