# * import libraries
import email, imaplib, smtplib
from decouple import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self):
        # * init
        self.port = 587
        self.imap_host = config('IMAP_SERVER')
        self.smtp_host = config('SMTP_SERVER')
        self.user = config('EMAIL_HOST_USER')
        self.pwd = config('EMAIL_HOST_PASSWORD')

        # * login to server imap
        self.imap = imaplib.IMAP4_SSL(self.imap_host)
        self.imap.login(self.user, self.pwd)

        # * login to server smtp
        self.smtp = smtplib.SMTP(self.smtp_host, self.port)

    def getText(self, msg):
        """Extracts the text content from a given email message.

        Args:
            msg: The email message object.

        Returns:
            The extracted text content.
        """

        if msg.is_multipart():
            return self.getText(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)


    def detectMail(self)->list:
        """Get all mails

        Returns:
            list: List of mails with details
        """

        try:
            self.imap.select('Inbox')
            client = []

            _, data = self.imap.uid('search', None, 'ALL')

            for num in data[0].split()[:3]:
                # Check email is read or unread
                _, msg_data = self.imap.uid('fetch', num, "(FLAGS)")
                if msg_data and msg_data[0] is not None:
                    flags = imaplib.ParseFlags(msg_data[0])
                    is_read = r'\Seen' in [flag.decode() for flag in flags]

                _, data = self.imap.uid('fetch', num, '(RFC822)')

                # Convert Bytes :
                email_message = email.message_from_bytes(data[0][1])

                # Exploit email text :
                text = self.getText(email_message)

                client.append({
                    'from': email_message['from'],
                    'subject': email_message['subject'],
                    'text': text
                })

                # Remove "Seen" Flag
                if not is_read:
                    self.imap.uid('STORE', num, '-FLAGS', '(\Seen)')

            return client
        except Exception as e:
            print(f"Error : {str(e)}")
            return []




    def sendEmail(self, to:str, subject:str, body:str, content_type:str)->str:
        """Send email

        Args:
            to (str): Recipient's email address
            subject (str): Email subject
            body (str): Email body
            content_type (str): Type of content (plain or html)

        Returns:
            str: ok or error
        """

        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.user
            msg['To'] = to

            body = body

            part = MIMEText(body, 'plain')

            msg.attach(part)

            with self.smtp as server:
                server.starttls()
                server.login(self.user, self.pwd)
                server.sendmail(self.user, to, msg.as_string())

            return "ok"
        except Exception as e:
            print(f"Error : {str(e)}")
            return "error"