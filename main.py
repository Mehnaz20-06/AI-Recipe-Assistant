"""
CLI entry point.
Run: python main.py

Commands:
    exit     -> quit
    /profile -> show stored user memories
"""

from memory_manager import (
    store_message,
    get_relevant_memories,
    get_all_memories,
)

from recipe_agent import chat_with_gemini


USER_ID = "mehnaz_demo_user"


def should_store_memory(text: str) -> bool:
    """
    Lightweight rule-based check.

    We intentionally do NOT call Gemini here because Mem0 already
    uses Gemini internally when storing memories. This avoids
    unnecessary API requests and helps prevent free-tier quota issues.
    """

    lowered = text.lower()

    memory_phrases = [
        "i have ",
        "i'm allergic",
        "i am allergic",
        "allergic to",
        "i don't like ",
        "i do not like ",
        "i dislike ",
        "i love ",
        "i like ",
        "i prefer ",
        "i hate ",
        "i avoid ",
        "i can't eat ",
        "i cannot eat ",
        "i am vegetarian",
        "i'm vegetarian",
        "i am vegan",
        "i'm vegan",
        "i follow a ",
        "my diet is ",
    ]

    return any(phrase in lowered for phrase in memory_phrases)


def main():
    print(
        "=== Recipe Assistant "
        "(type 'exit' to quit, '/profile' to see stored facts) ===\n"
    )

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Bye.")
            break

        if user_input.lower() == "/profile":
            facts = get_all_memories(USER_ID)

            print("\n--- Stored facts about you ---")

            if facts:
                for fact in facts:
                    print(f"- {fact}")
            else:
                print("(nothing stored yet)")

            print()
            continue

        # Retrieve relevant memories for the current message
        relevant_facts = get_relevant_memories(
            USER_ID,
            query=user_input
        )

        # Gemini handles the actual conversation
        response = chat_with_gemini(
            user_input,
            relevant_facts
        )

        print(f"\nAssistant:\n{response}\n")

        # Only save messages that look like useful long-term facts
        if should_store_memory(user_input):
            store_message(
                USER_ID,
                user_input
            )


if __name__ == "__main__":
    main()