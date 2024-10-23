# Mail Agent
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)](https://github.com/langchain-ai/langchain)

An intelligent agent that automatically analyzes incoming emails to identify and process requests.

## 📋 Description

This agent leverages the Gmail API and LangChain to:
- Automatically read and analyze incoming emails
- Detect if need to send email
- Send automated responses

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/mail-agent.git
cd insurance-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Gmail

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com)
2. Enable the Gmail API
3. Create OAuth 2.0 credentials
4. Copy the `credentials.json` file to the project folder
5. Create a `.env` file with the following variables:
```
GMAIL_USER=you@gmail.com
OPENAI_API_KEY=sk-proj-...
```

### IMAP & SMTP

1. Get SMTP & IMAP host
2. Create a `.env` file with the following variables:
```
OPENAI_API_KEY=sk-proj-...
IMAP_SERVER=imap.host.com
SMTP_SERVER=smtp.host.com
EMAIL_HOST_USER=me@mail.com
EMAIL_HOST_PASSWORD=PWD
```

## 🚀 Usage

```bash
python main.py
```

The agent will:
1. Connect to the specified email account
2. Analyze new incoming emails
3. Identify requests
4. Send an automated response

## 📁 Project Structure

```
mail-agent/
├── agent.py            # Agent 
├── gmail.py            # Gmail manager
├── mail.py             # Mail manager
├── example.py          # Example folder
│   └── ex_gmail.py     # Gmail example
│   └── ex_mail.py      # Mail example
├── requirements.txt    # Dependencies
├── .env                # Environment variables
└── README.md           # Documentation
```

## 📦 Main Dependencies

- langchain>=0.2.0
- google-api-python-client>=2.0.0

## 🔒 Security

- Gmail credentials are stored locally
- Access tokens are securely managed via OAuth 2.0
- Sensitive data is loaded from environment variables
- Email content is processed securely and not stored permanently

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.