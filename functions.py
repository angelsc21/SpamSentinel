import re
import os

# -----  Functions  -----

""""
    Extracts links from mail file data
    Args: 
        raw_mail contains the mail file data
    Returns:
        1. Unique array containing extracted links.
        2. Empty array
"""
def extract_links(raw_mail):
    # Utilizar una expresión regular para buscar enlaces HTTP
    http_pattern = rb'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    links = re.findall(http_pattern, raw_mail)
    formatted_links = set()
    for link in links:
                formatted_links.add(link.decode('utf-8'))

    return formatted_links

""""
    Extracts plain text without html tags from mail file html body
    Args: 
        message contains mail html body
    Returns:
        1. Plain text without html tags
        2. Nothing
"""
def extract_text_body(message):
    for part in message.walk():
        if part.get_content_type() == 'text/html':
            try:
                return part.get_payload(decode=True).decode('utf-8')
            except UnicodeDecodeError:
                # Si la decodificación UTF-8 falla, intenta otras codificaciones
                possible_encodings = ['utf-8', 'iso-8859-1', 'latin-1']
                for encoding in possible_encodings:
                    try:
                        return part.get_payload(decode=True).decode(encoding)
                    except UnicodeDecodeError:
                        pass  # Si la decodificación con esta codificación falla, continúa con la siguiente
                # Si todas las codificaciones fallan, regresa una cadena vacía
                return ''
    return ''

""""
    Extracts ip addresses from mail file data
    Args: 
        message contains the mail file data
    Returns:
        1. Unique array containing extracted ip addresses.
        2. Empty array
"""
def find_ip_addresses(raw_mail):
    # Utilizar una expresión regular para buscar direcciones IP
    ip_pattern = rb'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    all_addresses = re.findall(ip_pattern, raw_mail)
    formatted_addresses = set()
    for address in all_addresses:
                formatted_addresses.add(address.decode('utf-8'))
    formatted_addresses = [ip for ip in formatted_addresses if not ip.startswith('0.')]
    return formatted_addresses

""""
    Extracts sender mail address from mail file line data which contains the 
    sender and returns the address cleaned and divided into name and domain
    Args: 
        sender contains the mail file line which contains the sender between <>
    Returns:
        1. Sender address cleaned and divided into name and domain.
        2. Empty
"""
def obtain_email_address(sender):
    re_sender = r'<(\S+)@(\S+)>'
    result = re.search(re_sender, sender)
    if result:
        return result.group(1), result.group(2)
    else:
        return '', ''
    
""""
    Insert a row with mail extracted data in the database
    Args: 
        sender contains the mail file line which contains the sender between <>
    Returns:
        1. Sender address cleaned.
        2. Empty
"""
def insert(cursor, subject, sender, body_wrapped_text, links, addresses):
    # Store data

        if links:
            links_str = ', '.join(links)
        else:
            links_str = 'No Links'

        if addresses:
            ips_str = ', '.join(addresses)
        else:
            ips_str = 'No IP addresses'

        query = '''
            INSERT INTO spam_emails (subject, sender, body, links, ips)
            VALUES (?, ?, ?, ?, ?)
        '''

        # Convertir los vectores en cadenas de texto
        if links:
            links_str = ', '.join(links)
        else:
            links_str = 'No Links'

        if addresses:
            ips_str = ', '.join(addresses)
        else:
            ips_str = 'No IP addresses'

        # Ejecutar la consulta con los valores de las variables
        cursor.execute(query, (str(subject), str(sender), str(body_wrapped_text), links_str, ips_str))

""""
    Stores attached files
    Args: 
        email_message mail data in bytes
    Returns:
        If there is an attached file, it will be stored at the path selected
"""
def get_attachments(email_message):
    if email_message.is_multipart():
        text_content = None
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    filepath = os.path.join('/home/your_user', filename)
                    open(filepath, "wb").write(part.get_payload(decode=True))
                    print("Saved attachment:", filename)