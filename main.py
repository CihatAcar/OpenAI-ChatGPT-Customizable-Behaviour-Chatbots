import openai
from utilities import Conversation
import os
from collections import deque
import yaml
from decouple import config

STORAGE_PATH = "./conversations/"


class Chatbot:
    def __init__(self, bot_name, engine, previous_conversation=None):
        self.bot_name = bot_name
        self.engine = engine
        self.conversation = Conversation(bot_name)
        self.context = deque(maxlen=10)  # Storing the last 10 conversation lines
        self.user_name = None

        # Load previous context if a previous conversation is passed.
        if previous_conversation:
            for entry in previous_conversation.entries:
                self.context.append(f"{entry['role']}: {entry['message']}")

    def create_prompt(self, message):
        return "\n".join(self.context) + "\n" + self.get_prompt(message)

    def get_prompt(self, message):
        raise NotImplementedError("Subclasses must implement this method.")

    def generate_response(self, message):
        # Update context with the user's message.
        self.context.append(f"user: {message}")

        # Generate the prompt for OpenAI using the entire context.
        prompt = self.create_prompt(message)

        try:
            response = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            ).choices[0].text.strip()

            self.context.append(f"bot: {response}")

            return response

        except Exception as e:
            return f"Sorry, I encountered an error: {e}"

    def start_chat(self):
        if not self.user_name:  # Only ask for the user name if it's not already known
            self.user_name = input("Hello! Before we begin, may I know your name? ")
        else:
            print(f"Welcome back, {self.user_name}!")

        greeting = f"Hello, {self.user_name}! I am {self.bot_name}. How can I help you?"
        print(greeting)
        print("(Type 'EXIT' anytime to end the chat)")

        while True:
            user_message = input(f"{self.user_name}: ")
            if len(user_message) > 1000:
                print("That's a long input! Please keep your messages shorter.")
                continue

            # Update to handle "EXIT"
            if user_message.upper() == "EXIT":
                print(f"{self.bot_name}: See you next time, {self.user_name}!")
                self.conversation.save(self.user_name)
                break

            self.conversation.add_user_message(
                user_message)

            response = self.generate_response(user_message)
            self.conversation.add_bot_message(response)

            print(f"{self.bot_name}: {response}")


class Henry(Chatbot):
    def __init__(self, bot_name, engine, behavior, previous_conversation=None):
        super().__init__(bot_name, engine, previous_conversation=previous_conversation)
        self.behavior = behavior

    def get_prompt(self, message):
        return self.behavior["prompt_style"].format(message=message)

    def start_chat(self):
        print(self.behavior["start_message"].format(name=self.bot_name))
        super().start_chat()


class Vera(Chatbot):
    def __init__(self, bot_name, engine, behavior, previous_conversation=None):
        super().__init__(bot_name, engine, previous_conversation=previous_conversation)
        self.behavior = behavior

    def get_prompt(self, message):
        return self.behavior["prompt_style"].format(message=message)

    def start_chat(self):
        print(self.behavior["start_message"].format(name=self.bot_name))
        super().start_chat()


class ChatbotManager:
    @staticmethod
    def load_chatbots_config():
        with open("chatbots_config.yaml", 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def list_conversations():
        return [f for f in os.listdir(STORAGE_PATH) if f.endswith('.json')]

    @staticmethod
    def start_or_continue_conversation():
        try:
            action = int(input("What do you want to do?\n[0] continue a conversation\n[1] start a new conversation\n"))
            if action not in [0, 1]:
                raise ValueError("Invalid choice.")

            if action == 0:
                print("Available conversations:")
                conversations = ChatbotManager.list_conversations()
                if not conversations:
                    return print("No conversations available.")

                for idx, file in enumerate(conversations):
                    print(f"[{idx}] {file}")

                choice_idx = int(input("Enter the index of conversation you want to continue: "))

                if choice_idx < 0 or choice_idx >= len(conversations):
                    print(f"Please choose a valid index between 0 and {len(conversations) - 1}.")
                    return

                selected_file = conversations[choice_idx]
                conversation = Conversation.load(f"{STORAGE_PATH}{selected_file}")
                engine = CHATBOTS[conversation.bot_name]['engine']

                BotClass = globals()[conversation.bot_name]
                bot = BotClass(bot_name=conversation.bot_name, engine=engine, previous_conversation=conversation)
                bot.user_name = conversation.user_name
                bot.start_chat()

            elif action == 1:

                for idx, bot in enumerate(CHATBOTS["chatbots"]):
                    print(f"[{idx}] {bot['name']}")

                choice_idx = int(input("Enter the index of chatbot you want to chat with: "))

                if choice_idx < 0 or choice_idx >= len(CHATBOTS["chatbots"]):
                    raise ValueError("Invalid chatbot index.")

                selected_bot = CHATBOTS["chatbots"][choice_idx]

                BotClass = globals()[selected_bot["name"]]

                bot = BotClass(

                    bot_name=selected_bot["name"],

                    engine=selected_bot["engine"],

                    behavior=selected_bot["behavior"]

                )

                bot.start_chat()

        except ValueError as ve:
            print(f"Error: {ve}")


if __name__ == "__main__":
    openai.api_key = config('OPENAI_API_KEY')
    if not openai.api_key:
        print("Please set your OpenAI API key in the environment variables or the .env file.")
        exit()

    CHATBOTS = ChatbotManager.load_chatbots_config()
    ChatbotManager.start_or_continue_conversation()
