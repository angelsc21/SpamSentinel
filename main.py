import email.message
import os
from bs4 import BeautifulSoup
import textwrap
import sqlite3
import glob
from elasticsearch import Elasticsearch
from functions import *


# --------------------  MAIN  --------------------

# Searching for mails stored locally
root = "/home/user/Untrouble_Database"
search_pattern = root + "/**/**/*"
files = [archivo for archivo in glob.glob(search_pattern, recursive=True) if os.path.isfile(archivo)]
es = Elasticsearch(['http://localhost:9200']) # Connect to elasticsearch

# Connect to database
conn = sqlite3.connect('spam_trap.db')
cursor = conn.cursor()

# Analyzing mail files one by one
for mail_file in files:

    with open(mail_file, 'rb') as file:

        email_data = file.read() # Raw content of the email
        msg = email.message_from_bytes(email_data) # Structure and data of the email to simplify the analysis
        subject = msg['Subject']
        sender = msg['From']
        sender_name, sender_domain = obtain_email_address(str(sender))

        # Clean HTML, whitespaces, newlines ... from body
        try:
            soup = BeautifulSoup(extract_text_body(msg), 'html.parser')
            text_body = soup.get_text()
            body_wrapped_text = textwrap.fill(text_body, width=80)
        except Exception as e:
            print(f"Error: {e}")
            body_wrapped_text = 'cuerpo del correo no procesable'

        # Extract links
        links = extract_links(email_data)

        # Extract IP adresses
        addresses = find_ip_addresses(email_data)  

        # Insert mail extracted data into the 'spam_emails' table of the database
        insert(cursor, subject, sender, body_wrapped_text, links, addresses)

        # Prepare data to be sent to elasticsearch
        index_data = {
            'subject': str(subject),
            'sender_name': sender_name,
            'sender_domain': sender_domain,
            'body': str(body_wrapped_text),
            'links': list(links),
            'ips': list(addresses)
        }
        es.index(index='prueba2', body=index_data)
     
conn.commit()
conn.close()

        