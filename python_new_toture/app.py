import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from prompts import PROMPT_TEMPLATES


load_dotenv()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_client():
    """Create the OpenAI client only when the user submits a request."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_openai_api_key_here":
        return None

    return OpenAI(api_key=api_key)


def build_prompt(mode, user_input):
    template = PROMPT_TEMPLATES[mode]
    return template.format(user_input=user_input.strip())


def tutor_response(mode, user_input):
    if not user_input or not user_input.strip():
        return "Please enter a Python concept, error message, quiz topic, or code sample first."

    client = get_client()
    if client is None:
        return (
            "OPENAI_API_KEY is missing. Add it to your local .env file, "
            "or add it as a Hugging Face Space secret named OPENAI_API_KEY."
        )

    prompt = build_prompt(mode, user_input)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Python Tutor Bot, a patient tutor for beginner Python learners. "
                        "Use clear explanations, small examples, and an encouraging tone."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as error:
        return f"Something went wrong while contacting OpenAI: {error}"


with gr.Blocks(title="Python Tutor Bot", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Python Tutor Bot
        Learn Python concepts, debug errors, practice with quizzes, and improve your code.
        """
    )

    with gr.Row():
        mode_dropdown = gr.Dropdown(
            choices=list(PROMPT_TEMPLATES.keys()),
            value="Explain Concept",
            label="Choose a mode",
        )

    user_input_box = gr.Textbox(
        label="Your question or code",
        placeholder="Example: Explain Python lists, or paste code with an error...",
        lines=10,
    )

    submit_button = gr.Button("Ask Python Tutor Bot", variant="primary")

    output_box = gr.Markdown(label="Tutor response")

    submit_button.click(
        fn=tutor_response,
        inputs=[mode_dropdown, user_input_box],
        outputs=output_box,
    )


if __name__ == "__main__":
    demo.launch()
