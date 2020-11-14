
import pika


class RabbitMQ:
    
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.115'))
        self.channel = connection.channel()
     

    def consume(self, queueName, exchange, routingKey, callback):
        self.channel.queue_declare(queue=queueName, durable=True)
        self.channel.exchange_declare(exchange=exchange, durable=True, auto_delete=True)
        self.channel.queue_bind(queue=queueName, exchange=exchange, routing_key=str(routingKey))
        self.channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)
        print("Consuming...")
        self.channel.start_consuming()

    def publish(self, queueName, exchange, routingKey, data):
        self.channel.queue_declare(queue=queueName, durable=True)
        self.channel.exchange_declare(exchange=exchange, durable=True, auto_delete=True)
        self.channel.queue_bind(queue=queueName, exchange=exchange, routing_key=str(routingKey))
        self.channel.basic_publish(exchange=exchange, routing_key=str(routingKey), body=data)
        print("Published")

 