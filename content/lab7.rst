Асинхронное программирование. Библиотека asyncio.
#################################################

:date: 2019-10-28 09:00
:summary: Тема 6. Часть 2. Работа с асинхронными операциями.
:status: draft

.. default-role:: code

.. role:: python(code)
   :language: python

.. contents::

Ключевые определения
====================

-  Concurrency (конкурентность) — две или более задачи могут
   запускаться, выполняться и завершаться в перекрывающиеся периоды
   времени (наиболее общее понятие)
-  Parallel execution (параллелизм) — исполнение нескольких задач
   одновременно, например, при помощи многоядерного процессора
-  Multithreading (многопоточность) — один из способов реализации
   конкурентности путем выделения абстракции "рабочего потока" (возможна
   и на многоядерных, и на одноядерных процессорах)
-  Asynchrony (асинхронность) — возникновение событий, которые
   происходят одновременно с выполнением программы, без блокировки
   программы для ожидания результатов

Важно понимать разницу между параллелизмом и конкурентностью!

Параллелизм и конкурентность
============================

Выделим 2 типа операций:

-  CPU-bound — связаны с ограничениями на центральный процессор. Программа могла бы работать быстрее, если бы процессор работал быстрее.
-  IO-bound — связаны со скоростью работы I/O системы. Чем быстрее устройство, на котором происходит чтение/запись файла, тем быстрее на нем будут выполняться I/O операции.

.. image:: https://camo.githubusercontent.com/b059a5a2eeb507e0e5188e90d2e171d1ec0b1313/68747470733a2f2f626c6f672d6173736574732e726973696e67737461636b2e636f6d2f323031362f4170722f6e6f6e5f6173796e635f626c6f636b696e675f6f7065726174696f6e735f6578616d706c655f696e5f6e6f64655f6865726f2d313435393835363835383139342e706e67
   :width: 500
   :align: center
   :alt: CPU-bound vs IO-bound

Пример длительной I/O операции:

.. code:: python

    with open('large_file.txt') as f:
        # blocks until OS reads all the data
        data = f.read()

Чтение из большого файла может занимать несколько секунд, но эта
операция блокирующая, хотя процессор мог бы в это время совершать другую
полезную работу. Процессор "простаивает" пока не произойдет чтение всего
файла.

Еще один пример (мы ждем, пока не получим ответ с сайта, хотя могли бы в
это время выполнять полезную работу и продолжить исполнение этого кода
как только получили бы ответ):

.. code:: python

    import requests

    # blocks until site returns response
    response = requests.get('http://very.slow.site')

Асинхронные операции и обратные вызовы
======================================

Асинхронные операции чтения/записи позволяют программе продолжать выполнение, не дожидаясь результата их исполнения.
Как только такая операция завершается, вызывается исполнение функции обратного вызова.
Это написанная вами функция, в которой можно реализовать необходимую логику.

.. code:: python

    # функция, отвечающая за обработку ответа
    def handle_response(response):
        print('\n{:.70}...'.format(response.body))

    # создание объекта для общения с сетью
    http_client = AsyncHTTPClient()

    # неблокирующий вызов функции!
    # после вызова функции fetch будет выполняться следующий за этой строчкой код без ожидания получения ответа
    # ответ с сайта будет обработан функцией handle_response (так называемым callback'ом)
    http_client.fetch('http://yandex.ru', callback=handle_response)

Проблема данного подхода заключается в том, что внутри одной callback
функции может быть вызвана другая и т.д. Такой код становится трудно
читаем.

Корутины и asyncio
==================

Корутина (coroutine) - подпрограмма (функция), которая может начинаться и завершаться в неопределенный момент времени.
Корутины описываются синтаксисом async/await.

.. code:: python

    import asyncio

    async def main():
        print('hello')
        await asyncio.sleep(1)
        print('world')

    loop = asyncio.get_event_loop()
    # Blocking call which returns when the main() coroutine is done
    loop.run_until_complete(main())
    loop.close()

Рассмотрим несколько способов работы с корутинами:

+ Запуск через функцию run_until_complete() (пример выше).
+ Ожидание корутины (инструкция await).

Следующий пример напечатает “hello” после ожидания в 1 секунду, а затем напечатает “world” после ожидания в 2 секунды:

.. code:: python

    import asyncio
    import time

    async def say_after(delay, what):
        await asyncio.sleep(delay)
        print(what)

    async def main():
        print(f"started at {time.strftime('%X')}")

        await say_after(1, 'hello')
        await say_after(2, 'world')

        print(f"finished at {time.strftime('%X')}")

    loop = asyncio.get_event_loop()
    # Blocking call which returns when the main() coroutine is done
    loop.run_until_complete(main())
    loop.close()

+ Создание тасков через loop.create_task().

.. code:: python

    import asyncio
    import time

    async def say_after(delay, what):
        await asyncio.sleep(delay)
        print(what)

    loop = asyncio.get_event_loop()
    # Ожидание завершения обоих операций должно занять около 2х секунд
    print(f"started at {time.strftime('%X')}")
    loop.run_until_complete(asyncio.gather(
        say_after(1, 'hello'),
        say_after(2, 'world')
    ))
    print(f"finished at {time.strftime('%X')}")
    loop.close()

asyncio абстракции
------------------

Выделим понятия, которыми оперирует asyncio:

+  **цикл событий** (event loop) по большей части всего лишь управляет
   выполнением различных задач: регистрирует поступление и запускает в
   подходящий момент
+  **корутины** — специальные функции, описанные с async def, от которых ожидают (await),
   что они будут отдавать управление обратно в цикл событий.
   Необходимо, чтобы они были запущены именно через цикл событий
+  **футуры** — объекты, в которых хранится текущий результат выполнения
   какой-либо задачи. Это может быть информация о том, что задача ещё не
   обработана или уже полученный результат; а может быть вообще
   исключение

C помощью синтаксиса **await** мы определяем места, где можно
переключиться на другие ожидающие выполнения задачи.

Рассмотрим подробнее следующий пример:

.. code:: python

    import asyncio

    async def compute(a, b):
        print('Compute...')
        await asyncio.sleep(1.0)
        return a + b

    async def print_sum(a, b):
        result = await compute(a, b)
        print('{} + {} = {}'.format(a, b, result))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_sum(1, 2))
    loop.close()

.. image:: https://camo.githubusercontent.com/de86a2c33affd5101ddc77b69a274823e643bda2/687474703a2f2f6e746f6c6c2e6f72672f7374617469632f696d616765732f74756c69705f636f726f2e706e67
   :width: 700
   :align: center
   :alt: Visualisation of the example compute/print_sum

Начиная с версии Python 3.7 синтаксис работы с библиотекой был упрощен.
Подробнее про библиотеку можно узнать здесь_.

.. _здесь: https://docs.python.org/3/library/asyncio.html

Упражнение №1
-------------

Что будет напечатано и почему?

.. code:: python

    import asyncio

    async def factorial(name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({i})...")
            await asyncio.sleep(1)
            f *= i
        print(f"Task {name}: factorial({number}) = {f}")

    async def main():
        await asyncio.gather(
            factorial("A", 2),
            factorial("B", 3),
            factorial("C", 4),
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

Waiting & timeouts
==================

Иногда выполнение операции может занять очень длительное время.
Например, вы до сих пор не получили ответ от сервера.
В случае отсутствия соединения ваша операция может висеть бесконечно долго.
В таком случае на асинхронные операции имеет смысл выставлять timeout.
Пример на выставление timeout:

.. code:: python

    import asyncio

    async def eternity():
        # Sleep for one hour
        await asyncio.sleep(3600)
        print('yay!')

    async def main():
        # Wait for at most 1 second
        try:
            await asyncio.wait_for(eternity(), timeout=1.0)
        except asyncio.TimeoutError:
            print('timeout!')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

async with
==========

Асинхронный контекстный менеджер - это контекстный менджер, который
умеет приостанавливать выполнение в методах входа и выхода:
\_\ *aenter\_*\ (), \_\ *aexit\_*\ ()

.. code:: python

    lock = asyncio.Lock()

    # ... later
    await lock.acquire()
    try:
        # access shared state
    finally:
        lock.release()

.. code:: python

    lock = asyncio.Lock()

    # ... later
    async with lock:
        # access shared state

aiohttp
=======

Рядом с asyncio создано огромное количество асинхронных модулей для
решения всевозможных задач. **aiohttp** - лишь одна из них. Это
асинхронный HTTP Клиент/Сервер

В следующем примере получаем содержимое страницы google.com:
(при отсутствии доступа в интернет, cs.mipt.ru)

.. code:: python

    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get('http://google.com') as resp:
            text = await resp.text()
            print('{:.70}...'.format(text))

Реализация простого сервера:

.. code:: python

    from aiohttp import web

    async def handle(request):
        name = request.match_info.get('name', 'Anonymous')
        text = 'Hello, ' + name
        # ...
        # здесь идет некоторая дополнительная логика с async/await
        #
        return web.Response(text=text)

    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])

    web.run_app(app)


Упражнение №2
-------------

Узнать свой IP адрес. Есть куча сервисов, которые позволяют узнать ваш
ip. Но на момент запуска программы вы не знаете какой из сервисов
доступен. Вместо того, чтобы опрашивать каждый из этих сервисов
последовательно, можно запустить все запросы конкурентно и выбрать
первый успешный.

При отсутствии доступа в интернет симулируйте задачу через cs.mipt.ru (к примеру, получение страниц вида cs.mipt.ru/advanced_python/lessons/labX.html и выбора первой, в которой количество символов больше, чем N)

Потребуется **asyncio.wait()** и параметр **return\_when**

.. code:: python

    from collections import namedtuple
    import time
    import asyncio
    from concurrent.futures import FIRST_COMPLETED
    import aiohttp

    Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

    SERVICES = (
        Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
        Service('ip-api', 'http://ip-api.com/json', 'query')
    )

    async def fetch_ip(service):
        # получение ip


    async def asynchronous():
        # TODO:
        # создание футур для сервисов
        # используйте FIRST_COMPLETED

    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(asynchronous())

Для правильной реализации немного теории.

Возможные состояния футур: - ожидание (pending) - выполнение (running) -
выполнено (done) - отменено (cancelled)

Когда футура находится в состояние **done**, у неё можно получить
результат выполнения. В состояниях **pending** и **running** такая
операция приведёт к исключению **InvalidStateError**, а в случае
**canelled** будет **CancelledError**, и наконец, если исключение
произошло в самой корутине, оно будет сгенерировано снова (также, как
это сделано при вызове exception).

Узнать состояние футуры с помощью методов **done**, **cancelled** или
**running**, но не забывайте, что в случае **done** вызов **result**
может вернуть как ожидаемый результат, так и исключение, которое
возникло в процессе работы.

Для отмены выполнения футуры есть метод **cancel** (он то нам и
требуется для корректного завершения работы)

Теперь мы изучили достаточно для того, чтобы написать простого чат бота,
который будет делать что-то полезное.

Упражнение №3
-------------

Напишите телеграм бота, который будет на сообщение присылать
соответствующее изображение

-  установить aiogram 1.4 - асинхронная обертка над api телеграмма
-  поговорить с @FatherBot, создать бота и запомнить выданный токен
-  В рф нужно использовать впн или прокси (в сети есть огромное
   количество списков адресов)
-  разобраться с примером эхо бота ниже
-  написать требуемый функционал (картинки можно запрашивать через поиск
   яндекса или гугла, существуют готовые api, можно написать и
   самостоятельно)

.. code:: python

    from aiogram import Bot, types
    from aiogram.dispatcher import Dispatcher
    from aiogram.utils import executor

    PROXY_URL = 'socks5://xxx.xxx.xxx.xxx' # вставить здесь подходящий ip

    secret_token = 'XXX'  # строка вида: 123456789:ABCDEFGHJABCDEFGHJABCDEFGHJABCDEFGHJ

    bot = Bot(token=secret_token, proxy=PROXY_URL)
    dp = Dispatcher(bot)


    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
        await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


    @dp.message_handler()
    async def echo(message: types.Message):
        await message.reply(message.text)


    if __name__ == '__main__':
        executor.start_polling(dp)
