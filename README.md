# Mail Agent
![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white) ![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat&logo=googlecloud&logoColor=white)

An intelligent agent that automatically analyzes incoming emails to identify and process requests.

## 🔧 Installation

Clone the repository
```shell
git clone https://github.com/<your-username>/mail-agent.git
cd insurance-agent
```

Create a virtual environment
```shell
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

Install dependencies
```shell
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

```python
from agent import AgentMail

# create template (prompt)
template = """Bla bla bla"""

# init agent
agentMail = AgentMail(template=template)

# check mail
data = agentMail.classifyMail("Body mail")
```

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

## 📝 License

This project is licensed under the MIT License.