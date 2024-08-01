import os
import time
import pika


def get_env(key: str, default: str="") -> str:
    value = os.environ.get(key, default)
    print(f"{key}: {value}")
    return value


class PikaClient:
    def __init__(self, process_callable=None) -> None:
        self.queue_name = get_env("QUEUE_NAME")
        self.exchange_name = get_env("EXCHANGE_NAME")

        credentials = pika.PlainCredentials(get_env("RABBITMQ_USER"), get_env("RABBITMQ_PASSWORD"))
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=get_env("RABBITMQ_HOST", "localhost"), credentials=credentials)
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

    def receive(self) -> None:
        def callback(ch, method, properties, body):
            print(f" [x] Received {body.decode()}")
            time.sleep(body.count(b'.') )
            time.sleep(20)
            print(" [x] Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key="")  # routing key is ignored for fanout exchange type
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback) # , auto_ack=true for auto acknowledgement
        print("Ready to receive message")

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
