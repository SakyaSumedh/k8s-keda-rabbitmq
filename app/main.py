from utils.pika_client import PikaClient

rabbitmq_client = PikaClient()
rabbitmq_client.receive()
rabbitmq_client.connection.close()