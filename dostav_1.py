import psycopg2
import datetime
import sys

# Текст задачи:
# за каждый день января 2021 года (по дате завершения заказа = finish_dt) вывести следующие данные:
# client_payments -- сколько денег клиенты заплатили за заказы
# revenue         -- сколько денег осталось после всех выплат курьерам
# AOR             -- average order revenue (доход в расчете на выполненный заказ)
# деньги считаем только за выполненные (completed) заказы


def database_search_test_1(dbname='dostavista', user='postgres', password='Grof240192#', host='localhost', text=0):
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
    report = {}
    while start_date <= end_date:
        if start_date in date_check.keys():
            revenue = date_check[start_date][0] - date_check[start_date][1]
            report.update({start_date: {'client_payment': date_check[start_date][0],
                                        'revenue': revenue,
                                        'AOR': revenue/date_check[start_date][2]}})
        else:
            report.update({start_date: {'client_payment': 0,
                                        'revenue': 0,
                                        'AOR': 0}})
        start_date += delta
    if text != 0:
        with open('report_test_1.txt', 'w', encoding='UTF-8') as port:
            for key in sorted(report.keys()):
                port.write(f'Date - {key}\n'
                           f'client payments - {report[key]["client_payment"]}\n'
                           f'revenue - {report[key]["revenue"]}\n'
                           f'AOR - {report[key]["AOR"]}\n\n')
    return report

    # давай распишем логику
    # крутить по 20 раз массив с данными нельзя - их может быть 100500 штук
    # значит нужно один раз рассортировать массив. Сделать словарь с ключом-датой. Как?
    # Все просто: если существует в словаре ключ с данной штукой - плюсуем, если не существует - минусуем.
    # В задании не сказано чекнуть базу на ошибки, поэтому принимаем, что база корректная.
    # логично не делать десять проверок, а сразу сделать словарь + кортеж


def entry():
    cycle = 0
    while cycle == 0:
        print(f'Если вы хотите ввести параметры БД в этом окне - отправьте 1\n'
              f'Если вы уже ввели параметры в функцию внутри кода - нажмите 0\n'
              f'Если вы хотите завершить программу, чтобы внести параметры в код - нажмите 2\n'
              f'Введите: ')
        answer = int(input())
        if answer == 0 or answer == 1:
            cycle = 1
        elif answer == 2:
            sys.exit()
        else:
            print(f'Введено некорректное значение, повторите ввод\n')
    if answer == 0:
        print('Хорошо')
        return None
    else:
        print(f'Введите имя базы данных:')
        dbname = input()
        print(f'Введите имя пользователя:')
        user = input()
        print(f'Введите пароль:')
        password = input()
        cycle_2 = 0
        while cycle_2 == 0:
            print(f'Параметр host отличается от localhost? Y/N')
            host_answer = input()
            if host_answer.upper() == 'Y' or host_answer.upper() == 'N':
                cycle_2 = 1
            else:
                print(f'Введено некорректное значение, повторите ввод\n')
        if host_answer.upper() == 'N':
            host = 'localhost'
        else:
            print(f'Пожалуйста, введите значение host:')
            host = input()
        cycle_3 = 0
        while cycle_3 == 0:
            print(f'Хотите ли вы получить отчет в том числе в виде текстового файла? Y/N')
            text_answer = input()
            if text_answer.upper() == 'Y' or text_answer.upper() == 'N':
                cycle_3 = 1
            else:
                print(f'Введено некорректное значение, повторите ввод\n')
        if text_answer.upper() == 'N':
            text = 0
        else:
            text = 1
    return_dictionary = {'dbname': dbname, 'user': user,
                         'password': password, 'host': host, 'text': text}
    return return_dictionary


if __name__ == "__main__":
    db_info = entry()
    if db_info:
        report = database_search_test_1(dbname=db_info['dbname'],
                                        user=db_info['user'],
                                        password=db_info['password'],
                                        host=db_info['host'],
                                        text=db_info['text'])
    else:
        report = database_search_test_1()
    for key in report.keys():
        print(f'Дата - {key}:\n'
              f'client payments - {report[key]["client_payment"]}\n'
              f'revenue - {report[key]["revenue"]}\n'
              f'AOR - {report[key]["AOR"]}\n')

# (dbname='dostavista', user='postgres', password='Grof240192#', host='localhost', text=0)