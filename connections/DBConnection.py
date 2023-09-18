import mysql.connector
import os

class DBConnection:

    def __init__(self):
        
        self.config = {
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'database': os.getenv("DB_APP"),
            'raise_on_warnings': True
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor() # Inicializa o cursor
                print("Conexão bem-sucedida ao banco de dados MySQL")
                return self.connection  
        except mysql.connector.Error as error:
            print("Erro ao conectar ao banco de dados MySQL:", error)

    def close_connection(self):
        if self.connection.is_connected():
            try:
                self.connection.close()
                print("Conexão fechada com sucesso")
            except mysql.connector.Error as error:
                print("Ocorreu um erro ao fechar a conexão", error)
