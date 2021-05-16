# Dostavista_test
Тестовые задания для Dostavista

Во всех скриптах идет подключение к базе данных postgres через psycopg2.
В данный момент во всех скриптах в качестве пароля к БД стоит '', а user - 'postgres'.

В во всех скриптах (по одному на каждое тестовое задание) реализована функция ввода параметров БД внутри скрипта

В репозитории 4 скрипта:
1) dsdb.py - скрипт для создания локальной базы данных. Вспомогательный скрипт, если базы не существует.
   К сожалению, моя база данных не поддерживала тип данных unsigned и tinyint, поэтому первый я опустил, а второй заменил на smallint:
   исходя из условий задачи, эти параметры не имели особого значения
2) dostav_test_1.py - задание №1.
3) dostav_test_2.py - задание №2. Скрипт написан согласно ТЗ, однако если пользователь сделал заказ в январе, а получил доставку в феврале - он не будет считаться как пользователь,
   сделавший свой первый заказ в январе (так как сказано считать по дате завершения). Я нахожу это условие немного нелогичным, 
   и если подразумевалось, что такой пользователь все же будет считаться январским - могу переписать скрипт.
4) dostav_test_3.py - задание №3.

Вспомогательные файлы:
1) cb.csv и orders.csv - файлы для моей небольшой личной бд для проверки
2) cb.json и orders.json - данные, которыми я наполнил бд.
3) dostavista-sql-test-task.txt - файл с заданием.
