Паттерны проектирования. Введение
#################################

:date: 2018-11-19 18:00
:summary: Паттерны проектирования. Абстрактный класс, Singleton, Adapter
:status: published
:published: yes

.. default-role:: code

.. contents:: Содержание


.. table_of_contest

Паттерны проектирования
=======================

При проектировании больших приложений, очень удобно использовать уже существующие паттерны проектирования, а не изобретать каждый раз велосипед.

Паттерн (шаблон) проектирования (от англ. design pattern) — повторяемая архитектурная конструкция, представляющая собой решение проблемы проектирования в рамках некоторого часто возникающего контекста.

Как и где применять паттерн — целиком и полностью Ваша ответственность. В данном уроке мы познакомимся с некоторыми из них. Стоит отметить, что паттерны проектирования пришли в программирование из архитектуры, где они не получили широкого распространения. Все паттерны делятся на несколько групп:

#. Основные шаблоны
#. Порождающие шаблоны — шаблоны, абстрагирующие процесс инстанцирования.
#. Структурные шаблоны — определяют различные сложные структуры, изменяющие интерфейс существующих объектов или его реализацию, позволяя облегчить разработку и оптимизировать программу.
#. Поведенческие шаблоны — определяют взаимодействие между объектами, увеличивая их гибкость.


Абстрактные методы
------------------
Перед переходом к первому шаблону, поговорим об абстрактных методах и классах.

Абстрактный метод — метод класса, не имеющий реализацию, но обязательный к реализации в классах-наследниках.

Абстрактный класс — класс, который не предполагает создание экземпляров данного класса. Обычно такой класс содержит абстрактные методы.

Для работы с абстрактными методами и классами используется библиотека ``abc``.

Рассмотрим пример:

.. code-block:: python

    from abc import ABC, abstractmethod
    
    class A(ABC):               # Говорим, что A - абстрактный класс: нельзя создавать его экземпляры
                                # и все его абстрактные методы должны быть определены в наследниках
        @abstractmethod
        def do_something(self):
            pass
    
    class B(A):                 # Создадим класс В - потомок А, но не определим do_something
    
        def do_something_else(self):
            print("I am class B")
    
    class C(A):                 # Создадим класс C - потомок А, и определим do_something
    
        def do_something(self):
            print("I am class С")
    
    
    # Попытаемся создать экземпляры каждого из классов, и вызвать do_something
    
    try:
        print("Пытаюсь создать A")
        a = A()
        a.do_something()
    except:
        print("Не могу создать A")
    
    try:
        print("Пытаюсь создать B")
        b = B()
        b.do_something()
    except:
        print("Не могу создать B")
    
    try:
        print("Пытаюсь создать C")
        c = C()
        c.do_something()
    except:
        print("Не могу создать C")

Выводом данной программы будет:

.. code-block:: text

    Пытаюсь создать A
    Не могу создать A
    Пытаюсь создать B
    Не могу создать B
    Пытаюсь создать C
    I am class С

Как Вы можете видеть: Питон не позволяет создать экземпляры классов A(абстрактный класс) и B(класс, без реализации do_something)

Упражнение №1
~~~~~~~~~~~~~

Для классов ``A``, ``B`` и ``С`` из `файла`__ создайте базовый — абстрактный класс Base(ABC). Наследуйте его классами A, B C и проверьте работу их работу.

.. __: {filename}/code/lab12/abs_class.py

Паттерн Singleton
-----------------

Паттерн Singleton — порождающий паттерн. Подразумевает класс, который будет существовать только в одном экземпляре. Фактически Паттерн singleton является своего рода безопасной заменой использованию глобальных переменных.

Паттерн singleton подразумевает использование статических методов(переменных), которые и будут, собственно хранить информацию, был ли уже создан объект данного класса.

Примеры создания Singleton-а:

**Используя декоратор**

.. code-block:: python

    def singleton(cls):
        instances = {}
        def getinstance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return getinstance

    @singleton
    class MyClass(BaseClass):
        pass

**Используя Singleton, как базовый класс**

.. code-block:: python

    class Singleton(object):
        _instance = None
        def __new__(cls, *args, **kwargs):
            if not isinstance(cls._instance, cls):
                cls._instance = object.__new__(cls, *args, **kwargs)
            return cls._instance

    class MyClass(Singleton, BaseClass):
        pass

Пример использования (вариант декоратора):

.. code-block:: python

   def singleton(cls):
        instances = {}
        def getinstance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return getinstance

    @singleton
    class A_CLS:
        def __init__(self):
            self.data = 1

    a = A_CLS()
    print('data =', a.data)
    a.data = 13
    print('data =', a.data)
    b = A_CLS()
    print('data =', b.data)

Результат работы

.. code-block:: text

    data = 1
    data = 13
    data = 13

В конце работы, программа выглядит так:

.. image:: {filename}/images/lab12/prog_graph.png

Паттерн адаптер
---------------

Паттерн **адаптер** — структурный шаблон. Предназначен для обеспечения совместимости объекта системе. По своему принципу подобен переходнику: например у вас есть *объект* (ноутбук, рассчитанный на подключение к американской розетке) и *система* (европейская розетка с элестричеством). Тогда — для присоединения *объекта* к *системе* необходим **адаптер** (переходник с европейской розетки на американскую).

Пример использования:

.. code-block:: python

    import re
    from abc import ABC, abstractmethod

    _text = '''
    Design Patterns: Elements of Reusable Object-Oriented Software is a software
    engineering book describing software design patterns. The book's authors are
    Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides with a foreword by
    Grady Booch. The book is divided into two parts, with the first two chapters
    exploring the capabilities and pitfalls of object-oriented programming, and
    the remaining chapters describing 23 classic software design patterns. The
    book includes examples in C++ and Smalltalk.
    It has been influential to the field of software engineering and is regarded
    as an important source for object-oriented design theory and practice. More
    than 500,000 copies have been sold in English and in 13 other languages.
    The authors are often referred to as the Gang of Four (GoF).
    '''

    class System:
        ''' Класс, представляющий систему '''
        def __init__(self, text):
            tmp = re.sub(r'\W', ' ', text.lower())
            tmp = re.sub(r' +', ' ', tmp).strip()
            self.text = tmp

        def get_processed_text(self, processor):
            ''' Метод, требующий на вход класс-обработчик '''
            result = processor.process_text(self.text) # Вызов метода обработчика
            print('\n'.join(map(str, result))) # печать результата

    class TextProcessor(ABC):
        ''' Абстрактный интерфейс обработчика '''
        @abstractmethod
        def process_text(self, text):
            ''' Здесь должен быть обработчик '''
            pass
        
    class WordCounter:
        ''' Обработчик, несовместимый с основной системой '''
        def count_words(self, text):
            ''' Считает сколько раз встретилось каждое слово текста'''
            self.__words = dict()
            for word in text.split():
                self.__words[word] = self.__words.get(word, 0) + 1

        def get_count(self, word):
            ''' Возвращает количество вхождений '''
            return self.__words.get(word, 0)

        def get_all_words(self):
            ''' Возвращает копию всего словоря слов '''
            return self.__words.copy()

    class WordCounterAdapter(TextProcessor):
        ''' Адаптер к обработчику '''
        def __init__(self, adaptee):
            ''' В конструкторе указывается, к какому объекту следует подключить адаптер '''
            self.adaptee = adaptee

        def process_text(self, text):
            ''' Реализация интерфейса обработчика, требуемого системой.'''
            self.adaptee.count_words(text)
            words = self.adaptee.get_all_words().keys()
            return sorted(words,
                          key = lambda x: self.adaptee.get_count(x),
                          reverse = True)

    # Создаём систему
    system = System(_text)
    # Создаём объект - "считатель слов" 
    counter = WordCounter()
    # Подключаем адаптер к обекту
    adapter = WordCounterAdapter(counter)
    # Запускаем обработчик в системе, через адаптер
    system.get_processed_text(adapter)

Упражнение №2
~~~~~~~~~~~~~
Вам нужно написать адаптер, который позволил бы использовать найденный вами класс совместно с вашей системой.

Интерфейс класса выглядит следующим образом:

.. code-block:: python

    class Light:
        def __init__(self, dim):
            self.dim = dim
            self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
            self.lights = []
            self.obstacles = []
            
        def set_dim(self, dim):
            self.dim = dim
            self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        
        def set_lights(self, lights):
            self.lights = lights
            self.generate_lights()
        
        def set_obstacles(self, obstacles):
            self.obstacles = obstacles
            self.generate_lights()
            
        def generate_lights(self):
            return self.grid.copy()

Интерфейс системы выглядит следующим образом:

.. code-block:: python

    class System:
        def __init__(self):
            self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
            self.map[5][7] = 1 # Источники света
            self.map[5][2] = -1 # Стены
        
        def get_lightening(self, light_mapper):
            self.lightmap = light_mapper.lighten(self.map)

Класс ``Light`` создает в методе ``__init__`` поле заданного размера.
За размер поля отвечает параметр, представляющий из себя кортеж из 2 чисел.
Элемент ``dim[1]`` отвечает за высоту карты, ``dim[0]`` за ее ширину.
Метод ``set_lights`` устанавливает массив источников света с заданными координатами
и просчитывает освещение. Метод ``set_obstacles`` устанавливает препятствия
аналогичным образом. Положение элементов задается списком кортежей.
В каждом элементе кортежа хранятся 2 значения: ``elem[0]`` -- координата
по ширине карты и ``elem[1]`` — координата по высоте соответственно.
Метод ``generate_lights`` рассчитывает освещенность с учетом источников и препятствий.

Вам необходимо написать адаптер MappingAdapter. Прототип класса вам дан в качестве исходного кода.

для проверки кода используйте (ссылка работает только из локали МФТИ):

.. code-block:: bash

    wget -qO - --post-file=<filename> http://10.55.169.100:5000/