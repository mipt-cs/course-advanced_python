
Многопоточность в питоне. Threads, Processes.
#############################################

:date: 2019-02-16 13:00
:summary: Многопоточность в питоне
:status: published
:published: yes

.. default-role:: code

.. contents:: Содержание


.. role:: python(code)
   :language: python


Процесс и Поток
===============

Процесс — экземпляр программы во время выполнения, независимый объект, которому выделены системные ресурсы (например, процессорное время и память). Каждый процесс выполняется в отдельном адресном пространстве: один процесс не может получить доступ к переменным и структурам данных другого. Если процесс хочет получить доступ к чужим ресурсам, необходимо использовать межпроцессное взаимодействие. Это могут быть конвейеры, файлы, каналы связи между компьютерами и многое другое.

Поток (поток выполнения, thread) - единица обработки, исполнение которой
может быть назначено ядром операционной системы. Исполняющаяся
последовательность инструкций внутри процесса.

Поток использует то же самое пространства стека, что и процесс, а множество потоков совместно используют данные своих состояний. Как правило, каждый поток может работать (читать и писать) с одной и той же областью памяти, в отличие от процессов, которые не могут просто так получить доступ к памяти другого процесса. У каждого потока есть собственные регистры и собственный стек, но другие потоки могут их использовать.

Поток также называют "легковестным процессом". Потоки одного процесса в отличие от процессов имеют множество разделяемых (shared) ресурсов.

.. image:: http://www.cs.miami.edu/home/visser/Courses/CSC322-09S/Content/UNIXProgramming/Threads.JPG
   :width: 500
   :align: center
   :alt: Sharing data between threads

Несколько потоков выполнения могут существовать в рамках одного и того
же процесса и совместно использовать его ресурсы.

-  одно ядро процессора в один момент времени может исполнять только
   один тред
-  треды одного процесса могут исполняться физически одновременно (на
   разных ядрах)
-  бессмысленно порождать вычислительных тредов больше, чем у вас есть
   ядер

threading
=========

Global lock (GIL)
-----------------

CPython (самая популярная реализация интерпретатора питона) был
реализован с максимальной простотой и имеет потокобезопасный механизм -
GIL (Global Interpreter Lock).

.. image:: https://uwpce-pythoncert.github.io/SystemDevelopment/_images/gil.png
   :width: 500
   :align: center
   :alt: GIL visualisation

Благодаря этому Lock'у интерпретатор питона может исполнять лишь одну
команду в один момент времени (single threading). По этой причине,
создание несколько потоков не приведет к их одновременному исполнению на
разных ядрах процессора (как было бы, к примеру, на си), тем не менее, потоки могут быть полезны и в python.

.. code:: python

    # модуль питона для работы с потоками
    import threading

Рассмотрим простой пример программы, создающей потоки:

.. code:: python

    import threading
    import sys
    
    def thread_job(number):
        print('Hello {}'.format(number))
        sys.stdout.flush()
    
    def run_threads(count):
        thread_job(0)
        threads = [
            threading.Thread(target=thread_job, args=(i,))
            for i in range(1, count + 1)
        ]
        for thread in threads:
            thread.start()  # каждый поток должен быть запущен
        for thread in threads:
            thread.join()  # дожидаемся исполнения всех потоков
    
    run_threads(4)


Упражнение №1
-------------

Запустите следующий код. В чем проблема данного кода? Всегда ли counter
= 10 после исполнения кода программы?

.. code:: python

    counter = 0
    
    def thread_job():
        global counter
        old_counter = counter
        counter = old_counter + 1
        print('{} '.format(counter), end='')
    
    threads = [threading.Thread(target=thread_job) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    counter


Демонстрация "проблемности" кода:

.. code:: python

    import random
    import time
    
    counter = 0
    def thread_job():
        global counter
        old_counter = counter
        time.sleep(random.randint(0, 1))
        counter = old_counter + 1
        print('{} '.format(counter), end='')
    
    threads = [threading.Thread(target=thread_job) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    counter


Почему так происходит?


Одно из возможных решений (не самое аккуратное):

.. code:: python

    counter = 0
    
    def thread_job(lock):
        lock.acquire() # mutex
        global counter
        counter += 1
        print('{} '.format(counter), end='')
        sys.stdout.flush()
        lock.release()
    
    lock = threading.Lock()
    threads = [
        threading.Thread(target=thread_job, args=(lock,))
        for i in range(10)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    counter

Решение лучше (с with):

.. code:: python

    counter = 0
    
    def thread_job(lock):
        with lock:
            global counter
            counter += 1
            print('{} '.format(counter), end='')
            sys.stdout.flush()
    
    lock = threading.Lock()
    threads = [
        threading.Thread(target=thread_job, args=(lock,))
        for i in range(10)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    counter


Лучшее решение. Используя queue (очереди) на счет и вывод на экран:

.. code:: python

    import threading
    import queue
    
    class Counter:
        def __init__(self, value):
            self.value = value
    
    def printer(printing_queue):
        while True:
            value = printing_queue.get()
            print(value)
            printing_queue.task_done()
    
    def calculator(counter, calculation_queue, printing_queue):
        while True:
            delta = calculation_queue.get()
            counter.value += delta
            printing_queue.put(counter.value)
            calculation_queue.task_done()
    
    def delta_generator(calculation_queue):
        calculation_queue.put(1)
    
    # Main
    printing_queue = queue.Queue()
    printer_daemon = threading.Thread(
        target=printer,
        args=(printing_queue,),
        daemon=True
    )
    printer_daemon.start()
    
    counter = Counter(0)
    calculation_queue = queue.Queue()
    calculator_daemon = threading.Thread(
        target=calculator,
        args=(counter, calculation_queue, printing_queue),
        daemon=True
    )
    calculator_daemon.start()
    
    workers = [
        threading.Thread(target=delta_generator, args=(calculation_queue,))
        for _ in range(10)
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    
    calculation_queue.join()
    printing_queue.join()


-  ошибки в многопоточном коде - одни из самых неприятных
-  модуль queue позволяет на порядок меньше думать и ошибаться, это
   самый pythonic способ писать многопоточный код


Упражнение №2
-------------

Написать программу, которая будет находить сумму чисел массива с
использованием N тредов. Запустить с разным параметром N.
Убедиться, что несмотря на увеличение N, ускорения подсчета не происходит - влияние GIL (Lock) на исполнение.
**Вычисления** распараллеливать бессмысленно.

Тем не менее, существуют сценарии, при которых использование потоков оправдано!

Упражнение №3
-------------

Запустите на исполнение. Объясните, почему получаем ускорение (в отличие
от предыдущего примера)

При отсутствии доступа к интернету укажите доступные адреса urls ниже.
К примеру:
http://cs.mipt.ru/advanced_python/lessons/lab1.html
http://cs.mipt.ru/advanced_python/lessons/lab2.html
и т.д.

.. code:: python

    import urllib.request
    
    urls = [
        'https://www.yandex.ru', 'https://www.google.com',
        'https://habrahabr.ru', 'https://www.python.org',
        'https://isocpp.org',
    ]
    
    def read_url(url):
        with urllib.request.urlopen(url) as u:
            return u.read()

.. code:: python

    %%timeit
    for url in urls:
        read_url(url)

Треды очень уместны, если в коде есть блокирующие операции (ввод-вывод,
сетевые взаимодействия). Также, удобно разбивать логические
процессы по тредам (анимация, графический интерфейс, и тд),
хоть и не всегда это может привести к ускорению.

Рассмотрим действительно полезный сценарий использования модуля **threading**.

Задача №1
---------

Иногда бывает нужно узнать доступность набора ip адресов. Неэффективный
вариант представлен ниже.

Реализуйте то же самое, но используя threading.

.. code:: python

    import os, re
    
    received_packages = re.compile(r"(\d) received")
    status = ("no response", "alive but losses", "alive")
    
    for suffix in range(20, 30):
        ip = "192.168.178."+str(suffix)
        ping_out = os.popen("ping -q -c2 "+ip, "r")  # получение вердикта
        print("... pinging ", ip)
        while True:
            line = ping_out.readline()
            if not line:
                break
            n_received = received_packages.findall(line)
            if n_received:
                print(ip + ": " + status[int(n_received[0])])


multiprocessing
===============

Модуль для работы с процессами. Создание, управление и т. д.

Как мы убедились ранее, GIL не позволяет использовать одному процессу использовать мощности всей
системы (исполнять несколько потоков одновременно на нескольких ядрах).
Но можно создать несколько процессов и каждый будет исполняться на своем
ядре.

.. code:: python

    import multiprocessing

Интерфейс (api) строится аналогично threading. Модуль позволяет полностью
использовать мощности многоядерных процессоров.

Но нужно понимать, что создание новых процессов более затратно по времени, чем
создание новых потоков.

Упражнение №4
-------------

Запустите код. Объясните почему так происходит: LIST - пуст.

.. code:: python

    import multiprocessing
    
    LIST = []
    
    def worker():
        LIST.append('item')
        
    processes = [
        multiprocessing.Process(target=worker)
        for _ in range(5)
    ]
    
    for p in processes:
        p.start()
    for p in processes:
        p.join()
        
    LIST


Как организовать общение между процессами:

.. code:: python

    from multiprocessing import Process, Queue
    
    def f(q):
        q.put([42, None, 'hello'])
    
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    p.join()
    print(q.get())


Использование очередей позволяет улучшить читаемость кода и уменьшить количество ошибок.
Всегда старайтесь использовать очереди при многопоточном/многопроцессорном программировании.

Пример, демонстрирующий взаимодействие процессов.

Каждый из процессов записывает в очередь случайную строку. Результат
выводится на экран:

.. code:: python

    import multiprocessing as mp
    import random
    import string
    
    random.seed(123)
    
    # Define an output queue
    output = mp.Queue()
    
    # define a example function
    def rand_string(length, output):
        """ Generates a random string of numbers, lower- and uppercase chars. """
        rand_str = ''.join(random.choice(
                            string.ascii_lowercase
                            + string.ascii_uppercase
                            + string.digits)
                       for i in range(length))
        output.put(rand_str)
    
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=rand_string, args=(5, output)) for x in range(4)]
    
    # Run processes
    for p in processes:
        p.start()
    
    # Exit the completed processes
    for p in processes:
        p.join()
    
    # Get process results from the output queue
    results = [output.get() for p in processes]
    
    print(results)

Класс Pool в multiprocessing
----------------------------

Класс Pool - удобный механизм распараллеливания выполнения функций,
распределения входных данных по процессам и т. д.

Наиболее интересные функции: \* Pool.apply \* Pool.map \*
Pool.apply\_async \* Pool.map\_async

apply, map работают аналогично питоновским built-in apply, map.

Как работает Pool можно понять на примере:

.. code:: python

    def cube(x):
        return x**3
    
    pool = mp.Pool(processes=4)  # создаем пул из 4 процессов
    # в apply можно передать несколько аргументов
    results = [pool.apply(cube, args=(x,)) for x in range(1,7)]  # раскидываем числа от 1 до 7 по 4 процессам
    print(results)
    
    pool = mp.Pool(processes=4)
    # то же самое, но с map. разбивает итерируемый объект (range(1,7)) на chunks и раскидывает аргументы по процессам
    results = pool.map(cube, range(1,7))
    print(results)


map, apply - блокирующие вызовы. Главная программа будет заблокирована,
пока процесс не выполнит работу.

map\_async, apply\_async - неблокирующие. При их вызове, они сразу
возвращают управление в главную программу (возвращают ApplyResult как
результат). Метод get() объекта ApplyResult блокирует основной поток,
пока функция не будет выполнена.

.. code:: python

    pool = mp.Pool(processes=4)
    results = [pool.apply_async(cube, args=(x,)) for x in range(1,7)]
    output = [p.get() for p in results]
    print(output)


Сравнение производительности программы на вычисление, используя multiprocessing
-------------------------------------------------------------------------------

Kernel Density Estimation (Ядерная оценка плотности)

**Задача ставится следующим образом**:

Существуют объекты (samples) в пространстве распределенные по некоторому
закону. Наша задача оценить плотность вероятности в заданной точке

Оценим плотность вероятности методом окна Парзена.

.. code:: python

    import numpy as np
    
    def parzen_estimation(x_samples, point_x, h):
        """
        Implementation of a hypercube kernel for Parzen-window estimation.
    
        Keyword arguments:
            x_sample:training sample, 'd x 1'-dimensional numpy array
            x: point x for density estimation, 'd x 1'-dimensional numpy array
            h: window width
    
        Returns the predicted pdf as float.
    
        """
        k_n = 0
        for row in x_samples:
            x_i = (point_x - row[:,np.newaxis]) / (h)
            for row in x_i:
                if np.abs(row) > (1/2):
                    break
            else:
                k_n += 1
        return (k_n / len(x_samples)) / (h**point_x.shape[1])

Пример использования (окно: 0.1):

.. code:: python

    X_inside = np.array([[0,0,0],[0.2,0.2,0.2],[0.1, -0.1, -0.3]])
    
    X_outside = np.array([[-1.2,0.3,-0.3],[0.8,-0.82,-0.9],[1, 0.6, -0.7],
                          [0.8,0.7,0.2],[0.7,-0.8,-0.45],[-0.3, 0.6, 0.9],
                          [0.7,-0.6,-0.8]])
    
    point_x = np.array([[0],[0],[0]])
    X_all = np.vstack((X_inside,X_outside))
    
    print('p(x) =', parzen_estimation(X_all, point_x, h=1))

Сгенерируем данные:

.. code:: python

    import numpy as np
    
    np.random.seed(123)
    
    # Generate random 2D-patterns
    mu_vec = np.array([0,0])
    cov_mat = np.array([[1,0],[0,1]])
    x_2Dgauss = np.random.multivariate_normal(mu_vec, cov_mat, 10000)

Вопрос заключается в том, какой размер окна выбрать для лучшего
приближения. Изменим функцию parzen\_estimation, чтобы она возвращала
дополнительно размер окна:

.. code:: python

    def parzen_estimation(x_samples, point_x, h):
        k_n = 0
        for row in x_samples:
            x_i = (point_x - row[:,np.newaxis]) / (h)
            for row in x_i:
                if np.abs(row) > (1/2):
                    break
            else:
                k_n += 1
        return (h, (k_n / len(x_samples)) / (h**point_x.shape[1]))

Однопоточный алгоритм вычисления для нескольких окон:

.. code:: python

    def serial(samples, x, widths):
        return [parzen_estimation(samples, x, w) for w in widths]

Упражнение №5
-------------

Написать многопоточный вариант, используя Pool.apply\_async.

.. code:: python

    def multiprocess(processes, samples, x, widths):
        # TODO:
        results = ...
        return results

Запустить и посмотрим на результаты

.. code:: python

    point_x = np.array([[0],[0]])
    widths = np.linspace(1.0, 1.2, 100)

.. code:: python

    import timeit
    
    mu_vec = np.array([0,0])
    cov_mat = np.array([[1,0],[0,1]])
    n = 10000
    
    x_2Dgauss = np.random.multivariate_normal(mu_vec, cov_mat, n)
    
    benchmarks = []
    
    benchmarks.append(timeit.Timer('serial(x_2Dgauss, point_x, widths)',
                'from __main__ import serial, x_2Dgauss, point_x, widths').timeit(number=1))
    
    benchmarks.append(timeit.Timer('multiprocess(2, x_2Dgauss, point_x, widths)',
                'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))
    
    benchmarks.append(timeit.Timer('multiprocess(4, x_2Dgauss, point_x, widths)',
                'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))

Упражнение №6
-------------

отобразить benchmarks на графике (matplotlib.pyplot)

При написании программ с использованием модуля **multiprocessing** нужно
помнить, что:

-  передача данных между процессами - это дорого
-  если задача легкая, а данные тяжелые, то возможно лучше ничего не
   параллелить
-  нет ограничения в виде GIL, можно легко параллелить тяжелые
   независимые задачи
