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

from flask import render_template, request, jsonify, session
from openai import OpenAI

from iwa.blueprints.assistant import assistant_bp


logger = logging.getLogger(__name__)

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    logger.debug("OPENAI_API_KEY: %s", api_key)
    logger.debug("AI Assistant functionality is enabled.")
    client = OpenAI(api_key=api_key)
else:
    logger.debug("OpenAI API key not found. Assistant functionality is disabled.")

# Initialize the assistant and thread globally
assistant_id = ""
thread_id = ""

# Define a global chat history
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]


def create_assistant():
    global assistant_id
    if assistant_id == "":
        my_assistant = client.beta.assistants.create(
            instructions="""You are a helpful medical assistant. You can help with medical questions and provide 
                information on various health topics. If you are unsure about a question, please advise the user to 
                consult a healthcare professional. You can also help with scheduling appointments, providing information on medications,
                and answering general health inquiries. Always prioritize user safety and confidentiality.
            """,
            name="MyMedicalAssistant",
            model="gpt-3.5-turbo",
            tools=[{"type": "file_search"}],
        )
        assistant_id = my_assistant.id
    else:
        my_assistant = client.beta.assistants.retrieve(assistant_id)
        assistant_id = my_assistant.id

    return my_assistant


def create_thread():
    global thread_id
    if thread_id == "":
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)
        thread_id = thread.id

    return thread


@assistant_bp.route('/', methods=['GET', 'POST'])
def index():
    """assistant page."""
    if not api_key:
        session["assistant_enabled"] = False
        message = "The AI Assistant is not currently available. Please try again later!"
    else:
        session["assistant_enabled"] = True
        message = "The AI Assistant is ready to help you!"
    return render_template("assistant/index.html", message=message)

@assistant_bp.route('/chat', methods=['POST'])
def chat():
    content = request.json["message"]
    chat_history.append({"role": "user", "content": content})

    # Send the message to the assistant
    message_params = {"thread_id": thread_id, "role": "user", "content": content}

    thread_message = client.beta.threads.messages.create(**message_params)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    # Wait for the run to complete and get the response
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    response = client.beta.threads.messages.list(thread_id).data[0]

    text_content = None

    # Iterate through the content objects to find the first text content
    for content in response.content:
        if content.type == "text":
            text_content = content.text.value
            break  # Exit the loop once the first text content is found

    # Check if text content was found
    if text_content:
        chat_history.append({"role": "assistant", "content": text_content})
        return jsonify(success=True, message=text_content)
    else:
        # Handle the case where no text content is found
        return jsonify(success=False, message="No text content found")


@assistant_bp.route('/reset', methods=['POST'])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

    global thread_id
    thread_id = ""
    create_thread()
    return jsonify(success=True)

@assistant_bp.route("/get_ids", methods=["GET"])
def get_ids():
    return jsonify(assistant_id=assistant_id, thread_id=thread_id)

@assistant_bp.route("/get_messages", methods=["GET"])
def get_messages():
    if thread_id != "":
        thread_messages = client.beta.threads.messages.list(thread_id, order="asc")
        messages = [
            {
                "role": msg.role,
                "content": msg.content[0].text.value,
            }
            for msg in thread_messages.data
        ]
        return jsonify(success=True, messages=messages)
    else:
        return jsonify(success=False, message="No thread ID")

@assistant_bp.before_request
def before_request():
    if api_key:
        create_assistant()
        create_thread()

@assistant_bp.after_request
def after_request(response):
    return response