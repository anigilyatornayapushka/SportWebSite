from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)

from abstracts.models import (
    AbstractModel,
    AbstractManager,
)

import typing


class UserManager(BaseUserManager, AbstractManager):
    """
    Manager for user custom methods.
    """

    def create_user(self, first_name: str, last_name: str,
                    gender: int, password: str, email: str,
                    **extra_fields: typing.Any) -> 'User':
        """
        Create default user method.
        """
        u: User = User(first_name=first_name, last_name=last_name, gender=gender,
                       password=password, email=email, **extra_fields)
        u.set_password(password)
        u.is_active = True
        u.save(using=self._db)
        return u

    def create_superuser(self, first_name: str, last_name: str,
                    gender: int, password: str, email: str,
                    **extra_fields: typing.Any) -> 'User':
        """
        Create admin method.
        """
        u: User = User(first_name=first_name, last_name=last_name, gender=gender,
                       password=password, email=email, **extra_fields)
        u.set_password(password)
        u.is_active = True
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin, AbstractModel):
    """
    Custom model of User.
    """

    MALE = 1
    FEMALE = 2

    GENDERS: tuple = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    first_name: str = models.CharField(
        verbose_name='имя',
        max_length=45
    )
    last_name: str = models.CharField(
        verbose_name='фамилия',
        max_length=45
    )
    gender: int = models.PositiveSmallIntegerField(
        verbose_name='пол',
        choices=GENDERS,
        null=True
    )
    email: str = models.CharField(
        verbose_name='почта',
        max_length=60,
        unique=True
    )
    password: str = models.CharField(
        verbose_name='пароль',
        max_length=128,
        validators=(
            MinLengthValidator(7),
        )
    )
    height: float = models.PositiveSmallIntegerField(
        verbose_name='рост',
        validators=(
            MinValueValidator(100),
            MaxValueValidator(210)
        ),
        null=True
    )
    weight: float = models.PositiveSmallIntegerField(
        verbose_name='вес',
        validators=(
            MinValueValidator(35),
            MaxValueValidator(120)
        ),
        null=True
    )
    age: int = models.PositiveSmallIntegerField(
        verbose_name='возраст',
        validators=(
            MinValueValidator(10),
            MaxValueValidator(70)
        ),
        null=True
    )
    is_active: bool = models.BooleanField(
        verbose_name='активный ли',
        default=False
    )
    is_staff: bool = models.BooleanField(
        verbose_name='сотрудник ли',
        default=False
    )
    is_superuser: bool = models.BooleanField(
        verbose_name='администратор ли',
        default=False
    )
    
    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: tuple = (
        'first_name',
        'last_name',
        'password',
        'gender',
    )

    objects: UserManager = UserManager()

    @property
    def full_name(self) -> str:
        return f'< [{self.id}] {self.last_name} {self.first_name} >'

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
