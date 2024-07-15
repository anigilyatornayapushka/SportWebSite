import re

from auths.models import User


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

    if (password.isalpha() or password.isdigit()) and not password.isalnum():
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
        errors.append('Пол должен быть числом'
                      '(1 - мужской, 2 - женский)')

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

    user: User | None = User.objects.get_object_or_none(email=email)

    if user:
        errors.append('Пользователь с таким email уже существует.')

    if errors:
        return True, errors

    return False, []


def validate_weight(weight: str | int) -> tuple[bool, list[str]]:
    """
    Check if weight matches the range.

    Return tuple of number False if everything okay or
    True if there are validation errors and comments of data status.
    """
    errors: list[str] = []

    if isinstance(weight, str) and weight.isdigit():
        weight = int(weight)
        if weight < 35 or weight > 120:
            errors.append('Вес должен входить в диапазон от 35 до 120 кг.')
    else:
        errors.append('Вес должен быть числом.')

    if errors:
        return True, errors
    
    return False, []


def validate_height(height: str | int) -> tuple[bool, list[str]]:
    """
    Check if height matches the range.

    Return tuple of number False if everything okay or
    True if there are validation errors and comments of data status.
    """
    errors: list[str] = []

    if isinstance(height, str) and height.isdigit():
        height = int(height)
        if height < 35 or height > 120:
            errors.append('Высота должна входить в диапазон от 100 до 210 см.')
    else:
        errors.append('Высота должна быть числом.')

    if errors:
        return True, errors
    
    return False, []


def validate_age(age: str | int) -> tuple[bool, list[str]]:
    """
    Check if age matches the range.

    Return tuple of number False if everything okay or
    True if there are validation errors and comments of data status.
    """
    errors: list[str] = []

    if isinstance(age, str) and age.isdigit():
        age = int(age)
        if age < 10 or age > 70:
            errors.append('Возраст должен входить в диапазон от 35 до 120.')
    else:
        errors.append('Возраст должен быть числом.')

    if errors:
        return True, errors
    
    return False, []
