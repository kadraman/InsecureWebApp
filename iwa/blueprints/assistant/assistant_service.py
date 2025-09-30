import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not found.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
        self.assistant_id = ""
        self.thread_id = ""

    def create_assistant(self, instructions, name="MyMedicalAssistant", model="gpt-3.5-turbo", tools=None):
        if not self.client:
            return None
        if not self.assistant_id:
            logger.debug("Creating new assistant")
            my_assistant = self.client.beta.assistants.create(
                instructions=instructions,
                name=name,
                model=model,
                tools=tools or [{"type": "file_search"}],
            )
            self.assistant_id = my_assistant.id
        else:
            logger.debug("Retrieving existing assistant with ID: %s", self.assistant_id)
            my_assistant = self.client.beta.assistants.retrieve(self.assistant_id)
        return my_assistant

    def create_thread(self):
        if not self.client:
            return None
        if not self.thread_id:
            logger.debug("Creating new thread")
            thread = self.client.beta.threads.create()
            self.thread_id = thread.id
        else:
            logger.debug("Retrieving existing thread with ID: %s", self.thread_id)
            thread = self.client.beta.threads.retrieve(self.thread_id)
        return thread

    def send_message(self, content, role="user"):
        if not self.client or not self.thread_id:
            return None
        message_params = {"thread_id": self.thread_id, "role": role, "content": content}
        return self.client.beta.threads.messages.create(**message_params)

    def run_assistant(self):
        if not self.client or not self.thread_id or not self.assistant_id:
            return None
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )
        import time
        while run.status != "completed":
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=run.id)
        return run

    def get_latest_message(self):
        if not self.client or not self.thread_id:
            return None
        response = self.client.beta.threads.messages.list(self.thread_id).data[0]
        for content in response.content:
            if content.type == "text":
                return content.text.value
        return None

    def get_all_messages(self):
        if not self.client or not self.thread_id:
            return None
        thread_messages = self.client.beta.threads.messages.list(self.thread_id, order="asc")
        messages = []
        for msg in thread_messages.data:
            # Extract text content from each message
            text_content = ""
            for content in msg.content:
                if content.type == "text":
                    text_content = content.text.value
                    break
            messages.append({
                "role": msg.role,
                "content": text_content
            })
        return messages
    
    def chat_completion(self, messages, model="gpt-3.5-turbo", timeout=10, max_tokens=1000):
        if not self.client:
            return None
        return self.client.chat.completions.create(
            model=model,
            timeout=timeout,
            max_tokens=max_tokens,
            messages=messages
        )