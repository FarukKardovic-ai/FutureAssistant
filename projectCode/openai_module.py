import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text_basic(prompt: str, model: str = "gpt-3.5-turbo", system_prompt: str = "You are helpful"):
    """
    Generates text using OpenAI's GPT model.

    :param prompt: The user prompt to send to the model.
    :param model: The model to use for generating text (default is 'gpt-3.5-turbo').
    :param system_prompt: The system prompt to guide the behavior of the model.
    :return: The generated response from the model as a string.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"
    

def generate_text_with_conversation(messages,model = "gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
        )
    return response.choices[0].message.content