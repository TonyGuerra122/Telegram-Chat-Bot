import telebot
from models.Order import Order

class BotController:

    def __init__(self, api_key):
        self.bot = telebot.TeleBot(api_key)

    def init(self):
        @self.bot.message_handler(commands=["start"])
        def welcome(message):
            chat_id = message.chat.id
            user_name = message.from_user.first_name
            self.bot.send_message(chat_id, f"""
            Olá {user_name}, sou o ChefBot e estou aqui para te ajudar com algum pedido seu.
            Digite /pedido para fazer o seu pedido
            Digite /mostrar_pedidos para ver todos os seu pedidos
            """)

        @self.bot.message_handler(commands=["pedido"])
        def order(message):
            chat_id = message.chat.id
            self.bot.send_message(chat_id, "Por favor, descreva o seu pedido")

            # Use a função lambda para criar uma função anônima que receberá a descrição do pedido
            self.bot.register_next_step_handler(message, lambda msg: make_order(msg, message.from_user))

        def make_order(message, user):
            chat_id = message.chat.id
            name_user = user.first_name + " " + user.last_name
            order_desc = message.text

            order = Order(name_user, order_desc)
            if order.save():
                message_bot = "Pedido Registrado com sucesso"
            else:
                message_bot = "Ocorreu um erro ao registrar o pedido"

            self.bot.send_message(chat_id, message_bot)

        @self.bot.message_handler(commands=["mostrar_pedidos"])
        def show_my_orders(message):
            chat_id = message.chat.id
            name_user = message.from_user.first_name + " " + message.from_user.last_name
            orders = Order(name_user, None).show_my_orders()
            if orders:
                # Use um contador para numerar os pedidos
                order_number = 1
                for order in orders:
                    self.bot.send_message(chat_id, f"Pedido {order_number}:\n{order}")
                    order_number += 1
            else:
                self.bot.send_message(chat_id, "Nenhum pedido foi encontrado")
        @self.bot.message_handler(commands=["cancelar_pedido"])
        def delete_my_order(message):
            chat_id = message.chat.id
            self.bot.send_message(chat_id, "Insira o número do pedido")

            self.bot.register_next_step_handler(message, lambda msg: delete_next(msg))
        
        def delete_next(message):
            chat_id = message.chat.id
            id_number = message.text

            result = order = Order(None, None).delete_my_order(id_number)
            if result:
                self.bot.send_message(chat_id, "Pedido Deletado com sucesso")
            else:
                self.bot.send_message(chat_id, "Este número não foi registrado")            


        self.bot.polling()
