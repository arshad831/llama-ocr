import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from prompts import FOLLOW_UP_INSTRUCTION, MODE_INSTRUCTIONS, QUIZ_INSTRUCTIONS


load_dotenv()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "450"))

SYSTEM_MESSAGE = """
You are Python Tutor Bot, a professional and patient Python tutor for beginners.
Teach through a clear learning journey:
1. Understand what the learner wants.
2. Explain or review in small steps.
3. Ask one useful follow-up question.
4. Keep answers practical, short, and encouraging.

Use simple language, small Python examples, and avoid overwhelming the learner.
"""


def get_client():
    """Create the OpenAI client only when the user submits a request."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_openai_api_key_here":
        return None

    return OpenAI(api_key=api_key)


def chat_with_openai(messages):
    client = get_client()
    if client is None:
        return (
            "OPENAI_API_KEY is missing. Add it to your local .env file, "
            "or add it as a Hugging Face Space secret named OPENAI_API_KEY."
        )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3,
            max_tokens=MAX_OUTPUT_TOKENS,
        )
        return response.choices[0].message.content
    except Exception as error:
        return f"Something went wrong while contacting OpenAI: {error}"


def start_state():
    return {
        "quiz_active": False,
        "quiz_topic": "",
        "quiz_number": 0,
        "quiz_notes": [],
    }


def build_messages(mode, user_input, message_history):
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

    for chat_message in message_history[-6:]:
        messages.append(
            {
                "role": chat_message["role"],
                "content": chat_message["content"],
            }
        )

    prompt = MODE_INSTRUCTIONS[mode].format(user_input=user_input.strip())
    prompt = f"{prompt}\n\n{FOLLOW_UP_INSTRUCTION}"
    messages.append({"role": "user", "content": prompt})
    return messages


def build_quiz_messages(user_input, state, message_history):
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

    for chat_message in message_history[-8:]:
        messages.append(
            {
                "role": chat_message["role"],
                "content": chat_message["content"],
            }
        )

    quiz_prompt = QUIZ_INSTRUCTIONS.format(
        topic=state["quiz_topic"],
        quiz_number=state["quiz_number"],
        user_answer=user_input.strip(),
        quiz_notes="\n".join(state["quiz_notes"]) or "No previous quiz notes yet.",
    )
    messages.append({"role": "user", "content": quiz_prompt})
    return messages


def tutor_response(mode, user_input, chat_history, message_history, state):
    chat_history = chat_history or []
    message_history = message_history or []
    state = state or start_state()

    if not user_input or not user_input.strip():
        warning = "Please type a Python topic, code sample, error message, or quiz answer first."
        chat_history.append({"role": "assistant", "content": warning})
        return chat_history, message_history, state, ""

    clean_input = user_input.strip()
    chat_history.append({"role": "user", "content": clean_input})
    message_history.append({"role": "user", "content": clean_input})

    if mode == "Quiz Me":
        current_quiz_number = None

        if not state["quiz_active"]:
            state = start_state()
            state["quiz_active"] = True
            state["quiz_topic"] = clean_input
            state["quiz_number"] = 1
            intro_prompt = (
                f"Start a beginner Python quiz journey about: {state['quiz_topic']}.\n"
                "Ask exactly one multiple-choice question. Do not give the answer yet. "
                "After the options, ask the learner to reply with A, B, C, or D."
            )
            messages = [{"role": "system", "content": SYSTEM_MESSAGE}, {"role": "user", "content": intro_prompt}]
        else:
            current_quiz_number = state["quiz_number"]
            state["quiz_notes"].append(f"Question {state['quiz_number']} answer: {clean_input}")
            messages = build_quiz_messages(clean_input, state, message_history)

        reply = chat_with_openai(messages)

        if state["quiz_active"] and "Something went wrong" not in reply:
            if current_quiz_number and current_quiz_number >= 3:
                state = start_state()
            elif current_quiz_number:
                state["quiz_number"] = current_quiz_number + 1
    else:
        state = start_state()
        messages = build_messages(mode, clean_input, message_history)
        reply = chat_with_openai(messages)

    message_history.append({"role": "assistant", "content": reply})
    chat_history.append({"role": "assistant", "content": reply})
    return chat_history, message_history, state, ""


def clear_chat():
    return [], [], start_state(), ""


with gr.Blocks(title="Python Tutor Bot") as demo:
    gr.Markdown(
        """
        # Python Tutor Bot
        Learn Python step by step with explanations, debugging help, quizzes, and code reviews.
        """
    )

    app_state = gr.State(start_state())
    message_history = gr.State([])

    with gr.Row():
        mode_dropdown = gr.Dropdown(
            choices=list(MODE_INSTRUCTIONS.keys()),
            value="Explain Concept",
            label="Learning mode",
        )

    chatbot = gr.Chatbot(
        label="Python Tutor Bot",
        height=430,
    )

    user_input_box = gr.Textbox(
        label="Message",
        placeholder="Example: I want to learn Python lists, or paste code with an error...",
        lines=5,
    )

    with gr.Row():
        submit_button = gr.Button("Send", variant="primary")
        clear_button = gr.Button("Clear")

    submit_button.click(
        fn=tutor_response,
        inputs=[mode_dropdown, user_input_box, chatbot, message_history, app_state],
        outputs=[chatbot, message_history, app_state, user_input_box],
    )

    user_input_box.submit(
        fn=tutor_response,
        inputs=[mode_dropdown, user_input_box, chatbot, message_history, app_state],
        outputs=[chatbot, message_history, app_state, user_input_box],
    )

    clear_button.click(
        fn=clear_chat,
        inputs=None,
        outputs=[chatbot, message_history, app_state, user_input_box],
    )


if __name__ == "__main__":
    demo.launch()
