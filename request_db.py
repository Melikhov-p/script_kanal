import psycopg2


def request_db_get(request):
    conn = psycopg2.connect(dbname='kanal_db', user='pavel', password='', host='localhost', connect_timeout=5)  # Подключение к БД

    cursor = conn.cursor()

    cursor.execute(request)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def request_db_post(request):
    conn = psycopg2.connect(dbname='kanal_db', user='pavel', password='', host='localhost', connect_timeout=5)  # Подключение к БД

    cursor = conn.cursor()

    cursor.execute(request)
    conn.commit()
    cursor.close()
    conn.close()
    return 0

# print(request_db_get('SELECT * from kanal_table WHERE "order"=1120833')[0][4].strftime("%d.%m.%Y"))
