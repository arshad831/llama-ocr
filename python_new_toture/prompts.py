MODE_INSTRUCTIONS = {
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


FOLLOW_UP_INSTRUCTION = """
End by asking exactly one short follow-up question that helps the learner continue.
Do not ask multiple questions at once.
"""


QUIZ_INSTRUCTIONS = """
You are running a beginner Python quiz on this topic:

{topic}

The learner answered the previous question with:

{user_answer}

Previous quiz notes:

{quiz_notes}

This is quiz step {quiz_number}.

Please:
- Say whether the learner's answer is correct.
- Explain the answer in 2-4 short sentences.
- If this was question 3, finish with a short score-style summary and recommend the next topic.
- If this was question 1 or 2, ask exactly one new multiple-choice question with A, B, C, and D options.
- Do not reveal the new answer until the learner replies.
"""
