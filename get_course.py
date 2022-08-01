import xml.etree.ElementTree as ET
from datetime import datetime
import requests


def get_course():
    CB_URL = 'https://www.cbr-xml-daily.ru/daily_json.js' # Формирование url для запроса курса из цб
    response = requests.get(CB_URL).json()
    course = response['Valute']['USD']['Value'] # получение курса
    return round(course, 2)


