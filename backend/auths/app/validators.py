import re
import datetime

from .models import User


def validate_name(name: str) -> tuple[bool, list[str]]:
	"""
	Check if name is not empty and
	consists of russian letters.

	Return tuple of number False if everything okay or
	True if there are validation errors and comments of data status.
	"""
	errors: list[str] = []

	if len(name) == 0:
		errors.append('Не может быть пустым.')

	if not re.match(r'[а-яА-ЯёЁ]+', name):
		errors.append('Должно состоять из русских букв.')

	if errors:
		return True, errors

	return False, []


def validate_password(password: str) -> tuple[bool, list[str]]:
	"""
	Check if password longer than 7 symbols
	and consist of numbers, different cases letters

	Return tuple of number False if everything okay or
	True if there are validation errors and comments of data status.
	"""
	errors: list[str] = []

	if len(password) < 7 or len(password) > 128:
		errors.append('Пароль должен быть от 7 до 128 символов.')

	if re.match(r'^[a-zA-Z]+$', password) or password.isdigit():
		errors.append('Пароль должен состоять из цифр и букв.')

	if errors:
		return True, errors

	return False, []


def validate_gender(gender: str | int) -> tuple[bool, list[str]]:
	"""
	Check if gender exists

	Return tuple of number False if everything okay or
	True if there are validation errors and comments of data status.
	"""
	errors: list[str] = []

	if isinstance(gender, str) and gender.isdigit():
		gender = int(gender)

	if gender != User.MALE and gender != User.FEMALE:
		errors.append('Пол должен быть числом' '(1 - мужской, 2 - женский)')

	if errors:
		return True, errors

	return False, []


def validate_email(email: str) -> tuple[bool, list[str]]:
	"""
	Check if email matches pattern.

	Return tuple of number False if everything okay or
	True if there are validation errors and comments of data status.
	"""
	errors: list[str] = []

	if not re.match(r'[a-zA-Z0-9]+@[a-z]+\.[a-z]+', email):
		errors.append('Неправильный формат почты.')

	if errors:
		return True, errors

	return False, []


def validate_unique_user(email: str) -> tuple[bool, list[str]]:
	"""
	Check and return if user with this email already exists.
	"""
	errors: list[str] = []

	user: User | None = User.objects.filter(email=email)

	if user:
		errors.append('Пользователь с таким email уже существует.')

	if errors:
		return True, errors

	return False, []


def validate_weight(weight: int) -> tuple[bool, list[str]]:
	"""
	Check if weight matches the range.

	Return tuple of number False if everything okay or
	True if there are validation errors and comments of data status.
	"""
	errors: list[str] = []

	if weight < 35 or weight > 120:
		errors.append('Вес должен входить в диапазон от 35 до 120 кг.')

	if errors:
		return True, errors

	return False, []


def validate_height(height: int) -> tuple[bool, list[str]]:
	"""
	Check if height matches the range.

	Return tuple of number False if everything okay or
	True if there are validation errors and comments of data status.
	"""
	errors: list[str] = []

	if height < 100 or height > 210:
		errors.append('Высота должна входить в диапазон от 100 до 210 см.')

	if errors:
		return True, errors

	return False, []


def validate_age(date: datetime.date) -> tuple[bool, list[str]]:
	"""
	Check if user's age matches the conditions.

	Return tuple of number False if everything okay or
	True if there are validation errors and comments of data status.
	"""
	errors: list[str] = []

	if date > datetime.date.today() - datetime.timedelta(days=365 * 14):
		errors.append('Пользователь должен быть старше 14 лет.')

	if errors:
		return True, errors

	return False, []
