import openai
import os
import json
from datetime import datetime

STORAGE_PATH = "./conversations/"


class Conversation:
    def __init__(self, bot_name):
        self.bot_name = bot_name
        self.user_name = None
        self.user_chars_count = 0
        self.bot_words_count = 0
        self.entries = []
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    def add_user_message(self, message):
        self.user_chars_count += len(message)
        self.entries.append({"role": "user", "message": message})

    def add_bot_message(self, message):
        self.bot_words_count += len(message.split())
        self.entries.append({"role": "bot", "message": message})

    def infer_subject(self):
        try:
            prompt = "Based on the following conversation, determine the main subject:\n"
            for entry in self.entries:
                prompt += f"{entry['role']}: {entry['message']}\n"
            prompt += "\nSubject:"

            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=50
            ).choices[0].text.strip()
            return response

        except Exception:
            return "UNKNOWN"

    def save(self, user_name):
        filename = f"conversation_{self.timestamp}.json"
        save_path = os.path.join(STORAGE_PATH, filename)

        # Check and create the conversations directory if not exists
        if not os.path.exists(STORAGE_PATH):
            os.makedirs(STORAGE_PATH)

        self.user_name = user_name
        subject = self.infer_subject()
        data = {
            "bot_name": self.bot_name,
            "timestamp": self.timestamp,  # Storing the timestamp here
            "user_name": user_name,
            "user_chars_count": self.user_chars_count,
            "bot_words_count": self.bot_words_count,
            "subject": subject,
            "conversation": self.entries
        }

        with open(save_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load(filename):
        load_path = os.path.join(STORAGE_PATH, filename)

        with open(load_path, 'r') as file:
            data = json.load(file)
            conversation = Conversation(data["bot_name"])
            conversation.timestamp = data["timestamp"]  # Loading the timestamp here
            conversation.user_chars_count = data["user_chars_count"]
            conversation.bot_words_count = data["bot_words_count"]
            conversation.entries = data["conversation"]
            if "user_name" in data:
                conversation.user_name = data["user_name"]
            return conversation
