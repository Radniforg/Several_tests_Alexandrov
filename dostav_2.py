import psycopg2

# сколько заказов в феврале 2021 года сделали клиенты, которые сделали свой первый заказ в январе?
# заказы опять считаем только выполненные и по дате завершения


def database_search(dbname='dostavista', user='postgres', password='Grof240192#', host='localhost', text=0):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    with conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM orders WHERE finish_dt < '2021-01-01' "
                    "AND status = 'completed' ")
        before = []
        for row in cur:
            before.append(row)
        cur.execute("SELECT * FROM orders WHERE finish_dt > '2020-12-31' "
                    "AND finish_dt < '2021-02-01' AND status = 'completed' ")
        january = []
        for row in cur:
            january.append(row)
        cur.execute("SELECT * FROM orders WHERE finish_dt >= '2021-02-01' "
                    "AND finish_dt <= '2021-03-01' AND status = 'completed' ")
        february = []
        for row in cur:
            february.append(row)
        cur.close()
    old_clients = []
    for row in before:
        if row[2] not in old_clients:
            old_clients.append(row[2])
    # print(f'old clients: {old_clients}')
    new_clients = []
    for row in january:
        if row[2] not in old_clients:
            new_clients.append(row[2])
    # print(f'new clients: {new_clients}')
    clients = []
    new_client_orders = 0
    for row in february:
        # if row[2] not in old_clients and row[2] in new_clients and row[2] not in clients:
        #     clients.append(row[2])
        if row[2] not in old_clients and row[2] in new_clients:
            new_client_orders += 1
    if text != 0:
        with open('report_test_2.txt', 'w', encoding='UTF-8') as port:
            port.write(f'Количество новых заказов в феврале 2021 года от клиентов, которые сделали '
                       f'свой первый заказ в январе: {new_client_orders}')
    return new_client_orders


print(f'Количество новых заказов в феврале 2021 года от клиентов, которые сделали '
      f'свой первый заказ в январе: {database_search(text=1)}')
