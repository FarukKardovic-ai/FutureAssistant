import os
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import openai
from openai_module import generate_text_with_conversation
from prompts import react_system_prompt
from sample_functions import get_weather, get_news, calculate,calculate_bmi
from json_helpers import extract_json
import logging
from functools import lru_cache
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_wtf.csrf import CSRFProtect

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

available_actions = {
    "get_weather": get_weather,
    "get_news": get_news,
    "calculate": calculate,
    "calculate_bmi":calculate_bmi
}

@lru_cache(maxsize=128)
def cached_answer_question(question):
    return answer_question(question)

import re

def answer_question(question):
    
    messages = [
        {"role": "system", "content": react_system_prompt},
        {"role": "user", "content": question},
    ]
    turn_count = 1
    max_turns = 5

    while turn_count < max_turns:
        turn_count += 1
        response = generate_text_with_conversation(messages, model="gpt-4")
        json_function = extract_json(response)

        if json_function:
            function_name = json_function[0]['function_name']
            function_parms = json_function[0]['function_parms']
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_parms}")
            action_function = available_actions[function_name]
            result = action_function(**function_parms)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
        else:
            break

    return response 

class QuestionForm(FlaskForm):
    question = StringField('Your Question', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = QuestionForm()  
    answer = ''
    if form.validate_on_submit():  
        question = form.question.data
        try:
            answer = cached_answer_question(question)
        except Exception as e:
            logging.error(f"Error answering question: {e}")
            answer = "Sorry, I couldn't process your request. Please try again later."
    return render_template('index.html', form=form, answer=answer)  

if __name__ == '__main__':
    app.run(debug=True)
