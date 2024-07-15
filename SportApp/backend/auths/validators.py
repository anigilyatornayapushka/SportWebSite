import re

from auths.models import User


def validate_name(name: str) -> tuple[bool, list[str]]:
    """
    Check if name is not empty and
    consists of russian letters.

    Return tuple of number 0 if everything okay or
    1 if there are validation errors and comments of data status.
    """
    errors: list[str] = []

    if len(name) == 0:
        errors.append('Не может быть пустым.')

    if not re.match(r'[а-яА-ЯёЁ]+', name):
        errors.append('Должно состоять из русских букв.')

    if errors:
        return 1, errors

    return 0, []


def validate_password(password: str) -> tuple[bool, list[str]]:
    """
    Check if password longer than 7 symbols
    and consist of numbers, different cases letters

    Return tuple of number 0 if everything okay or
    1 if there are validation errors and comments of data status.
    """
    errors: list[str] = []

    if len(password) < 7 or len(password) > 128:
        errors.append('Пароль должен быть от 7 до 128 символов.')

    if (password.isalpha() or password.isdigit()) and not password.isalnum():
        errors.append('Пароль должен состоять из цифр и букв.')

    if errors:
        return 1, errors

    return 0, []


def validate_gender(gender: str | int) -> tuple[bool, list[str]]:
    """
    Check if gender exists

    Return tuple of number 0 if everything okay or
    1 if there are validation errors and comments of data status.
    """
    errors: list[str] = []

    if isinstance(gender, str) and gender.isdigit():
        gender = int(gender)

    if gender != User.MALE and gender != User.FEMALE:
        errors.append('Пол должен быть числом'
                      '(1 - мужской, 2 - женский)')

    if errors:
        return 1, errors

    return 0, []


def validate_email(email: str) -> tuple[bool, list[str]]:
    """
    Check if email matches pattern.

    Return tuple of number 0 if everything okay or
    1 if there are validation errors and comments of data status.
    """
    errors: list[str] = []

    if not re.match(r'[a-zA-Z0-9]+@[a-z]+\.[a-z]+', email):
        errors.append('Неправильный формат почты.')

    if errors:
        return 1, errors
    
    return 0, []
