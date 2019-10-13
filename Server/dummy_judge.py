import pika
import time
import threading
import sys
rabbitmq_username = 'judge1'
rabbitmq_password = 'judge1'
host = 'localhost'

global client_id
client_id = 'Nul'

username = ''
password = ''

try:
	connection = pika.BlockingConnection(pika.URLParameters("amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"))
	channel = connection.channel()
	channel.queue_declare(queue = username, durable = True)
	channel.queue_bind(exchange = 'connection_manager', queue = 'client_requests')
	channel.queue_bind(exchange = 'connection_manager', queue = username)
except:
	print("Error")

def login():
	global username
	global password
	username = input('Enter judge username: ') or 'judge00001'
	password = input('Enter judge password: ') or 'CbkTJv'
	print("Sending")
	message = {
		'Code' : 'LOGIN', 
		'Username' : username, 
		'Password' : password,
		'ID' : client_id,
		'Type' : 'JUDGE'
		}
	
	message = json.dumps(message)
	channel.basic_publish(exchange = 'connection_manager', routing_key = 'client_requests', body = message)
	print("Sent")


def handler(ch, method, properties, body):
	global client_id
	server_data = str(body.decode("utf-8"))
	json_data = json.loads(server_data)

	code = json_data["Code"]
	if code == 'JUDGE':
		run_id = json_data['Run ID']
		username = json_data['Client Username'] 
		client_id = json_data['Client ID']
		language = json_data['Language']
		PCode = json_data['PCode']
		Source = json_data['Source']

		message = {
		'Code' : 'VRDCT', 
		'Client Username' : username,
		'Client ID' : client_id,
		'Status' : 'AC',
		'Run ID' : run_id,
		'Message' : 'No Error'
		}
		message = json.dumps(message)


		ch.basic_publish(exchange = 'judge_manager', routing_key = 'judge_verdicts', body = message)
		print('[ JUDGE ] Sent ' + message)
	
	elif code =='VALID':
		client_id = json_data['Client ID']
		message = json_data['Message']
		print('[ ' + code + ' ] ::: ' + client_id + ' ::: ' + message  )
	elif code == 'INVLD':
		print("[ INVALID LOGIN ]")

	return




def listen(queue_name):
	global username
	global password
	print("[ LISTEN ] " + queue_name)
	channel.basic_consume(queue = queue_name, on_message_callback = handler)
	try:
		channel.start_consuming()
	except (KeyboardInterrupt, SystemExit):
		channel.stop_consuming()
		connection.close()
		print("[ STOP ] Keyboard interrupt")
		sys.exit()


def main():
	print('1.Login\n2.Start judging\n3.Exit')
	while True:
		a = input('> ')
		if a == '':
			continue
		a = int(a)
		if a == 1:
			login()
			listen(username)
		elif a == 2:
			listen('judge_requests')
		else:
			break;
	
	print('[ DELETE ] Queue ' + username + ' deleted...')
	channel.queue_delete(username)


main()