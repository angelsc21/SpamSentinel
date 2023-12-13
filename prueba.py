import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# -----  Main  -----

# Create mail object
mail_msg = MIMEMultipart()
mail_msg['From'] = 'tfm.imf.st1@gmail.com'
mail_msg['To'] = recipient
mail_msg['Subject'] = subject
mail_msg.add_header('reply-to', reply_to)

# Add body
mail_msg.attach(MIMEText(body_wrapped_text, 'plain'))

# Configure smtp server
smtp_server = 'smtp.gmail.com'  
smtp_port = 587  
smtp_username = 'example@gmail.com'
smtp_password = 'example'

# Sent mail
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail('sender@gmail.com', 'sender <sender@gmail.com>', mail_msg.as_string())
    print('Successful')
except smtplib.SMTPException as e:
    print('Error', str(e))


        