Обзор модулей python.
###############################

:date: 2018-12-01 23:00
:summary: Обзор модулей python
:status: draft
:published: no

.. default-role:: code

.. contents:: Содержание


.. role:: python(code)
   :language: python


Collections
===========

Модуль содержит расширение стандартных built-in контейнеров питона,
таких как dict, list, set, and tuple

Зачастую ими пользоваться удобней, чем стандартными

defaultdict
-----------

.. code:: ipython3

    from collections import defaultdict
    # Отнаследован от dict, а значит, имеет те же методы

К примеру, нам нужно посчитать частоту чисел в массиве. Используя
словарь, это можно сделать так:

.. code:: ipython3

    elems = [2, 2, 4, 2, 3]
    build_in_dict = dict()
    
    for elem in elems:
        if elem in build_in_dict:
            build_in_dict[elem] += 1
        else:
            build_in_dict[elem] = 1
    
    print(build_in_dict)

Выглядит неаккуратно - 4 строчки занимают очень простую операцию -
добавление элемента. Перепишем, используя defaultdict:

.. code:: ipython3

    dct = defaultdict(int)
    
    for elem in elems:
        dct[elem] += 1
    
    print(dct)

Красиво и просто

defaultdict принимает аргументом фабрику для первого элемента в словаре.
В представленном случае - int. То есть, в строчке

::

    dct[elem] += 1

происходит что-то вроде:

::

    dct[elem] = (int() if elem not in dct else dct[elem]) + 1

.. code:: ipython3

    # По умолчанию, аргумент - None
    dct = defaultdict()
    # И при обращении к несуществующему элементу мы получим KeyError:
    dct[0]

Конечно, можно передать вместо int - list, set или даже свою фабрику

Упражнение 1
~~~~~~~~~~~~

Написать с помощью defaultdict функцию для подсчета количества различных
labels для каждого цвета

.. code:: ipython3

    def count_colors_labels(colors_labels):
        raise NotImplementedError()

.. code:: ipython3

    # format: list of tuples: (color, label)
    elems = [('yellow', 3), ('green', 4), ('green', 4), ('red', 2), ('green', 7), ('yellow', 4)]
    
    # check
    true_answer = {'yellow': 2, 'green': 2, 'red': 1}
    
    assert count_colors_labels(elems) == true_answer

Можем передать функцию:

.. code:: ipython3

    import random
    
    def factory():
        return random.randint(0, 100)
    
    dct = defaultdict(factory)
    
    print(dct[0], dct[1], dct[2], dct[0])
    print(dct)

Не нужно забывать следующую особенность - объекты записываются в
defaultdict, как только мы к ним обращаемся в первый раз

Упражнение 2
~~~~~~~~~~~~

Написать класс, с помощью которого можно создать словарь, который по
умолчанию будет выдавать количество уже заведенных элементов до него

.. code:: ipython3

    class StrangeClass(object):
        pass

.. code:: ipython3

    dct = defaultdict(StrangeClass())
    
    elems = [9, 3, 1, 3, 4, 10]
    
    assert [dct[elem] for elem in elems] == [0, 1, 2, 1, 3, 4]

deque (double-ended queue)
--------------------------

.. code:: ipython3

    from collections import deque

Deques поддерживают **thread-safe**, **memory efficient** добавление и
извлечение элементов с любого края за амортизированный О(1)

Его часто (!) используют как примитив синхронизации потоков из-за
простоты и хорошей читаемости кода

Почему использовать deque вместо list?

.. code:: ipython3

    elems = [1 for _ in range(20000000)]
    delems = deque(elems)
    
    %timeit (elems.pop(0), elems.append(1))
    
    %timeit (delems.popleft(), delems.append(1))

Конструктор принимает итерируемый объект и максимальное количество
элементов (по умолчанию None). При достижении границы, старые элементы
будут удаляться с противоположного конца

.. code:: ipython3

    d = deque(maxlen=2)
    print(d)
    d.extend([1, 2, 3, 4])
    print(d)

Несколько полезных методов:

.. code:: ipython3

    dq = deque([1,2,3,4,1])
    print('elem count: {}'.format(dq.count(1)))
    
    dq.extend([4, 5, 6])
    print(dq)
    
    dq.rotate(-1)
    print(dq)

Упражнение 3
~~~~~~~~~~~~

С помощью deque написать функцию, выдающую последние n строк из файла

.. code:: ipython3

    def tail(filename, n=10):
        raise NotImplementedError()

.. code:: ipython3

    # check with your file
    
    filename = ''
    last_lines = ''
    
    n = 10
    # assert tail(filename, n) == last_lines

Упражнение 4\*
~~~~~~~~~~~~~~

Реализовать свой deque

Counter
-------

Отнаследован от dict. Как следует из названия, хорош, если требуется
что-то посчитать (вообще-то, только **hashable** объекты)

.. code:: ipython3

    from collections import Counter

.. code:: ipython3

    c = Counter()
    print(c)
    
    c = Counter('gallahad')
    print(c)
    
    c = Counter({'red': 4, 'blue': 2})
    print(c)
    
    c = Counter(cats=4, dogs=8)
    print(c)

Можем найти N наиболее встречаемых слов в тексте в 1 строчку!

.. code:: ipython3

    text = '''The rose is red the violet is blue The honey is sweet and so are you'''
    
    Counter(text.split()).most_common(3)

Упражнение 5
~~~~~~~~~~~~

Написать функцию, выводящую наименее встречаемые элементы с помощью
Counter

.. code:: ipython3

    def get_least_common(iterable_obj, n=3):
        raise NotImplementedError()

.. code:: ipython3

    elems = [1,4,3,1,1,8,9,2,8,8,9,9]
    assert get_least_common(elems) == [2, 3, 4]

OrderedDict
-----------

Как следует из названия, словарь, но уже с порядком элементов

.. code:: ipython3

    from collections import OrderedDict

.. code:: ipython3

    data = [(1, 'a'), (3, 'c'), (2, 'b')]
    
    print(dict(data))
    print(OrderedDict(data))

При удалении элементов, порядок сохраняется, но новый элемент
добавляется в конец без учета порядка

Упражнение 6
~~~~~~~~~~~~

Написать класс LastUpdatedOrderedDict. Модификация относительно
OrderedDict в том, чтобы при добавлении уже существующих элементов,
перезаписывать их места в словаре

.. code:: ipython3

    class LastUpdatedOrderedDict(OrderedDict):
        'Store items in the order the keys were last added'

.. code:: ipython3

    lud = LastUpdatedOrderedDict()
    
    elems = ['a', 'b', 'c']
    
    for elem in elems:
        lud[elem] = 1
    
    assert list(lud) == elems
    
    lud['a'] = 1
    
    assert list(lud) == ['b', 'c', 'a']

namedtuple
~~~~~~~~~~

Как следует из названия, именованные tuple, возможность организовать
доступ к элементам через field\_names в конструкторе. **namedtuple**
возвращает класс, поэтому первым аргументом должны передать его имя.
Лучше всего как он работает можно понять на примерах:

.. code:: ipython3

    from collections import namedtuple

.. code:: ipython3

    Point = namedtuple('Point', ['x', 'y'])
    
    p = Point(1, 2)
    print(p)

.. code:: ipython3

    t = [11, 22]
    Point._make(t)

Может быть полезно при чтении csv файлов (конструирование объектов через
соответствие полей и значений:

.. code:: ipython3

    EmployeeRecord = namedtuple('EmployeeRecord', 'name, age')
    
    # imagine, that rows is returned from csv.reader(...):
    rows = [
        ['Name1', 46],
        ['Name2', 24]
    ]
    
    for emp in map(EmployeeRecord._make, rows):
        print(emp.name, emp.age)

Упражнение 7
~~~~~~~~~~~~

Полностью написать функцию, считывающую работников из csv файла.
Использовать модуль csv

.. code:: ipython3

    def read_employees(filename):
        raise NotImplementedError()

Usefull functions from collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Вместе с контейнерами, в collections есть также несколько полезных
функций. К примеру, мы можем узнать, является ли объект итерируемым или
хешируемым:

.. code:: ipython3

    import collections

.. code:: ipython3

    objs = [set([1,2,3]), (1,)]
    
    for obj in objs:
        if isinstance(obj, collections.Hashable):
            print('object of type {} is hashable'.format(type(a)))
        else:
            print('object of type {} is not hashable'.format(type(a)))

Узнать больше:

https://docs.python.org/3/library/collections.html

itertools
=========

itertools - Модуль для "эффективного итерирования"

Лучше всего понять как с ним работать - выполнить простые упражнения

.. code:: ipython3

    import itertools

Упражнение №1
~~~~~~~~~~~~~

Написать функцию, принимающую 2 списка и возвращающую декартово
произведение (использовать itertools.product)

.. code:: ipython3

    def get_cartesian_product(a, b):
        raise RuntimeError("Not implemented")
    
    get_cartesian_product([1, 2], [3, 4]) == [(1, 3), (1, 4), (2, 3), (2, 4)]

Упражнение №2
~~~~~~~~~~~~~

Написать функцию, принимающую строку s и число n и возвращающую
всевозможные перестановки из n символов в s строке в
лексикографическом(!) порядке (использовать itertools.permutations)

.. code:: ipython3

    def get_permutations(s, n):
        raise RuntimeError("Not implemented")
    
    get_permutations("cat", 2) == ["ac", "at", "ca", "ct", "ta", "tc"]

Упражнение №3
~~~~~~~~~~~~~

Реализовать функцию get\_combinations. Должна принимать строку s и число
k и возвращать все возможные комбинации из символов в строке s с длинами
<= k (использовать itertools.combinations)

.. code:: ipython3

    def get_combinations(s, n):
        raise RuntimeError("Not implemented")
    
    get_combinations("cat", 2) == ["a", "c", "t", "ac", "at", "ct"]

Упражнение №4
~~~~~~~~~~~~~

Функция должна принимать строку s и число k и возвращать все возможные
комбинации из символов в строке s с длинами = k с повторениями
(использовать itertools.combinations\_with\_replacement)

.. code:: ipython3

    def get_combinations_with_r(s, n):
        raise RuntimeError("Not implemented")
    
    get_combinations_with_r("cat", 2) == ["aa", "ac", "at", "cc", "ct", "tt"]

Упражнение №5
~~~~~~~~~~~~~

Написать функцию, которая подсчитывает количество подряд идующих
символов в строке (использовать itertools.groupby)

.. code:: ipython3

    def compress_string(s):
        raise RuntimeError("Not implemented")
    
    compress_string('1222311') == [(1, 1), (3, 2), (1, 3), (2, 1)]

Упражнение №6
~~~~~~~~~~~~~

В функцию передается список списков. Нужно вернуть максимум, который
достигает выражение $(a\_1^2 + a\_2^2 + ... + a\_n^2) % m $. Где
:math:`a_i` --- некоторый элемент из :math:`i`-ого списка (использовать
функцию из itertools)

.. code:: ipython3

    def maximize(lists, m):
        raise RuntimeError("Not implemented")
    
    lists = [
        [5, 4],
        [7, 8, 9],
        [5, 7, 8, 9, 10]
    ]
    maximize(lists, m=1000) == 206

В примере = 206, так как это максимум от суммы
:math:`(a_1^2 + a_2^2 + a_3^2) \% 1000`

:math:`a_1 = 5, a_2 = 9, a_3 = 10`

functools
=========

Модуль **functools** используется для высокоуровневых функций, функций,
которые ведут себя как функции или возвращают другие функции

.. code:: ipython3

    import functools

**@functools.lru\_cache(maxsize=128, typed=False)** - позволяет
сохранять результаты maxsize последних вызовов. Очень полезно для
сохранения результатов долгих вычислений.

Поскольку в качестве кэша используется словарь, все аргументы должны
быть хешируемыми

Упражнение 1
~~~~~~~~~~~~

Напишите **не самую лучшую** версию вычисления чисел Фибоначчи (через
рекурсию), только для демонстрации силы lru\_cache.

А теперь запустите ее с достаточно большим n с декоратором и без

**@functools.total\_ordering** - декоратор класса, в котором задан один
или более методов сравнения. Этот декоратор автоматически добавляет все
остальные методы. Класс должен определять один из методов
\_\ *lt\_*\ (), \_\ *le\_*\ (), \_\ *gt\_*\ (), или \_\ *ge\_*\ ().
Кроме того, он должен определять метод \_\ *eq\_*\ ().

Применение:

::

    @total_ordering
    class Student:
        pass

Упражнение 2
~~~~~~~~~~~~

Напишите класс **Student**, в котором будут атрибуты firstname, lastname
и методы \_\ *lt\_*\ (), \_\ *eq\_*\ (). Добавьте декоратор, запустите
код и убедитесь в том, что декоратор работает так, как надо (добавляет
остальные функции сравнения)

С функцией reduce вы уже знакомы (эта built-in функция с 3 питона
доступна во 2 через functools модуль). Поведение аналогично:

**functools.reduce(function, iterable[, initializer])** - берёт два
первых элемента, применяет к ним функцию, берёт значение и третий
элемент, и таким образом сворачивает iterable в одно значение. Если
задан initializer, он помещается в начале последовательности.

Упражнение 3
~~~~~~~~~~~~

Напишите функцию, использующую reduce, которая суммирует все числа в
списке

functools.partial(func, \*args, \*\*keywords) - возвращает
partial-объект (по сути, функцию), который при вызове вызывается как
функция func, но дополнительно передают туда позиционные аргументы args,
и именованные аргументы kwargs. Если другие аргументы передаются при
вызове функции, то позиционные добавляются в конец, а именованные
расширяют и перезаписывают.

Пример:

::

    from functools import partial
    basetwo = partial(int, base=2)
    basetwo.__doc__ = 'Convert base 2 string to an int.'
    print(basetwo('10010'))

Упражнение 4
~~~~~~~~~~~~

С помощью partial и уже готовой функции add создайте функцию add2,
которая принимает один аргумент x и возвращает результат: x+2

.. code:: ipython3

    def add(a, b):
        return a + b

**functools.update\_wrapper(wrapper, wrapped,
assigned=WRAPPER\_ASSIGNMENTS, updated=WRAPPER\_UPDATES)**

Обновляет функцию-оболочку, чтобы она стала похожей на обёрнутую
функцию. assigned - кортеж, указывающий, какие атрибуты исходной функции
копируются в функцию-оболочку (по умолчанию это WRAPPER\_ASSIGNMENTS
(\_*name\_*, \_\ *module\_*, \_\ *annotations\_* и \_\ *doc\_*)).
updated - кортеж, указывающий, какие атрибуты обновляются (по умолчанию
это WRAPPER\_UPDATES (обновляется \_\ *dict\_* функции-оболочки)).

**@functools.wraps(wrapped, assigned=WRAPPER\_ASSIGNMENTS,
updated=WRAPPER\_UPDATES)**

Удобная функция для вызова partial(update\_wrapper, wrapped=wrapped,
assigned=assigned, updated=updated) как декоратора при определении
функции-оболочки. Например:

Все понятнее с примером (мы пытаемся решить проблему с тем, что при
доступе к атрибуту, скажем \_\ *name\_*, мы увидели декоратор, а не
вызываемую функцию):

.. code:: ipython3

    def foo(f):
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    
    @foo
    def bar(x, y):
        return x + y
    
    print(bar(1, 2))
    (bar.__name__)

.. code:: ipython3

    @wraps
    def foo(f):
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    
    @foo
    def bar(x, y):
        return x + y
    
    print(bar(1, 2))
    (bar.__name__)

copy
====

Модуль **copy** - поверхностное и глубокое копирование объектов

.. code:: ipython3

    import copy

В чем проблема?

.. code:: ipython3

    a = [1,2,3]
    b = a
    print(id(b) == id(a))

Но ведь тогда мы можем сделать так:

.. code:: ipython3

    a = [1,2,3]
    b = a.copy()
    
    print(id(b) == id(a))

Да..., но ведь так работает не всегда!

.. code:: ipython3

    class A():
        pass
    
    a = A()
    b = a
    print(id(a) == id(b))
    c = a.copy()
    print(id(c) == id(a))

А теперь модуль copy и функция поверхностного (верхний итератор)
копирования copy:

.. code:: ipython3

    c = copy.copy(a)
    print(id(c) == id(a))

Модуль содержит и функцию глубокого копирования **deepcopy**, которая
проходится по всем объектам рекурсивно и копирует их в новый объект

-  Поверхностная копия создает новый составной объект, и затем (по мере
   возможности) вставляет в него ссылки на объекты, находящиеся в
   оригинале.
-  Глубокая копия создает новый составной объект, и затем рекурсивно
   вставляет в него копии объектов, находящихся в оригинале.

И все таки, что же это значит?

Упражнение 1
~~~~~~~~~~~~

Проверьте работу **copy** и **deepcopy** на вложенных структурах (с
проверкой идентификаторов внутренних структур).

К примеру, вы можете, для начала, создать несколько списков, вложенных в
список и скопировать его сначала **copy**, а затем, **deepcopy**
