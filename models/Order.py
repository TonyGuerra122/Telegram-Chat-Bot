import mysql.connector
from connections.DBConnection import DBConnection

class Order:
    
    def __init__(self, client_name, order_desc):
        self.client_name = client_name
        self.order_desc = order_desc
        self.__connection = DBConnection()
    
    def save(self):
        try:
            conn = self.__connection.connect()
            cursor = conn.cursor()

            sql = "INSERT INTO orders (client_name, order_desc) VALUES (%s, %s)"
            values = (self.client_name, self.order_desc)

            cursor.execute(sql, values)  # Execute a inserção usando a conexão

            conn.commit()  # Faça o commit usando a conexão, não o cursor

            print("Inserção realizada com sucesso")
            return True
        except mysql.connector.Error as error:
            print("Ocorreu um erro", error)
            return False
        finally:
            self.__connection.close_connection()
            cursor.close()
    
    def show_my_orders(self):
        try:
            conn = self.__connection.connect()
            cursor = conn.cursor()

            sql = "SELECT id AS id_number, client_name, status, order_desc FROM orders WHERE client_name = %s"
            values = (self.client_name,)
            cursor.execute(sql, values)

            # Recupere todos os registros como uma lista de strings formatadas
            orders = []
            for record in cursor.fetchall():
                id_number, client_name, status, order_desc = record

                status_msg = "Entrege" if status == 0 else "Pendente"

                formatted_order = f"Cliente: {client_name} \nStatus: {status_msg} \nDescrição: {order_desc} \nNúmero do pedido: {id_number}"
                orders.append(formatted_order)

            return orders
        except mysql.connector.Error as error:
            print("Ocorreu um erro", error)
            return None
        finally:
            cursor.close()
            conn.close()
    def __exists(self, id_number):
        try:
            conn = self.__connection.connect()
            cursor = conn.cursor()

            sql = "SELECT COUNT(id) AS total FROM orders WHERE id = %s"
            values = (id_number,)
            cursor.execute(sql, values)

            data = []
            for record in cursor.fetchall():
                total = record

            return True if total[0] > 0 else False
        except mysql.connector.Error as error:
            print("Ocorreu um erro", error)
            return None
    def delete_my_order(self, id_number):
        if not self.__exists(id_number):
            return False
        try:
            conn = self.__connection.connect()
            cursor = conn.cursor()

            sql = "DELETE FROM orders WHERE id = %s"
            values = (id_number,)
            cursor.execute(sql, values)
            conn.commit()
            return True
        except mysql.connector.Error as error:
            print("Ocorreu um erro", error)
            return False