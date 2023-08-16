# OpenAI-ChatGPT-Customizable-Behaviour-Chatbots

Welcome to the OpenAI-ChatGPT-Customizable-Behaviour-Chatbots Repository! Dive into a world powered by OpenAI's GPT, offering modular and extensible chatbot experiences. Engage with personalities like Henry and Vera more you can create yourself, and even save conversations to resume later.

## Features:

- **Persistent Conversations**: Your chats aren't fleeting; save and continue whenever you wish.

- **Diverse Personalities**: Engage with chatbot personalities like `Henry` and `Vera`, each exuding distinct charm. You can also create your own choosing personalities give names in configuration file.

- **Simple UI**: Effortlessly chat, initiate a new conversation, or pick up from where you left from the terminal app.

- **Conversation Analytics**: Dive deeper into chats with insights on conversation topics and metrics.

## Setup:

### Prerequisites:
- Python 3.9 or higher versions

### Installation:
1. Clone this repository:
   ```bash
   git clone https://github.com/CihatAcar/OpenAI-ChatGPT-Customizable-Behaviour-Chatbots.git

2. Navigate to the repository's directory:
   ```bash
   cd path-to-chatbot-repo
   ```

3. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```
* Ensure your OpenAI API key is either set in the environment variables or stored in a .env file under the key OPENAI_API_KEY.

# Getting Started:
* Once set up, run the chatbot application:
   ```bash
   python main.py
   ```
* Follow on-screen instructions to begin or continue a conversation.

## Repo Structure:

- **main.py**: The heart of the application. It introduces Chatbot and ChatbotManager classes, offering functionality and flow.
- **utilities.py**: Meet the Conversation class handling the history, analytics, and other metrics of your chats.
- **chatbots_config.yaml**: Customize or check out configurations of chatbots, their unique behaviors, and engine details.
- **conversations/**: An archive. Every conversation you save is stored here in a neat JSON format.

## Meet the Chatbots:

- **Henry**: Engage with a warm and friendly bot that adjusts its tone and style based on pre-configured behaviors.
- **Vera**: Vera is ever-ready to chat with a sad tone of unique personality defined in the configuration settings.


## Engage and Contribute:

Enhancements, bug fixes, or ideas? Please fork, make changes, and send us a pull request. Or perhaps open an issue to start a discussion.
