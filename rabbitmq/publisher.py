from datetime import datetime
import pika

class PikaClient:
    def __init__(self, process_callable=None) -> None:
        self.queue_name = "poc-keda"
        self.exchange_name = "keda"

        credentials = pika.PlainCredentials('keda', 'test123')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="fanout")  # comment this out to use default exchange type

        # persistent queue
        self.queue = self.channel.queue_declare(queue=self.queue_name, durable=True)
        
        # # temporary queue
        # self.queue = self.channel.queue_declare(queue='', exclusive=True)
        # self.callback_queue = self.queue.method.queue  # random queue name

        self.response = None
        self.process_callable = process_callable

    def publish(self, message: str) -> None:
        self.channel.basic_publish(
            exchange=self.exchange_name,  # ""  for default exchange
            routing_key="",  # Fanout exchange so not required routing key. If default exhange, routing key is self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            )
        )


rabbitmq_client = PikaClient()
for _ in range(100):
    message = datetime.now().timestamp()
    rabbitmq_client.publish(message=f"Your Message is {message}")
    print(f" [x] Sent Message --> Your Message is {message}")

rabbitmq_client.connection.close()