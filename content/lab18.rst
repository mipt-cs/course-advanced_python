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
СУБД SQLite. Сегодня мы будем использовать SQLite библиотеку прямо из Python. Для этих целей есть стандартная библиотека
sqlite3. По возможности рекомендую ознакомится с ее `официальной документацией`__.

.. __: https://docs.python.org/3/library/sqlite3.html

Соответствие типов данных
-------------------------

SQLite и Python имеют достаточно простое преобразование между типами:

+ NULL ⟷ None
+ INTEGER ⟷ int
+ REAL ⟷ float
+ TEXT ⟷ str
+ BLOB ⟷ bytes

Common practice
---------------

В этой части будут рассмотрены основные принципы работы с библиотекой. За полным списком функций и методов и их
аргументов обращайтесь к документации.

Для работы с БД сначала необходимо создать объект `Connection`. Создается он при помощи функции `connect`, которой
необходимо передать путь до файла БД или `:memory:` для создания БД непосредственно в RAM.

.. code-block:: python

    import sqlite3
    conn = sqlite3.connect("my_data.db")

Когда соединение создано, можно работать с БД. Для этого используется специальный объект `Cursor`, получит который
можно методом `Connection.cursor()`. При помощи метода `Cursor.execute()` курсор исполняет написанный на языке SQL
запрос. Следует помнить, что запросы на изменение БД носят временный характер. Для сохранения изменений необходимо
использовать `Connection.commit()`, а для отката изменений `Connection.rollback()`.  По завершении работы с БД не
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

+ `fetchone()` — возвращает следующую строку из результата
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
методами класса `Cursor`: `execute()`, `executemany()`, `executescript()`. Эти методы возвращают курсор.

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
даже если подставляется одно значение. Для именованных параметров используется словарь.

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

В рассмотренных ранее примерах все изменения необходимо коммитить. Однако есть возможность применять эти изменения
автоматически. Первый вариант - использовать `executescript()`. Этот метод принимает один аргумент — строку с
полноценным SQL скриптом — и выполняет записанные в ней запросы. Не забывайте про `;` в конце каждого запроса в скрипте.

.. code-block:: python

    import sqlite3

    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript("""
        create table person(
            firstname,
            lastname,
            age
        );

        create table book(
            title,
            author,
            draft
        );

        insert into book(title, author, draft)
        values (
            'Dirk Gently''s Holistic Detective Agency',
            'Douglas Adams',
            1987
        );
        """)
    con.close()


Второй вариант — контекстный менеджер. Использование соединения в контекстном менеджере позволяет автоматически
коммитить изменения в случае успеха и откатывать в случае ошибки.

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect(":memory:")
    con.execute("create table person (id integer primary key, firstname varchar unique)")

    # Successful, conn.commit() is called automatically afterwards
    with conn:
        conn.execute("insert into person(firstname) values (?)", ("Joe",))

    # conn.rollback() is called after the with block finishes with an exception, the
    # exception is still raised and must be caught
    try:
        with conn:
            conn.execute("insert into person(firstname) values (?)", ("Joe",))
    except sqlite3.IntegrityError:
        print("couldn't add Joe twice")

    # Connection object used as context manager only commits or rollbacks transactions,
    # so the connection object should be closed manually
    conn.close()

Последнее, что надо рассмотреть, это возможность получать результаты `SELECT` в произвольном виде. По умолчанию, каждая
строка представлена кортежем. Однако это представление можно поменять. Для этого используется атрибут соединения
`row_factory`, которому можно присвоить функцию следующего вида:

.. code-block:: python

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

Здесь `cursor.description` возвращает список названий столбцов. Каждый столбец характеризуется кортежем из 7 элементов,
имя в нулевом элементе.

При необходимости, такая функция может создавать объекты пользовательского класса. Библиотека sqlite3 для удобства
содержит класс `Row`. `Row` в основном ведет себя как кортеж, но при этом дополнительно поддерживает обращение по
именам столбцов. Перепишем пример для `SELECT` с использованием этого класса.

.. code-block:: python

    import sqlite3

    conn = sqlite3.connect("my_data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM stocks WHERE symbol='RHAT'")
    r = c.fetchone()

    print(r.keys())
    for key in r.keys():
        print(r[key])

    conn.close()

Упражнение
----------

Используя базу данных с предыдущего занятия, напишите консольное приложение для работы с ней.
Ваше приложение должно поддерживать команды:

1. Вывести список книг
2. Вывести список читателей
3. Добавить книгу.
4. Добавить читателя.
5. Выдать книгу читателю
6. Принять книгу.

По желанию можно дополнительно добавить поддержку произвольных запросов.
