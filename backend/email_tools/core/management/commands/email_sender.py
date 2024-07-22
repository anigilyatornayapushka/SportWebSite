from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone

import json
import pika


class Command(BaseCommand):
	help = 'Consumes messages from RabbitMQ and sends emails'
	queue_name = 'email_queue'

	def handle(self, *args, **kwargs) -> None:
		connetion_param = pika.ConnectionParameters('localhost')
		connection = pika.BlockingConnection(connetion_param)
		channel = connection.channel()
		channel.queue_declare(queue=self.queue_name)

		def _callback(*_, body) -> None:
			data: dict = json.loads(body)
			send_mail(
				subject=data.get('subject'),
				message=data.get('message'),
				from_email=None,
				recipient_list=[data.get('send_to')],
				fail_silently=True,
			)
			print(
				f'  [i] {timezone.now()}: {data.get('sent_to')} | {data.get('subject')}'  # noqa: E501
			)  # noqa: E501

		channel.basic_consume(
			queue=self.queue_name, on_message_callback=_callback, auto_ack=True
		)

		print('  [i] Ожидание сообщений. для выхода нажмите CTRL+C')
		channel.start_consuming()
