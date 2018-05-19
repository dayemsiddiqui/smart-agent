#!/usr/bin/env python
import pika
import json
from pprint import pprint

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='node')
channel.queue_declare(queue='python')


def parseAction(method):
	if method == 'start_listening':
		print("Started Listening")
		publish_me({'type': 'response', 'statement': 'Play the song of ColdPlay'})
	if method == 'stop_listening':
		print("Stopped Listening")

def callback(ch, method, properties, body):
	j = json.loads(body)
	print()
	if j['type'] == 'action':
		parseAction(j['method'])
    # print(" [x] Received %r" % body)

def publish_me(msg):
	channel.basic_publish(exchange='',
                      routing_key='python',
                      body=json.dumps(msg))    

channel.basic_consume(callback,
                      queue='node',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
