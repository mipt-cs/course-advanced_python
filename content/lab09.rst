Итераторы и сопроцессы
######################

:date: 2020-10-27 09:00
:summary: Итераторы и сопроцессы.
:status: published

.. default-role:: code

.. role:: python(code)
   :language: python

.. contents::

Jupyter-notebook
----------------

`ссылка`_

.. _`ссылка`: /advanced_python/extra/lab9/Coroutine.ipynb

Итерируемые объекты
-------------------

В прошлой работе была подробно рассмотрена концепция генераторов --
функций, имеющих выражение ``yield``. Эти функции имеют возможность
приостанавливать свое выполнение и возвращать промежуточное значение.
Также был рассмотрен цикл for, который может инициализировать итрератор,
вызвав функцию iter(), а также получать следующее значение при помощи
вызова next().

Однако, иногда, итератор может быть более сложным, и невозможно описать
процесс итерации при помощи только одной функции. Таким образом
итерируемым объектом может быть класс. Для того, чтобы класс являлся
итерируемым объектом, у него должны были быть определены методы. Это
методы ``__iter__``, ``__next__``. Первый метод вызывается функцией
``iter()`` и возвращает итерируемый объект, второй метод возвращает
следующее значение и вызывается функцией ``next()``.

При этом, метод ``iter()`` может возвращать, другой объект по которому
можно итерироваться. Это может использоваться для сохранения текущего
состояния объекта на момент итерирования.

Кроме того, в объектах коллекциях можно получать элемент по индексу при
помощи метода ``__getitem__``.

Реализуем все эти возможности на примере односвязного списка.

.. code:: python

    class Node:
        def __init__(self, value, nxt=None):
            self.value = value
            self.nxt = nxt

        def get_value(self):
            return self.value

        def get_next(self):
            return self.nxt

    class LinkedList:
        def __init__(self):
            self.start = None
            self.length = 0
            self.last = None

        def add(self, value):
            elem = Node(value)
            if self.start is None:
                self.start = elem
                self.last = elem
            else:
                self.last.nxt = elem
                self.last = elem
            self.length += 1

        def __len__(self):
            return self.length

        def __getitem__(self, idx):
            if idx >= self.length:
                raise IndexError("Index out of range")
            current = self.start
            for i in range(idx):
                current = current.get_next()
            return current.get_value()

        def __iter__(self):
            self.__curr = self.start
            return self

        def __next__(self):
            if self.__curr is None:
                raise StopIteration()
            val = self.__curr.get_value()
            self.__curr = self.__curr.get_next()
            return val

.. code:: python

    lst = LinkedList()
    for i in range(10):
        lst.add(i*i)

    for i in lst:
        print(i)


.. parsed-literal::

    0
    1
    4
    9
    16
    25
    36
    49
    64
    81


При подобном подходе изменения в процессе итерации по основному объекту
приведут к изменению и при итерации. Для сохранения состояния объекта на
момент начала итерации, в методе ``__iter__`` необходимо
инициализировать объект, хранящий это состояние, по которому также можно
осуществлять итерирование.

Упражнение 1
============

Проверьте, возможно ли изменить список в процессе итерирования.

Упражнение 2
============

Реализуйте класс ``BinTree`` двоичного дерева, итерирование по которму
происходит в порядке обхода в глубину.

Упражнение 3
============

Одним из важнейших применений генераторов является загрузка наборов
данных "на лету", без необходимости загрузки в память всего набора.
Попробуйте решить похожую задачу.

Скачайте `архив`_, и разархивируйте его в отдельную папку в вашей рабочей
папке.

.. _`архив`: /advanced_python/extra/lab9/sample.zip

Вам необходимо создать класс ``TextLoader``, который принимает в
инициализаторе адрес папки. Метод ``__len__`` должен возвращать
количество текстов в папке. метод ``__getitem__`` загружает текст,
приводит его к нижнему регистру и убирает знаки препинания, при
итерировании возвращаются нормализованные тексты, аналогично методу
``__getitem__``.

Сопрограммы
-----------

Хотя это и является одной из самых мощных и интересных концепций,
реализованных в языке Python, в большинстве курсов им уделяется довольно
мало времени.

Рассмотрим ситуацию: есть социальная сеть, и один из ее пользователей в
какой-то мопмент запрашивает у сервера, например, страницу другого
пользователя. Для получения этой информации, сервер, в свою очередь,
подгружает информацию с диска, формирует страницу с результатом и отдает
ее обратно пользователю. При этом, операция чтения данных с диска
занимает довольно большое количество времени. В это время поток
выполнения программы простаивает, ожидая, когда же данные наконец
загрузятся в его память. И это было бы не страшно, если бы в сети
одновременно сидело мало пользователей, которые, скорее всего, не будут
делать запросы к серверу одновременно. Но если система
высоконагруженная, то подобные простои становятся недопустимы. Это время
можно было бы использовать, чтобы система могла сформировать следующий
запрос к диску или базе данных. Для этого надо переключить поток
выполнения на другую задачу, которая будет обрабатывать запрос от
другого пользователя. Затем, когда следующая задача будет в режиме
ожидания, управление будет преключено на первую, которая к тому моменту
закончит операцию чтения с диска. Аналогично можно поступить с обменом
данными с несколькими пользователями. После отправки пакета одному из
них, можно не дожидаясь ответа переключить управление на работу с другим
клиентом.

Технически сопроцессы являются такими же генераторами и также используют
синтаксис ключевого слова ``yield``. Для передачи управления в сопроцесс
из основной программы используется метод ``send``. Рассмотрим пример
сопроцесса.

.. code:: python

    def print_coroutine():
        x = "start"
        while True:
            x = yield x
            print("Got value", x)

    coroutine = print_coroutine()
    print(next(coroutine))
    for i in range(10):
        print(coroutine.send(i))


.. parsed-literal::

    start
    Got value 0
    0
    Got value 1
    1
    Got value 2
    2
    Got value 3
    3
    Got value 4
    4
    Got value 5
    5
    Got value 6
    6
    Got value 7
    7
    Got value 8
    8
    Got value 9
    9


При инициализации сопрограммы вызывается функция ``next``, которая
возвращает управление в основную программу в момент первого вызова
``yield``. Метод ``send`` позволяет передать значение и поток выполнения
в сопрограмму. Сопрограмма выполняется до появления следующего ключевого
слова в коде, а полученное значение возвращается в основную программу.

Процесс выполнения внутри сопрограммы можно контролировать при помощи
исключений. Для вызова исключения внутри сопроцесса используется метод
``throw(Exception, value)``. При этом стоит помнить, что если подобные
вызовы возвращают значение при помощи ``yield``, то для перехода к
следующей ключевой точке необходимо выполнить метод ``next``.

Остановить выполнение сопрограммы можно при помощи метода ``close``.

Основной поток, занимающийся переключением между сопрограммами, мы будем
называть *планировщиком задач* (*scheduler*)

.. code:: python

    class PrintCurrent(Exception):
        pass

    class PrintSum(Exception):
        pass

    def sum_coroutine():
        print("Starting coroutine")
        s = 0
        try:
            while True:
                try:
                    x = yield
                    s += x
                except PrintCurrent:
                    yield x
                except PrintSum:
                    yield s
        finally:
            print("Stop coroutine")

    coroutine = sum_coroutine()
    next(coroutine)
    for i in range(12):
        coroutine.send(i)
        if i%2 == 0:
            print("Current element:", coroutine.throw(PrintCurrent))
            next(coroutine)
        if i%3 == 0:
            print("Current sum:", coroutine.throw(PrintSum))
            next(coroutine)

    print()
    print(coroutine.throw(PrintCurrent))
    next(coroutine)

    print(coroutine.throw(PrintSum))
    next(coroutine)

    coroutine.close()


.. parsed-literal::

    Starting coroutine
    Current element: 0
    Current sum: 0
    Current element: 2
    Current sum: 6
    Current element: 4
    Current element: 6
    Current sum: 21
    Current element: 8
    Current sum: 45
    Current element: 10

    11
    66
    Stop coroutine


Упражнение 4
============

От некоторого устройства в режиме реального времени приходят данные.
Необходимо написать сопрограмму, которая вычисляет среднее, дисперсию, а
также количество элементов в переданном наборе данных с устройства.
Результаты работы сопрограмма должна выдавать при отправке
соответствующих сигналов.

``yield from``
--------------

Как уже было сказано, генераторы (в том числе сопрограммы) могут
использоваться для контроля потока выполнения программы. Пранировщик
задач распределяет ресурсы, запуская задачу, которая ожидает выполнения,
не допуская простоев. Таким образом реализуется асинхронное выполнение
программ.

Однако, иногда в процессе итерирования, может возникнуть ситуация, в
которй необходимо запустить итерацию внутри сопроцесса и передать
управление из внутреннего процесса в планировщик задач. Для этого
используется конструкция ``yield from``.

.. code:: python

    def generator1():
        for i in range(5):
            yield f"Generator 1: {i}"

    def generator2():
        for i in range(5):
            yield f"Generator 2: {i}"

    def generator():
        yield from generator1()
        yield from generator2()

    for i in generator():
        print(i)


.. parsed-literal::

    Generator 1: 0
    Generator 1: 1
    Generator 1: 2
    Generator 1: 3
    Generator 1: 4
    Generator 2: 0
    Generator 2: 1
    Generator 2: 2
    Generator 2: 3
    Generator 2: 4


Это же можно осуществить не только с генераторами, но и с сопрограммами.
Исключения которые создаются в методе ``throw`` автоматически
пробрасываются через ``yield from``.

.. code:: python

    class Terminate(Exception):
        pass

    def inner_coroutine():
        print("Inner coroutine started")
        try:
            while True:
                try:
                    x = yield
                    print(f"Inner: {x}")
                except Terminate:
                    break
        finally:
            print("Inner coroutine finished")

    def outer_coroutine():
        print("Outer coroutine started")
        try:
            x = yield
            print(f"Outer: {x}")
            x = yield
            print(f"Outer: {x}")

            yield from inner_coroutine()

            x = yield
            print(f"Outer: {x}")
        finally:
            print("Outer coroutine finished")

.. code:: python

    try:
        coroutine = outer_coroutine()
        next(coroutine)
        coroutine.send(1)
        coroutine.send(2)
        coroutine.send(3)
        coroutine.send(4)
        coroutine.send(5)
        coroutine.throw(Terminate)
        coroutine.send(6)
    except:
        pass


.. parsed-literal::

    Outer coroutine started
    Outer: 1
    Outer: 2
    Inner coroutine started
    Inner: 3
    Inner: 4
    Inner: 5
    Inner coroutine finished
    Outer: 6
    Outer coroutine finished


Упражнение 5
============

Представьте, что у вас настроено взаимодействие с сервером, от которого
приходят пакеты, содержащие сообщения от различных клиентов. Обработка
каждого из клиентов должна идти в отдельном потоке.

Реализуйте:

1) Корутина ``connect_user`` принимает данные авторизации от
   пользователя, открывает файл с названием .txt и создает на его основе
   корутину ``write_to_file``

2) Корутина ``write_to_file(f_obj)`` записывает переданное планировщиком
   задач сообщение пользователя, которые записываются в файловый объект,
   переданный в качестве аргумента при генерации. Также принимает и
   обрабатывает сигнал об окончании соединения и выходит из сопрограммы.

3) Планировщик задач, распределяющий задачи по сопроцессам на каждого
   пользователя.

.. code:: python

    def user_connection(username):
        import random
        for i in range(random.randint(10, 20)):
            yield f"{username} message{i}"

    def establish_connection(auth=True):
        import random
        id = f"{random.randint(0,100000000):010}"
        if auth:
            yield f"auth {id}"
        yield from user_connection(id)
        if auth:
            yield f"disconnect {id}"

Пример данных, приходящих от авторизованного пользователя:

.. code:: python

    for i in establish_connection(): print(i)


.. parsed-literal::

    auth 0081575115
    0081575115 message0
    0081575115 message1
    0081575115 message2
    0081575115 message3
    0081575115 message4
    0081575115 message5
    0081575115 message6
    disconnect 0081575115


Пример данных, приходящих от неавторизованного пользователя:

.. code:: python

    for i in establish_connection(False): print(i)


.. parsed-literal::

    0015354373 message0
    0015354373 message1
    0015354373 message2
    0015354373 message3
    0015354373 message4
    0015354373 message5
    0015354373 message6
    0015354373 message7
    0015354373 message8
    0015354373 message9
    0015354373 message10
    0015354373 message11
    0015354373 message12


Данные от неавторизованных или разлогиненных пользователей
обрабатываться не должны.

.. code:: python

    def connection():
        import random
        connections = [establish_connection(True) for i in range(10)]
        connections.append(establish_connection(False))
        connections.append(establish_connection(False))
        while len(connections):
            conn = random.choice(connections)
            try:
                yield next(conn)
            except StopIteration:
                del connections[connections.index(conn)]

Пример сообщения, которое надо обработать, можно получить, выполнив следующий код.

.. code:: python

    for i in connection():
        print(i)
