import psycopg2
import datetime

# Текст задачи:
# за каждый день января 2021 года (по дате завершения заказа = finish_dt) вывести следующие данные:
# client_payments -- сколько денег клиенты заплатили за заказы
# revenue         -- сколько денег осталось после всех выплат курьерам
# AOR             -- average order revenue (доход в расчете на выполненный заказ)
# деньги считаем только за выполненные (completed) заказы


def database_search(dbname='dostavista', user='postgres', password='Grof240192#', host='localhost'):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    with conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM orders WHERE finish_dt > '2020-12-31' "
                    "AND finish_dt < '2021-02-01' AND status = 'completed' ")
        data = []
        for row in cur:
            data.append(row)
        cur.execute("SELECT * FROM courier_bonuses WHERE date > '2020-12-31' "
                    "AND date < '2021-02-01' ")
        bonus = []
        for row in cur:
            bonus.append(row)
    # Фрагмент обрабатывает полученные данные и делает из них словарь по датам. Работает некорректно,
    # не решает дает возможность посчитать AOR
    print(data)
    print(bonus)
    date_check = {}
    for row in data:
        date_check_keys = date_check.keys()
        current_date = row[8].date()
        print(current_date)
        if current_date not in date_check_keys:
            dict_update = {current_date: (row[3], row[7], 1)}
            # Словарь - дата: сумма заказа, сумма выплат курьеру (без бонуса), количество заказов)
            date_check.update(dict_update)
            print(f'{current_date} - not')
        else:
            payment = date_check[current_date]
            new_client_payment = payment[0]+row[3]
            new_courier_payment = payment[1]+row[7]
            new_order_amount = payment[2] + 1
            # Суммируется сумма, выплаты курьеру, увеличивается число заказов в день
            dict_update = {current_date: (new_client_payment, new_courier_payment, new_order_amount)}
            date_check.update(dict_update)
            print(f'{current_date} - in')
    print(date_check)
    for row in bonus:
        date_check_keys = date_check.keys()
        if row[0] not in date_check_keys:
            print("DATABASE ERROR! COURIER BONUS WITHOUT COMPLETED ORDERS!")
            dict_update = {row[0]: (0, row[2], 1)}
            date_check.update(dict_update)
        else:
            payment = date_check[row[0]]
            new_courier_payment = payment[1]+row[2]
            dict_update = {row[0]: (payment[0], new_courier_payment, payment[2])}
            date_check.update(dict_update)
    print(date_check)
    # Фрагмент вывода данных:
    start_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2021, 1, 31)
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        if start_date in date_check.keys():
            print(f'{start_date} - YES')
        else:
            print(f'{start_date} - NAH')
        start_date += delta

    # давай распишем логику
    # крутить по 20 раз массив с данными нельзя - их может быть 100500 штук
    # значит нужно один раз рассортировать массив. Сделать словарь с ключом-датой. Как?
    # Все просто: если существует в словаре ключ с данной штукой - плюсуем, если не существует - минусуем.
    # В задании не сказано чекнуть базу на ошибки, поэтому принимаем, что база корректная.
    # логично не делать десять проверок, а сразу сделать словарь + кортеж


    # if '2021' in data[0][4]:
    #     print(data[0][4])
    # else:
    #     print('FUck')




database_search()