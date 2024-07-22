import datetime
import re


def datefy(date: str) -> tuple[bool, datetime.date | list[str]]:
	"""
	Converts a string to a datetime.date

	Return True if there are errors, False if there are no errors

	and description of error or datetime.date of string.
	"""
	if not re.match(r'\d{2}\.\d{2}\.\d{4}', date):
		return True, ['Дата не соответствует формату ДД/ММ/ГГГГ']
	day, month, year = date.split('.')
	return False, datetime.date(year=int(year), month=int(month), day=int(day))
