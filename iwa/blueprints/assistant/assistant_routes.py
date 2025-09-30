"""
        InsecureWebApp - an insecure Python/Flask Web application

        Copyright (C) 2024-2025  Kevin A. Lee (kadraman)

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import os
import time

from flask import make_response, render_template, request, jsonify, session
import markdown
from iwa.blueprints.assistant import assistant_bp
from iwa.blueprints.assistant.assistant_service import AssistantService

logger = logging.getLogger(__name__)

# Initialize the AssistantService
api_key = os.getenv("OPENAI_API_KEY")
assistant_service = AssistantService(api_key=api_key) if api_key else None

user_name = os.getenv("USER_NAME", "administrator") # Storing user name in an environment variable

# Define a global chat history
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]


@assistant_bp.route('/health_assistant', methods=['GET', 'POST'])
def health_assistant():
    """assistant page."""
    if not assistant_service:
        session["assistant_enabled"] = False
        message = "The Health Assistant is not currently available. Please try again later!"
    else:
        session["assistant_enabled"] = True
        message = "The Health Assistant is ready to help you!"
    #return render_template("assistant/health_assistant.html", message=message)
    resp = make_response(render_template("assistant/health_assistant.html", message=message))
    # Store assistant_id and thread_id in cookies if available
    if assistant_service and assistant_service.assistant_id and assistant_service.thread_id:
        resp.set_cookie('assistant_id', assistant_service.assistant_id)
        resp.set_cookie('thread_id', assistant_service.thread_id)
    return resp

@assistant_bp.route('/chat', methods=['POST'])
def chat():
    content = request.json["message"]
    chat_history.append({"role": "user", "content": content})

    # Send the message to the assistant
    assistant_service.send_message(content, role="user")

    # Run the assistant
    assistant_service.run_assistant()

    # Get the latest message
    text_content = assistant_service.get_latest_message()

    # Check if text content was found
    if text_content:
        chat_history.append({"role": "assistant", "content": text_content})
        return jsonify(success=True, message=text_content)
    else:
        return jsonify(success=False, message="No text content found")

@assistant_bp.route('/reset', methods=['POST'])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    assistant_service.reset_thread()
    return jsonify(success=True)

@assistant_bp.route("/get_ids", methods=["GET"])
def get_ids():
    return jsonify(assistant_id=assistant_service.assistant_id, thread_id=assistant_service.thread_id)

@assistant_bp.route("/get_messages", methods=["GET"])
def get_messages():
    messages = assistant_service.get_all_messages()
    if messages is not None:
        return jsonify(success=True, messages=messages)
    else:
        return jsonify(success=False, message="No thread ID")

@assistant_bp.route('/symptom_checker', methods=['GET', 'POST'])
def symptom_checker(symptoms=None, additional_symptoms=None):
    if request.method == 'GET':
        if not assistant_service:
            session["checker_enabled"] = False
            message = "The Symptom Checker is not currently available. Please try again later!"
        else:
            session["checker_enabled"] = True
            message = "The Symptom Checker is ready to help you!"
        return render_template("assistant/symptom_checker.html", message=message)
    if request.method == 'POST':
        # Get symptoms from form data
        symptoms_list = request.form.getlist('symptoms')  # For checkboxes
        additional = request.form.get('additional-symptoms', '').strip()
        symptoms = ', '.join(symptoms_list)
        if additional:
            symptoms = symptoms + ', ' + additional if symptoms else additional

        if symptoms:
            logger.debug("Health Assistant: user provided symptoms: %s", symptoms)
            # Call OpenAI API to get medicine recommendation
            messages = [
                {"role": "system", "content": "I have " + symptoms},
                {"role": "user", "content": """You are a helpful medical assistant.
                    Recommend me a medicine to alleviate the symptoms provided. 
                    Please provide a stockist or shop where it can be purchased over the counter and an approximate price.
                 """}
            ]
            completion = assistant_service.chat_completion(messages)
            response = {
                "role": completion.choices[0].message.role,
                "content": markdown.markdown(completion.choices[0].message.content)
            }
            return render_template("assistant/symptom_checker.html", message="Response received.", response=response)
    return render_template("assistant/symptom_checker.html")

@assistant_bp.before_request
def before_request():
    if assistant_service:
         # Try to retrieve IDs from cookies
        assistant_id = request.cookies.get('assistant_id')
        thread_id = request.cookies.get('thread_id')
        if assistant_id:
            assistant_service.assistant_id = assistant_id
        if thread_id:
            assistant_service.thread_id = thread_id
        instructions="""You are a helpful medical assistant. You can help with medical questions and provide 
                information on various health topics.Please ask questions about symptoms, existing health and medical 
                conditions in order to be able to provide better advice. If you are unsure about a question, 
                please advise the user to consult a healthcare professional. You can also help with scheduling 
                appointments, providing information on medications, and answering general health inquiries. 
                Always prioritize user safety and confidentiality.
            """
        assistant_service.create_assistant(instructions=instructions)
        assistant_service.create_thread()

@assistant_bp.after_request
def after_request(response):
    return response