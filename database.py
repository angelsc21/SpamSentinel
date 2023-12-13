import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('spam_trap.db')
cursor = conn.cursor()

# Crear una tabla para almacenar información de correos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS spam_emails (
        id INTEGER PRIMARY KEY,
        subject TEXT,
        sender TEXT,
        body TEXT,
        links TEXT,
        ips TEXT
    )
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()