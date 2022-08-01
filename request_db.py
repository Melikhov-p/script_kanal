import psycopg2


def request_db_get(request):
    conn = psycopg2.connect(dbname='kanal_db', user='USERNAME', password='', host='localhost', connect_timeout=5)  # Подключение к БД

    cursor = conn.cursor()

    cursor.execute(request)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def request_db_post(request):
    conn = psycopg2.connect(dbname='kanal_db', user='USERNAME', password='', host='localhost', connect_timeout=5)  # Подключение к БД

    cursor = conn.cursor()

    cursor.execute(request)
    conn.commit()
    cursor.close()
    conn.close()
    return 0
