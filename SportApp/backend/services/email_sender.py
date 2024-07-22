from django.core.mail import send_mail

import abc


class BaseEmailSender(metaclass=abc.ABCMeta):
	"""
	Interface for email senders.
	"""

	def __init__(self, send_to: str, subject: str, message: str) -> None:
		self.send_to = send_to
		self.subject = subject
		self.message = message

	def send_email(self) -> None:
		pass


class TextEmailSender(BaseEmailSender):
	"""
	Email sender of messages as a text.
	"""

	def send_email(self) -> None:
		send_mail(
			subject=self.subject,
			message=self.message,
			from_email=None,
			recipient_list=[self.send_to],
			fail_silently=True,
		)
