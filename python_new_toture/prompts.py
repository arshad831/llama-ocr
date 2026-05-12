PROMPT_TEMPLATES = {
    "Explain Concept": """
Explain this Python concept for a beginner:

{user_input}

Please include:
- A short explanation
- A simple code example
- A common mistake to avoid
""",
    "Debug Code": """
Help debug this Python code or error message:

{user_input}

Please include:
- What the error probably means
- The corrected code if possible
- A beginner-friendly explanation of the fix
""",
    "Quiz Me": """
Create a short beginner Python quiz about this topic:

{user_input}

Please include:
- 3 multiple-choice questions
- 1 small coding question
- The answers at the end
""",
    "Improve Code": """
Review and improve this Python code:

{user_input}

Please include:
- A cleaner version of the code
- What changed
- One beginner-friendly tip for writing better Python
""",
}
