sqlite3 в Python
################

:date: 2020-03-12 09:00
:summary: Работа с sqlite3 в Python
:status: draft

.. default-role:: code

.. contents:: Содержание

.. role:: python(code)
   :language: python

Библиотека sqlite3
------------------

На прошлой неделе вы познакомились с реляционными базами данных и языком запросов SQL. Для работы с БД мы использовали
СУБД SQLite. Сегодня мы будем использовать SQLite библиотеку прямо из Python. Для этих целей есть станартная библиотека
sqlite3. По возможности рекомендую ознакомится с ее `официальной документацией`__.

.. __: https://docs.python.org/3/library/sqlite3.html

Соответствие типов данных
-------------------------

SQLite и Python имеют достаточно простое преобразование между типами:

+ NULL ⟷ None
+ INTEGER ⟷ соответint
+ REAL ⟷ float
+ TEXT ⟷ str
+ BLOB ⟷ bytes

Common practice
---------------

В этой части будт рассмотрены основные принципы работы с библиотекой. За описанием функций и методов и их аргументов
обращайтесь к документации или разделу :ref:`SQLite API`.

Для работы с БД сначала необходимо создать объект `Connection`. Создается он при помощи функции `connect`, которой
необходимо передать путь до файла БД или `:memory:` для создания БД непосредственно в RAM.

.. code-block:: python

    import sqlite3
    conn = sqlite3.connect("my_data.db")

Когда соединение создано, можно работать с БД. Для этого используется специальный объект `Cursor`, получит который
можно методом `Connection.cursor()`. При помощи метода `Cursor.execute()` курсор исполняет написанный на языке SQL
запрос. Следует помнить, что запросы на изменение БД носят временный характер. Для сохранения изменений необходимо
использовать `Connection.commit()`, а для отката изменений `Connection.rollback()`.  По завершении рабоыт с БД не
забывайте закрывать соединение.

.. code-block:: python

    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE stocks
                 (date TEXT, trans TEXT, symbol TEXT, qty REAL, price REAL)''')

    # Insert a row of data
    c.execute('''INSERT INTO stocks VALUES ('2006-01-05', 'BUY', 'RHAT', 100, 35.14),
                 ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'IBM', 500, 53.00)''')

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

Запрос `SELECT` несколько отличается. Для получения его результатов необходимо использовать методы

+ `fetchone()` — возвращает следуюшую строку из результата
+ `fetchmany()` — возвращает указанное количество строк
+ `fetchall()` — возвращает все оставшиеся строки

Или использовать курсор как итератор.

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect("my_data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM stocks WHERE symbol='RHAT'")
    print(c.fetchone())

    for row in c.execute("SELECT * FROM stocks ORDER BY price"):
        print(row)

    conn.close()

Однако, работа с курсором напрямую необязательна. Класс `Connection` предоставляет методы-обертки над одноименными
методами класса `Cursor`: `execute()`, `executemany()`, `executescript()`. Что особенно удобно в случае `SELECT`
запроса. Нет необходимости использовать специальные методы курсора (`fetchone()`, `fetchmany()`, `fetchall()`) для
получения результата запроса.

.. code-block:: python

    import sqlite3

    persons = [
        ("Hugo", "Boss"),
        ("Calvin", "Klein")
        ]

    conn = sqlite3.connect(":memory:")

    # Create the table
    conn.execute("create table person(firstname, lastname)")

    # Fill the table
    conn.executemany("insert into person(firstname, lastname) values (?, ?)", persons)

    # Print the table contents
    for row in conn.execute("select firstname, lastname from person"):
        print(row)

    print("I just deleted", conn.execute("delete from person").rowcount, "rows")

    # close is not a shortcut method and it's not called automatically,
    # so the connection object should be closed manually
    conn.close()

Стоит обратить внимание на метод `executemany()`. Данный метод позволяет применить один и тот же запрос для разных
входных данных. Данные подаются в виде объекта-коллекции, итератора или генератора. Подстановки данных выполняюстя при
помощи вопросительных знаков или именованных параметров. В случае вопросительных знаков данные подаются в виде кортежа,
даже если подстваляется одно значение. Для именованных параметрови используется словарь.

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("create table people (name_last, age)")

    who = "Yeltsin"
    age = 72

    # This is the qmark style:
    cur.execute("insert into people values (?, ?)", (who, age))

    # And this is the named style:
    cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})

    print(cur.fetchone())

    conn.close()

.. TODO:
    executescript()
    context manager
    row

SQLite API
----------

Connection
==========

Объекты этого класса поддерживают соединение с файлом БД. Объекты класса `Connection` создются только при помощи
функции `connect()`.

Cursor
======

Row
===

Exception
=========

Упражнения
----------
