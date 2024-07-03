import imaplib
import email
from dateutil import parser
from email.header import decode_header
from datetime import datetime
from email.utils import parseaddr
from bs4 import BeautifulSoup
import re


class EmailParser:
    @staticmethod
    def decode_text(text, charset='utf-8'):
        try:
            return text.decode(charset) if charset else text.decode('utf-8')
        except Exception as e:
            print(f"Error decoding text: {e}")
            return text.decode('utf-8', errors='replace')
    @staticmethod
    def parse_attachment(part):
        filename = part.get_filename()
        if filename:
            filename = decode_header(filename)
            decoded_filename = ''.join([str(text, charset or 'utf-8') if isinstance(text, bytes) else text for text, charset in filename])
            return {
                'filename': decoded_filename,
                'content_type': part.get_content_type()
            }
        return None
    @staticmethod
    def clean_body(text):
        cleaned_text = re.sub(r'\n\d+\.', '', text)
        cleaned_text = cleaned_text.replace('\xa0', ' ').replace('\n', ' ').strip()
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text
    @staticmethod
    def process_part(part):
        attachments = []
        body = None
        html = None

        for content_part in part.walk():
            content_disposition = content_part.get('Content-Disposition', '')
            content_type = content_part.get_content_type()

            if content_disposition.startswith('attachment'):
                attachment = EmailParser.parse_attachment(content_part)
                if attachment:
                    attachments.append(attachment)
            
            elif content_type == 'text/plain':
                if body is None:
                    body = ''
                body += EmailParser.decode_text(content_part.get_payload(decode=True), content_part.get_content_charset())
                body = EmailParser.clean_body(body)
                
            elif content_type == 'text/html':
                if html is None:
                    html = ''
                html += EmailParser.decode_text(content_part.get_payload(decode=True), content_part.get_content_charset())

        data = {
            'body': body,
            'attachments': attachments
        }
        
        return data
    @staticmethod
    def clean_date_string(date_string):
        return re.sub(r'\(.*\)', '', date_string).strip()

    @staticmethod
    def parse_email(raw_email):
        msg = email.message_from_bytes(raw_email)
        email_account = email.utils.parseaddr(msg['From'])
        email_account = email_account[1]
        #print(f'Email: {email_account}')
        
    
        
        # Тема письма
        subject = msg.get('Subject')
        if not isinstance(subject, (str, bytes)):
            topic = ''
        else:
            decoded_header = decode_header(subject)
            topic = ''.join([str(text, charset or 'utf-8') if isinstance(text, bytes) else text for text, charset in decoded_header])
        #print(f'Subject: {topic}')

        
        # Дата отправки
        date_sent = msg.get('Date')
        if date_sent:
            try:
                date_sent = parser.parse(EmailParser.clean_date_string(date_sent))
            except parser.ParserError as e:
                date_sent = datetime.now() 

            #date_sent = datetime.strptime(date_sent, '%a, %d %b %Y %H:%M:%S %z')
        #print(f"Date Sent: {date_sent}")
        

        received = msg.get_all('Received')
        if received:
            try:
                last_received = received[-1].split(';')[-1].strip()
                date_received = parser.parse(EmailParser.clean_date_string(last_received))
            except parser.ParserError as e:
                date_received = datetime.now()
        else:
            date_received = datetime.now()  
        #print(f"Date Received: {date_received}")
        body = EmailParser.process_part(msg)
        data = {
            'email' : email_account,
            'topic' : topic,
            'date_sent' : date_sent,
            'date_recieved': date_received,
            'body': body['body'],
            'attachments': body['attachments']

        }
        #print(data)
        return data
        
    def fetch_all_emails(user, password):
        if user[user.find('@')+1:user.find('.')] == 'gmail':
            imap_url = 'imap.gmail.com'
        elif user[user.find('@')+1:user.find('.')] == 'mail':
            imap_url = 'imap.mail.ru'
        elif user[user.find('@')+1:user.find('.')] == 'yandex':
            imap_url = 'imap.yandex.ru'
        try:

            con = imaplib.IMAP4_SSL(imap_url)
            con.login(user, password)
            con.select('INBOX')
            result, data = con.search(None, 'ALL')

            emails = []
            for num in data[0].split():
                result, data = con.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                email_data = EmailParser.parse_email(raw_email)
                emails.append(email_data)
            con.logout()
            return emails
        except imaplib.IMAP4.error as e:
            return 'Невозможно подключиться'


