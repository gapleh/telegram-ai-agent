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

### Deploying on AWS EC2 (t2.micro Free Tier)

This section guides you through deploying the Telegram AI Agent on an AWS EC2 `t2.micro` instance, which is eligible for the AWS Free Tier.

#### 1. Launching a t2.micro EC2 Instance

1.  **Sign in to AWS Management Console**: Go to [https://aws.amazon.com/console/](https://aws.amazon.com/console/) and sign in.
2.  **Navigate to EC2 Dashboard**: Search for "EC2" in the services search bar and select it.
3.  **Launch Instance**: Click on "Launch Instance" from the EC2 Dashboard.
4.  **Choose an Amazon Machine Image (AMI)**:
    -   Select "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type" (or a similar free tier eligible Ubuntu AMI).
5.  **Choose an Instance Type**: Select `t2.micro` (this should be free tier eligible).
6.  **Configure Instance Details**: Keep default settings for most options. Ensure "Auto-assign Public IP" is enabled.
7.  **Add Storage**: Default 8 GiB General Purpose SSD (gp2) should be sufficient and is free tier eligible.
8.  **Add Tags (Optional)**: Add a tag like `Name: TelegramAIBot`.
9.  **Configure Security Group**:
    -   Create a new security group or select an existing one.
    -   **Add Rule**: Allow SSH access from your IP address (Type: `SSH`, Source: `My IP`).
    -   **Add Rule**: Allow all outbound traffic (Type: `All Traffic`, Destination: `0.0.0.0/0`). This is generally sufficient for a bot that only makes outbound connections. If your bot needs to receive inbound connections on specific ports (e.g., for webhooks), you would need to open those ports here.
10. **Review and Launch**: Review your settings and click "Launch".
11. **Create a new key pair**: Create a new key pair (e.g., `telegram-bot-key.pem`) and download it. **Keep this file secure**, as you will need it to connect to your instance.
12. **Launch Instances**: Click "Launch Instances".

#### 2. SSH into the EC2 Instance

1.  **Locate your instance**: Once the instance is running, find its Public IPv4 DNS or Public IPv4 address in the EC2 Dashboard.
2.  **Set permissions for your key pair**: Open your terminal and navigate to where you saved your `.pem` file. Change its permissions:

    ```bash
    chmod 400 telegram-bot-key.pem
    ```

3.  **Connect to your instance**: Use the following command, replacing `path/to/your/key.pem` with the path to your key file and `ec2-xx-xx-xx-xx.compute-1.amazonaws.com` with your instance's Public IPv4 DNS:

    ```bash
    ssh -i path/to/your/key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
    ```

#### 3. Install Docker and Dependencies

Once connected to your EC2 instance, run the following commands to install Docker:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
newgrp docker
```

#### 4. Clone the Repository

```bash
git clone https://github.com/kevo-dev/telegram-ai-agent.git
cd telegram-ai-agent
```

#### 5. Set Environment Variables

Create a `.env` file in the `telegram-ai-agent` directory:

```bash
nano .env
```

Add your environment variables (replace placeholders with your actual tokens/keys):

```
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
LITELLM_MODEL="gpt-3.5-turbo"
```

Save and exit (Ctrl+X, Y, Enter).

#### 6. Run the Bot with Docker

Build and run the Docker container:

```bash
docker build -t telegram-ai-agent .
docker run -d --name telegram-bot --restart always --env-file ./.env telegram-ai-agent
```

-   `docker build -t telegram-ai-agent .`: Builds the Docker image from your `Dockerfile`.
-   `docker run -d --name telegram-bot --restart always --env-file ./.env telegram-ai-agent`: Runs the container in detached mode (`-d`), names it `telegram-bot`, configures it to restart automatically (`--restart always`), and loads environment variables from your `.env` file.

#### 7. Keeping the Bot Running (using systemd - alternative to `--restart always`)

While `docker run --restart always` is often sufficient, for more robust process management, you can use `systemd`.

1.  **Create a systemd service file**: (Ensure your Docker container is stopped if you used `--restart always`)

    ```bash
sudo nano /etc/systemd/system/telegram-ai-agent.service
    ```

2.  **Add the following content**:

    ```ini
[Unit]
Description=Telegram AI Agent Bot
After=docker.service
Requires=docker.service

[Service]
ExecStartPre=-/usr/bin/docker stop telegram-bot
ExecStartPre=-/usr/bin/docker rm telegram-bot
ExecStart=/usr/bin/docker run --name telegram-bot --env-file /app/.env telegram-ai-agent
WorkingDirectory=/app
Restart=always
User=ubuntu
Group=docker

[Install]
WantedBy=multi-user.target
    ```

    **Note**: Make sure the `ExecStart` command points to the correct path of your `.env` file. If you cloned the repo to `/home/ubuntu/telegram-ai-agent`, then the `.env` file will be at `/home/ubuntu/telegram-ai-agent/.env`. Adjust `WorkingDirectory` and `ExecStart` accordingly.

3.  **Reload systemd, enable, and start the service**:

    ```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-ai-agent.service
sudo systemctl start telegram-ai-agent.service
    ```

4.  **Check the service status**:

    ```bash
sudo systemctl status telegram-ai-agent.service
    ```

#### 8. Basic Troubleshooting Tips

-   **Bot not responding**: Check the bot's logs:
    ```bash
    docker logs telegram-bot
    ```
    If using `systemd`:
    ```bash
    journalctl -u telegram-ai-agent.service -f
    ```
-   **Permission errors**: Ensure your `.pem` key has `chmod 400` permissions. Also, ensure the `ubuntu` user is part of the `docker` group (`sudo usermod -aG docker ubuntu` and `newgrp docker`).
-   **Environment variables not loaded**: Double-check your `.env` file for typos and ensure it's correctly referenced in your `docker run` command or `systemd` service file.
-   **Security Group issues**: Verify that your EC2 instance's security group allows necessary inbound/outbound traffic. For a Telegram bot, outbound HTTPS (port 443) is crucial.
-   **LiteLLM errors**: Ensure your `OPENAI_API_KEY` (or other LLM API keys) is correct and has the necessary permissions for the chosen `LITELLM_MODEL`.
