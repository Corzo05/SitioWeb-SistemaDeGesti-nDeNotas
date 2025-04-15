import mysql.connector

# PythonAnywhere

HOST1 = 'Corzo05.mysql.pythonanywhere-services.com'
USER1 = 'Corzo05'
PASSWORD1 = 'pythonDB'
DATABASE1 = 'Corzo05$cueto2'

# Localhost

HOST2 = 'localhost'
USER2 = 'root'
PASSWORD2 = ''
DATABASE2 = 'cueto'

try:
    database = mysql.connector.connect(
        host= HOST1,
        user= USER1,
        password= PASSWORD1,
        database= DATABASE1
    )
except:
    database = mysql.connector.connect(
        host= HOST2,
        user= USER2,
        password= PASSWORD2,
        database= DATABASE2
    )

print("Conectado a: ", database.server_host)