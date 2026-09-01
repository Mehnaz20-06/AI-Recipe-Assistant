"""
Gemini-powered conversational recipe assistant.

Gemini handles the conversation and recipe generation.
Mem0/Qdrant memory is handled separately in memory_manager.py.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

SYSTEM_PROMPT = """
You are a friendly, intelligent AI cooking assistant.

Your job is to have natural conversations with the user and help them
with food, cooking, recipes, ingredients, and meal planning.

You are a conversational AI, not just a recipe generator.

IMPORTANT BEHAVIOR:
- Respond naturally to greetings, thanks, acknowledgements, questions,
  and casual conversation.
- Do NOT generate a recipe unless the user asks for a recipe, meal,
  dish, cooking idea, or something they can cook/eat.
- If the user simply shares information such as a health condition,
  allergy, dietary preference, or food preference, acknowledge it
  naturally.
- Do not say "I'll keep that in mind" for ordinary messages like
  "thank you", "okay", or "that's great".
- Use the user's known memories when answering relevant questions.
- When generating recipes, respect allergies, dietary restrictions,
  health constraints, and preferences.
- Never invent a user preference that is not present in the provided
  memories.
- Keep responses clear, friendly, and practical.

RECIPE FORMAT:
When the user asks for a recipe, provide:
1. Recipe title
2. Ingredients with quantities
3. Numbered cooking instructions
4. A short note explaining how the recipe fits the user's relevant
   preferences or constraints.

For normal conversation, respond naturally and concisely.
"""


def chat_with_gemini(user_message: str, known_facts: list[str]) -> str:
    """
    Send the user's message and relevant memories to Gemini.
    Gemini decides how to respond naturally.
    """

    if known_facts:
        facts_block = "\n".join(
            f"- {fact}" for fact in known_facts
        )
    else:
        facts_block = "No known user preferences or constraints."

    user_prompt = f"""
Known information about the user:
{facts_block}

Current user message:
"{user_message}"

Respond naturally to the user.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    return response.text
def should_remember(user_message: str) -> bool:
    """
    Ask Gemini whether the user's message contains
    a useful long-term preference or constraint.
    """

    prompt = f"""
Decide whether this user message contains information
that would be useful to remember for future conversations.

Remember things such as:
- allergies
- health/dietary restrictions
- food preferences
- disliked ingredients
- favorite foods
- cooking preferences

Do NOT remember:
- greetings
- thanks
- acknowledgements
- casual conversation
- temporary requests

Return ONLY:
YES
or
NO

User message:
"{user_message}"
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text.strip().upper() == "YES"