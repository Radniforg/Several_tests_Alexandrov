import psycopg2
import json
import dostav_1


# вспомогательная функция для заполнения таблицы тестовыми данными.
def unravel(json_name):
    with open(json_name) as datafile:
        read = json.load(datafile)
        tup = ()
        for data_info in read:
            data_tup = ()
            for data in data_info:
                if not data:
                    data = None
                data_tup = data_tup + (data, )
            tup = tup + (data_tup, )
        return tup


# Техническая функция для создания новой базы данных.
def database_creation(dbname='postgres', user='postgres', password='', host='localhost'):
    conn = psycopg2.connect(
            database="postgres", user='postgres', password='', host='localhost')
    conn.autocommit = True
    cursor = conn.cursor()
    # Вставить название базы
    cursor.execute("CREATE DATABASE dostavista")
    print("Database successfully created")
    conn.close()


def table_creation(dbname='dostavista', user='postgres', password='', host='localhost'):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS orders;")
        cur.execute("DROP TABLE IF EXISTS courier_bonuses;")
        cur.execute("DROP TYPE IF EXISTS current_status")
        # Postgres (на котором я тестирую решение задач) не поддерживает unsigned int,
        # поэтому (на данном этапе) я воспользуюсь просто int).
        # То же самое касается tinyint, я буду использовать small int.
        cur.execute("CREATE TYPE current_status AS ENUM('active', 'completed', 'cancelled');")
        cur.execute("CREATE TABLE orders(order_id SERIAL PRIMARY KEY, "
                    "city_id SMALLINT NOT NULL,"
                    "client_id INT NOT NULL,"
                    "client_payment INT NOT NULL,"
                    "created_dt TIMESTAMP NOT NULL,"
                    "status current_status NOT NULL,"
                    "courier_id INT DEFAULT NULL,"
                    "courier_payment INT DEFAULT NULL,"
                    "finish_dt TIMESTAMP DEFAULT NULL);")
        cur.execute("CREATE TABLE courier_bonuses(date DATE NOT NULL,"
                    "courier_id int NOT NULL,"
                    "bonus_amount INT NOT NULL,"
                    "primary key(date, courier_id));")
        cur.close()


def database_many(dbname='dostavista', user='postgres',
                  password='Grof240192#', host='localhost', json='orders.json'):
    data_list = unravel(json)
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    with conn:
        cur = conn.cursor()
        query = "INSERT INTO orders(order_id, city_id, client_id, client_payment, " \
                "created_dt, status, courier_id, courier_payment, finish_dt) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.executemany(query, data_list)
        conn.commit()
        print('Ready')
        cur.close()


db_info = dostav_1.entry()
if db_info:
    table_creation(dbname=db_info['dbname'],
                   user=db_info['user'],
                   password=db_info['password'],
                   host=db_info['host'])
    database_many(dbname=db_info['dbname'],
                  user=db_info['user'],
                  password=db_info['password'],
                  host=db_info['host'],
                  json='orders.json')
    database_many(dbname=db_info['dbname'],
                  user=db_info['user'],
                  password=db_info['password'],
                  host=db_info['host'],
                  json='cb.json')
else:
    database_creation()
    table_creation()
    database_many(json='orders.json')
    database_many(json='cb.json')
