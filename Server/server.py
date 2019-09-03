import threading
import pika
from rabbitmq_connections import manage_connection
from client_connections import manage_clients
# Variables  
rabbitmq_username = 'BitsOJ'
rabbitmq_password = 'root'
host = 'localhost'


def main():
	print("----------------BitsOJ v1.0----------------")
	
	# This function handles the client login requests
	channel, connection = manage_connection.initialize_connection(rabbitmq_username, rabbitmq_password, host)
	manage_clients.listen_clients(channel)



	manage_connection.terminate_connection(connection)
main()


