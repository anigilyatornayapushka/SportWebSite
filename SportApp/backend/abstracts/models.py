from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

import datetime
import typing


class AbstractManager(models.Manager):
	"""
	Abstract manager with all most required methods.
	"""

	def get_not_deleted(self) -> QuerySet[typing.Any] | None:
		"""
		Get query set of all not deleted objects.
		"""
		queryset: QuerySet[typing.Any] = self.filter(
			datetime_deleted__isnull=True
		)
		return queryset

	def get_deleted(self) -> QuerySet[typing.Any] | None:
		"""
		Get query set of all deleted objects.
		"""
		queryset: QuerySet[typing.Any] = self.filter(
			datetime_deleted__isnull=False
		)
		return queryset

	def get_object_or_none(self, **filter) -> QuerySet[typing.Any] | None:
		"""
		Get object or None using filter.
		"""
		try:
			obj: typing.Any = self.get(**filter)
		except self.model.DoesNotExist:
			obj = None
		finally:
			return obj


class AbstractModel(models.Model):
	"""
	A model that implements all required
	fields for every other model.
	"""

	datetime_created: datetime.datetime = models.DateTimeField(
		verbose_name='время создания',
		default=timezone.now,
		null=True,
		blank=True,
	)
	datetime_updated: datetime.datetime = models.DateTimeField(
		verbose_name='время обновления',
		editable=True,
		auto_now=True,
		null=True,
		blank=True,
	)
	datetime_deleted: datetime.datetime = models.DateTimeField(
		verbose_name='время удаления', null=True, blank=True
	)

	objects: AbstractManager = AbstractManager()

	def delete(self):
		"""
		Soft delete the object by setting datetime_deleted to current time.
		"""
		self.datetime_deleted = timezone.now()
		self.save()

	class Meta:
		abstract = True
