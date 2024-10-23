# * Import libraries
import base64, os.path
from pathlib import Path
from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# * Google
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


class Gmail:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = os.path.join(BASE_DIR, 'credentials.json')

        credentials = Credentials.from_service_account_file(creds, scopes=SCOPES)
        delegated_credentials = credentials.with_subject(config("GMAIL_USER"))
        self.gmail = build('gmail', 'v1', credentials=delegated_credentials)


    def getMail(self, max_results=10, query=''):
        """Get all mails

        Args:
            max_results (int): Number max of mails to get
            query (str): Request query (Gmail format)

        Returns:
            list: List of mails with details
        """

        try:
            # Récupère la liste des messages
            results = self.gmail.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=max_results,
                q=query
            ).execute()

            messages = results.get('messages', [])
            emails = []

            for message in messages:
                msg = self.gmail.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()

                # Extraction des en-têtes importants
                headers = msg['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                sender = next(h['value'] for h in headers if h['name'] == 'From')
                date = next(h['value'] for h in headers if h['name'] == 'Date')

                # Récupération du corps du message
                if 'parts' in msg['payload']:
                    body = self._get_body_from_parts(msg['payload']['parts'])
                else:
                    body = base64.urlsafe_b64decode(
                        msg['payload']['body']['data']
                    ).decode('utf-8')

                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body
                })

            return emails

        except Exception as e:
            print(f"Error : {str(e)}")
            return []


    def _get_body_from_parts(self, parts):
        """Extracts the message body from the message parts."""
        text = ""
        for part in parts:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    text += base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8')
            elif 'parts' in part:
                text += self._get_body_from_parts(part['parts'])
        return text


    def sendMail(self, to, subject, body, content_type="text/plain"):
        """Send email

        Args:
            to (str): Recipient's email address
            subject (str): Email subject
            body (str): Email body
            content_type (str): Type of content (text/plain ou text/html)

        Returns:
            dict: Response of Gmail API after send
        """

        try:
            # Création du message
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject

            # Ajout du corps du message
            msg = MIMEText(body, 'plain' if content_type == "text/plain" else 'html')
            message.attach(msg)

            # Encodage du message
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')

            # Envoi du message
            send_message = self.gmail.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            return send_message

        except Exception as e:
            print(f"Error : {str(e)}")
            return None