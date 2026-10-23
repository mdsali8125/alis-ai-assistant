
import os
import gradio as gr
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Please configure GEMINI_API_KEY.")

client = genai.Client(api_key=api_key)

def chatbot(message, history):
    prompt = (
        "You are Ali's AI Assistant, a helpful general AI chatbot. "
        "Always answer in clear, simple English.\n\n"
    )

    for chat in history:
        role = chat.get("role", "")
        content = chat.get("content", "")

        if isinstance(content, str):
            if role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"

    prompt += f"User: {message}\nAssistant:"

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text or "Sorry, I could not generate a response."

demo = gr.ChatInterface(
    fn=chatbot,
    title="Ali's AI Assistant",
    description="Ask me anything. I reply in English.",
    examples=[
        "Explain Artificial Intelligence",
        "Write a simple Python program",
        "Explain Newton's rings"
    ]
)

if __name__ == "__main__":
    demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
    )

