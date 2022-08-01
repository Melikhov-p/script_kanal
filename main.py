from __future__ import print_function

import os.path
import time

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from request_db import request_db_get, request_db_post
from get_course import get_course


def get_service_acc():  # Авторизация сервисного аккаунта google
    creds_json = os.path.join(os.path.dirname(__file__), "SECRET_KEY.json")
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


def get_sheet():  # Получение таблицы с данными
    sheet_id = '1qt4QBYRvgzK4cdFAxHsSuVX8mxZsc9XqtTK7SkXn5eQ'
    resp = get_service_acc().spreadsheets().values().batchGet(spreadsheetId=sheet_id, ranges=["Лист1"]).execute()
    return resp['valueRanges'][0]['values'][1:]  # Список со строками таблицы, первый элемент - название колонок


def new_db_record(record): # Создание новой записи в БД
    cost_rub = round(float(record[2]) * get_course(), 2)
    request_db_post(f'INSERT INTO public.kanal_table(id, "order", cost_usd, cost_rub, delivery_date) VALUES ({int(record[0])}, {int(record[1])}, {float(record[2])}, {cost_rub}, \'{record[3].replace(".", "/")}\');')
    print("CREATED ", record[1])


def check_records(sheet: list): # Проверка наличия записи из таблицы в БД
    db_orders = []
    for order in request_db_get('SELECT ALL "order" from kanal_table'):
        db_orders.append(order[0])
    for record in sheet:
        if int(record[1]) in db_orders: # Проверка на существование записи из таблицы в БД
            db_order = request_db_get(f'SELECT * from kanal_table WHERE "order"={int(record[1])}')
            cost_rub = round(float(record[2]) * get_course(), 2)
            if int(record[1]) != db_order[0][1] or float(record[2]) != db_order[0][2] or cost_rub != float(db_order[0][3]) or record[3] != str(db_order[0][4].strftime("%d.%m.%Y")): # Проверка на соответствие данных в записи таблицы и БД, если не совпадает - обновляем запись в БД
                request_db_post(f'UPDATE public.kanal_table	SET "order"={int(record[1])}, cost_usd={float(record[2])}, cost_rub={cost_rub}, delivery_date=\'{record[3].replace(".", "/")}\' WHERE "order"={int(record[1])};')
                print('UPDATE ' + record[1])
        else: # Если записи из таблицы нет в БД, создаем новую запись
            new_db_record(record)

def check_deleted_records(sheet_orders: list): # Проверка на записи, удаленные из таблицы, но оставшиеся в БД
    db_orders = request_db_get('SELECT ALL "order" from kanal_table')
    for db_order in db_orders:
        if str(db_order[0]) not in sheet_orders: # Если заказа из БД нет в таблице - удаляем его и из БД
            request_db_post(f'DELETE FROM public.kanal_table WHERE "order"={db_order[0]};')
            print('DELETED ', db_order)

old_sheet = [] # Список для сохранения таблицы
print('START')
while True:
    sheet = get_sheet() # Получение новой таблицы с google sheets
    if old_sheet != sheet: # Сравниваем таблицу со старой, если отличаются, обновляем бд
        sheet_orders = [field[1] for field in sheet]
        try:
            check_records(sheet)
        except Exception as e:
            print(e)
        try:
            check_deleted_records(sheet_orders)
        except Exception as e:
            print(e)
        old_sheet = sheet # Переписываем старую таблицу
    time.sleep(60) # Период проверки данных в таблице
