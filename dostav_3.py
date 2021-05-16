import psycopg2
import datetime
import pandas as pd
import dostav_1

# для каждого города по дням создания заказа вывести следующие метрики. для заказов созданных в январе 2021:
# - кол-во созданных заказов
# - % отмененных заказов
# - кол-во активных клиентов (активный = тот кто создавал заказы)
# - кол-во заказов выполненных в тот же день
# - медианное время выполнения заказа
# (предполагаем, что запрос выполняется на последней версии postgresql/mysql/mariadb)


def database_search_test_3(dbname='dostavista', user='postgres',
                           password='Grof240192#', host='localhost', text= 0):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    with conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM orders WHERE created_dt < '2021-01-01' ")
        before = []
        for row in cur:
            before.append(row)
        cur.execute("SELECT * FROM orders WHERE created_dt > '2020-12-31' "
                    "AND created_dt < '2021-02-01' ")
        january = []
        for row in cur:
            january.append(row)
        city_list = []
        for row in before:
            if row[1] not in city_list:
                city_list.append(row[1])
        result = {}
        for city in city_list:
            result[city] = {'orders': 0, 'cancelled': 0, 'active': [], 'daily': 0, 'total_time': []}
        limit = datetime.timedelta(days=1)
        for row in january:
            if row[1] not in result.keys():
                result[row[1]] = {'orders': 1, 'cancelled': 0,
                                  'active': [row[2]], 'daily': 0,
                                  'total_time': []}
                if row[5] == 'cancelled':
                    result[row[1]]['cancelled'] = 1
                elif row[5] == 'completed':
                    result[row[1]]['total_time'].append(row[8] - row[4])
                    if row[8] - row[4] < limit:
                        result[row[1]]['daily'] = 1
            else:
                result[row[1]]['orders'] += 1
                if row[5] == 'completed':
                    result[row[1]]['total_time'].append(row[8] - row[4])
                    if row[8] - row[4] < limit:
                        result[row[1]]['daily'] += 1
                elif row[5] == 'cancelled':
                    result[row[1]]['cancelled'] += 1
                if row[2] not in result[row[1]]['active']:
                    result[row[1]]['active'].append(row[2])
        if text != 0:
            port = open('report_test_3.txt', 'w', encoding='UTF-8')
            for key in sorted(result.keys()):
                if result[key]['orders'] != 0:
                    port.write(f'Город {key} за январь 2021:\n '
                               f'Количество созданных заказов: {result[key]["orders"]}\n '
                               f'Процент отмененных заказов: '
                               f'{round(result[key]["cancelled"] / result[key]["orders"] * 100, 0)}%\n '
                               f'Количество активных клиентов: {len(result[key]["active"])}\n '
                               f'Количество выполненных заказов в тот же день: '
                               f'{result[key]["daily"]}\n '
                               f'Медианное время выполнения заказа: '
                               f'{pd.to_timedelta(result[key]["total_time"]).median()}\n\n')
                else:
                    port.write(f'Город {key} за январь 2021:\n'
                               f'Количество созданных заказов: 0\n'
                               f'Процент отмененных заказов: 0.0%\n'
                               f'Количество активных клиентов: 0\n'
                               f'Количество выполненных заказов в тот же день: 0\n'
                               f'Медианное время выполнения заказа: 0\n\n')
        return result


db_info = dostav_1.entry()
if db_info:
    report = database_search_test_3(dbname=db_info['dbname'],
                                    user=db_info['user'],
                                    password=db_info['password'],
                                    host=db_info['host'],
                                    text=db_info['text'])
else:
    report = database_search_test_3(text=1)
for key in sorted(report.keys()):
    if report[key]['orders'] != 0:
        print(f'Город {key} за январь 2021:\n'
              f'Количество созданных заказов: {report[key]["orders"]}\n'
              f'Процент отмененных заказов: '
              f'{report[key]["cancelled"] / report[key]["orders"] * 100}%\n'
              f'Количество активных клиентов: {len(report[key]["active"])}\n'
              f'Количество выполненных заказов в тот же день: '
              f'{report[key]["daily"]}\n'
              f'Медианное время выполнения заказа: '
              f'{pd.to_timedelta(report[key]["total_time"]).median()}')
    else:
        print(f'Город {key} за январь 2021:\n'
              f'Количество созданных заказов: 0\n'
              f'Процент отмененных заказов: 0.0%\n'
              f'Количество активных клиентов: 0\n'
              f'Количество выполненных заказов в тот же день: 0\n'
              f'Медианное время выполнения заказа: 0')
