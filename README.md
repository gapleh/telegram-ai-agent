# Telegram AI Agent with LiteLLM

This project is a Telegram bot that acts as an AI assistant, using LiteLLM to connect to various language models. It supports conversation history and is designed for easy deployment.

## Features

- **AI-Powered Conversations**: Responds to user messages with AI-generated answers.
- **Conversation History**: Maintains context for each user, allowing for more natural conversations.
- **LiteLLM Integration**: Uses LiteLLM as a proxy to route requests to different AI models (e.g., GPT-3.5-turbo, and others supported by LiteLLM).
- **Easy Deployment**: Can be deployed using Docker on platforms like Render.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- A Telegram Bot Token
- An API key for your chosen LLM (e.g., OpenAI)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kevo-dev/telegram-ai-agent.git
   cd telegram-ai-agent
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

### Configuration

1. **Get a Telegram Bot Token:**

   - Talk to the [BotFather](https://t.me/botfather) on Telegram.
   - Use the `/newbot` command to create a new bot.
   - The BotFather will give you a token. Keep it safe.

2. **Set up environment variables:**

   - Create a `.env` file in the project root by copying the example file:

     ```bash
     cp .env.example .env
     ```

   - Open the `.env` file and add your credentials:

     ```
     TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
     OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
     LITELLM_MODEL="gpt-3.5-turbo" # Optional, you can specify any model supported by LiteLLM
     ```

### Running the Bot Locally

Once you have configured your environment variables, you can run the bot:

```bash
python bot.py
```

Your bot should now be running and responding to messages on Telegram.

## Deployment

This bot is designed to be deployed easily using Docker.

### Deploying on Render

Render is a platform that offers free tiers for web services, making it a good choice for deploying this bot.

1. **Push your code to a GitHub repository.**

2. **Create a new Web Service on Render:**

   - Connect your GitHub account to Render.
   - Select your repository.
   - Configure the service:
     - **Environment**: `Docker`
     - **Name**: `telegram-ai-agent` (or your preferred name)
     - **Start Command**: This will be automatically detected from the `Dockerfile`.

3. **Add your environment variables:**

   - In the Render dashboard, go to the "Environment" tab for your service.
   - Add the following secret files:
     - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
     - `OPENAI_API_KEY`: Your OpenAI API key.
     - `LITELLM_MODEL`: (Optional) The LiteLLM model you want to use.

4. **Deploy:**

   - Click "Create Web Service".
   - Render will build and deploy your bot.

Your Telegram bot is now live!
