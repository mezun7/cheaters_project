import pika


def callback(ch, method, properties, body):
    print(f'Received: {body}')


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='checker', durable=True)

channel.basic_consume(queue='checker',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# channel.close()
