Генераторы и цикл for
#####################

:date: 2019-11-04 09:00
:summary: Тема 7. Часть 1. Генераторы и цикл for.
:status: published
:published: yes

.. default-role:: code

.. role:: python(code)
   :language: python

.. contents::

Цикл ``for``.
-------------

Цикл ``for`` может использоваться для различных целей.

Самый простой пример использования цикла:

.. code:: python

    for i in range(5):
        print(i)


.. parsed-literal::

    0
    1
    2
    3
    4
    

При помощи этого цикла можно итерироваться по любому объекту-коллекции:

.. code:: python

    lst = ["qwerty", 12345, 34.42]
    
    for i in lst:
        print(i)


.. parsed-literal::

    qwerty
    12345
    34.42
    

Но в таком случае встает вопрос, что же общего между объектом-коллекцией
и диапазоном значений? ``range`` является функцией. Попробуем
посмотреть, что эта функция возвращает:

.. code:: python

    a = range(5)
    
    print("object:\n\t", a)
    print("type:\n\t", type(a))
    print("Methods and attributes:\n\t", dir(a))


.. parsed-literal::

    object:
         range(0, 5)
    type:
         <class 'range'>
    Methods and attributes:
         ['__bool__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index', 'start', 'step', 'stop']
    

То есть ``range`` -- это класс и мы вызываем его конструктор. Объект
этого класса является итерируемым, а значит с ним может работать цикл
``for``. Чтобы создать итератор из объекта, воспользуемся функцией
``iter()``:

.. code:: python

    iterator = iter(a)
    
    print("object:\n\t", iterator)
    print("type:\n\t", type(iterator))
    print("Methods and attributes:\n\t", dir(iterator))


.. parsed-literal::

    object:
         <range_iterator object at 0x0000012FA12F9CF0>
    type:
         <class 'range_iterator'>
    Methods and attributes:
         ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__length_hint__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__']
    

Итератор — объект, который знает свое текущее состояние и может
вычислить следующее значение. Такой подход не приводит к созданию
дополнительных больших объектов в памяти и таким образом делает
программу более эффективной. Никакой лишней информации при этом в памяти
не хранится.

Для того, чтобы перейти к следующему состоянию, используется функция
``next()``.

.. code:: python

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))


.. parsed-literal::

    0
    1
    2
    3
    4
    

Но что же происходит, когда мы пытаемся получить следующий объект, но
его не существует?

.. code:: python

    next(iterator)


::


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    <ipython-input-19-4ce711c44abc> in <module>()
    ----> 1 next(iterator)
    

    StopIteration: 


В таком случае выпадает ошибка ``StopIteration``, которая говорит, что
следующий объект получить невозможно. Это и является признаком конца
итерации. На эту ошибку и ориентируется цикл ``for``.

Упражнение 1
============

Вам дана функция на языке python:

::

    def print_map(function, iterable):
        for i in iterable:
            print(function(i))

Требуется переписать данную функцию не используя цикл for. \*\*\*\*

Генераторы
----------

Рассмотрим несколько примеров итерируемых объектов, которые есть в языке
python (кроме ``range``).

**map(function, iterable)**

В начале рассмотрим функцию ``map(func, iterable)``. Эта функция
позволяет применить некоторую другую функцию ``func`` ко всем элементам
другого итерируемого объекта ``iterable``. **Обратите внимание, что
объект-функция передается без круглых скобок**

.. code:: python

    def baz(value):
        return value * value
    
    lst = [1, 2, 3, 4, 5]
    
    for i in map(baz, lst):
        print(i)


.. parsed-literal::

    1
    4
    9
    16
    25
    

**zip(iterable[, iterable, ...])**

Функция ``zip(iterable[, iterable, ...])`` позволяет параллельно
итерироваться по большому количеству итерируемых объектов, получая из
них соответствующие элементы в виде кортежа. Итератор прекращает свою
работу, когда один из переданных объектов закончится.

.. code:: python

    names = ["Alex", "Bob", "Alice", "John", "Ann"]
    age = [25, 17, 34, 24, 42]
    sex = ["M", "M", "F", "M", "F"]
    
    for values in zip(names, age, sex):
        print("name: {:>10} age: {:3} sex: {:2}".format(*values))


.. parsed-literal::

    name:       Alex age:  25 sex: M 
    name:        Bob age:  17 sex: M 
    name:      Alice age:  34 sex: F 
    name:       John age:  24 sex: M 
    name:        Ann age:  42 sex: F 
    

**filter(func, iterable)**

Пробегает по итерируемому объекту и возвращает только те элементы,
которые удовлетворяют условию, описанному в функции ``func``.

.. code:: python

    def bar(x):
        if abs((34-x*x))**0.5 > x:
            return True
        return False
    
    for i in filter(bar, [0, 1, 2, 3, 4, 5]):
        print(i)


.. parsed-literal::

    0
    1
    2
    3
    4
    

**enumerate(iterable, start=0)**

Принимает на вход итерируемый объект и возвращает пары (индекс элемента,
элемент). Индексация начинается со ``start``, который по умолчанию равен 0.

.. code:: python

    names = ["Alex", "Bob", "Alice", "John", "Ann"]
    
    for idx, elem in enumerate(names, 1):
        print("{:02}: {:>7}".format(idx, elem))


.. parsed-literal::

    01:    Alex
    02:     Bob
    03:   Alice
    04:    John
    05:     Ann
    

Кажется, что концепция генерации объектов налету, без предварительного
выделения памяти под целый массив, является довольно удобной и полезной.
Объекты-итераторы могут хранить, например, списки запросов к серверу,
логи системы и другую информацию, которую можно обрабатывать
последовательно. В таком случае, нам хочется научиться создавать
подобные объекты.

Для этих целей может использоваться ключевое слово ``yield``. Функция, в
которой содержится это ключевое слово, становится функцией-генератором.
Из такой функции можно создать объект-итератор. При вызове функции
``next()`` выполнение этой функции дойдет до первого встреченного
ключевого слова ``yield``, после чего, подобно действию ``return``,
управление перейдет основной программе. Поток управления вернется обратно
в функцию при следующем вызове ``next()`` и продолжит выполнение с того
места, на котором остановился ранее.

Рассмотрим, каким образом можно написать свою собственную функцию
``range()``:

.. code:: python

    def my_range(a, b=None, step=1):
        if b is None:
            a, b = 0, a
        _current = a
        while True:
            yield _current
            _next = _current + step
            if (_next - b)*(_current - b) <= 0:
                break
            _current = _next
                
    for i in my_range(5):
        print(i, end = " ")
    print()
    
    for i in my_range(1, 5):
        print(i, end = " ")
    print()
    
    for i in my_range(1, 10, 2):
        print(i, end = " ")
    print()
    
    for i in my_range(10, 0, -3):
        print(i, end = " ")
    print()


.. parsed-literal::

    0 1 2 3 4 
    1 2 3 4 
    1 3 5 7 9 
    10 7 4 1 
    

Упражнение 2
============

Напишите генератор, выводящий первые n чисел Фибоначчи. \*\*\*

Упражнение 3
============

Реализуйте аналог функций zip, map, enumerate. \*\*\*

<table class="docutils align-center">
<colgroup>
<col style="width: 14%">
<col style="width: 14%">
<col style="width: 39%">
<col style="width: 33%">
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Iterator</p></th>
<th class="head"><p>Arguments</p></th>
<th class="head"><p>Results</p></th>
<th class="head"><p>Example</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.count" title="itertools.count"><code class="xref py py-func docutils literal notranslate"><span class="pre">count()</span></code></a></p></td>
<td><p>start, [step]</p></td>
<td><p>start, start+step, start+2*step, …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">count(10)</span> <span class="pre">--&gt;</span> <span class="pre">10</span> <span class="pre">11</span> <span class="pre">12</span> <span class="pre">13</span> <span class="pre">14</span> <span class="pre">...</span></code></p></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.cycle" title="itertools.cycle"><code class="xref py py-func docutils literal notranslate"><span class="pre">cycle()</span></code></a></p></td>
<td><p>p</p></td>
<td><p>p0, p1, … plast, p0, p1, …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">cycle('ABCD')</span> <span class="pre">--&gt;</span> <span class="pre">A</span> <span class="pre">B</span> <span class="pre">C</span> <span class="pre">D</span> <span class="pre">A</span> <span class="pre">B</span> <span class="pre">C</span> <span class="pre">D</span> <span class="pre">...</span></code></p></td>
</tr>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.repeat" title="itertools.repeat"><code class="xref py py-func docutils literal notranslate"><span class="pre">repeat()</span></code></a></p></td>
<td><p>elem [,n]</p></td>
<td><p>elem, elem, elem, … endlessly or up to n times</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">repeat(10,</span> <span class="pre">3)</span> <span class="pre">--&gt;</span> <span class="pre">10</span> <span class="pre">10</span> <span class="pre">10</span></code></p></td>
</tr>
</tbody>
</table>

<table class="docutils align-center">
<colgroup>
<col style="width: 17%">
<col style="width: 17%">
<col style="width: 30%">
<col style="width: 37%">
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Iterator</p></th>
<th class="head"><p>Arguments</p></th>
<th class="head"><p>Results</p></th>
<th class="head"><p>Example</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.accumulate" title="itertools.accumulate"><code class="xref py py-func docutils literal notranslate"><span class="pre">accumulate()</span></code></a></p></td>
<td><p>p [,func]</p></td>
<td><p>p0, p0+p1, p0+p1+p2, …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">accumulate([1,2,3,4,5])</span> <span class="pre">--&gt;</span> <span class="pre">1</span> <span class="pre">3</span> <span class="pre">6</span> <span class="pre">10</span> <span class="pre">15</span></code></p></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.chain" title="itertools.chain"><code class="xref py py-func docutils literal notranslate"><span class="pre">chain()</span></code></a></p></td>
<td><p>p, q, …</p></td>
<td><p>p0, p1, … plast, q0, q1, …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">chain('ABC',</span> <span class="pre">'DEF')</span> <span class="pre">--&gt;</span> <span class="pre">A</span> <span class="pre">B</span> <span class="pre">C</span> <span class="pre">D</span> <span class="pre">E</span> <span class="pre">F</span></code></p></td>
</tr>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.chain.from_iterable" title="itertools.chain.from_iterable"><code class="xref py py-func docutils literal notranslate"><span class="pre">chain.from_iterable()</span></code></a></p></td>
<td><p>iterable</p></td>
<td><p>p0, p1, … plast, q0, q1, …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">chain.from_iterable(['ABC',</span> <span class="pre">'DEF'])</span> <span class="pre">--&gt;</span> <span class="pre">A</span> <span class="pre">B</span> <span class="pre">C</span> <span class="pre">D</span> <span class="pre">E</span> <span class="pre">F</span></code></p></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.compress" title="itertools.compress"><code class="xref py py-func docutils literal notranslate"><span class="pre">compress()</span></code></a></p></td>
<td><p>data, selectors</p></td>
<td><p>(d[0] if s[0]), (d[1] if s[1]), …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">compress('ABCDEF',</span> <span class="pre">[1,0,1,0,1,1])</span> <span class="pre">--&gt;</span> <span class="pre">A</span> <span class="pre">C</span> <span class="pre">E</span> <span class="pre">F</span></code></p></td>
</tr>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.dropwhile" title="itertools.dropwhile"><code class="xref py py-func docutils literal notranslate"><span class="pre">dropwhile()</span></code></a></p></td>
<td><p>pred, seq</p></td>
<td><p>seq[n], seq[n+1], starting when pred fails</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">dropwhile(lambda</span> <span class="pre">x:</span> <span class="pre">x&lt;5,</span> <span class="pre">[1,4,6,4,1])</span> <span class="pre">--&gt;</span> <span class="pre">6</span> <span class="pre">4</span> <span class="pre">1</span></code></p></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.filterfalse" title="itertools.filterfalse"><code class="xref py py-func docutils literal notranslate"><span class="pre">filterfalse()</span></code></a></p></td>
<td><p>pred, seq</p></td>
<td><p>elements of seq where pred(elem) is false</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">filterfalse(lambda</span> <span class="pre">x:</span> <span class="pre">x%2,</span> <span class="pre">range(10))</span> <span class="pre">--&gt;</span> <span class="pre">0</span> <span class="pre">2</span> <span class="pre">4</span> <span class="pre">6</span> <span class="pre">8</span></code></p></td>
</tr>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.groupby" title="itertools.groupby"><code class="xref py py-func docutils literal notranslate"><span class="pre">groupby()</span></code></a></p></td>
<td><p>iterable[, key]</p></td>
<td><p>sub-iterators grouped by value of key(v)</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.islice" title="itertools.islice"><code class="xref py py-func docutils literal notranslate"><span class="pre">islice()</span></code></a></p></td>
<td><p>seq, [start,] stop [, step]</p></td>
<td><p>elements from seq[start:stop:step]</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">islice('ABCDEFG',</span> <span class="pre">2,</span> <span class="pre">None)</span> <span class="pre">--&gt;</span> <span class="pre">C</span> <span class="pre">D</span> <span class="pre">E</span> <span class="pre">F</span> <span class="pre">G</span></code></p></td>
</tr>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.starmap" title="itertools.starmap"><code class="xref py py-func docutils literal notranslate"><span class="pre">starmap()</span></code></a></p></td>
<td><p>func, seq</p></td>
<td><p>func(*seq[0]), func(*seq[1]), …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">starmap(pow,</span> <span class="pre">[(2,5),</span> <span class="pre">(3,2),</span> <span class="pre">(10,3)])</span> <span class="pre">--&gt;</span> <span class="pre">32</span> <span class="pre">9</span> <span class="pre">1000</span></code></p></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.takewhile" title="itertools.takewhile"><code class="xref py py-func docutils literal notranslate"><span class="pre">takewhile()</span></code></a></p></td>
<td><p>pred, seq</p></td>
<td><p>seq[0], seq[1], until pred fails</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">takewhile(lambda</span> <span class="pre">x:</span> <span class="pre">x&lt;5,</span> <span class="pre">[1,4,6,4,1])</span> <span class="pre">--&gt;</span> <span class="pre">1</span> <span class="pre">4</span></code></p></td>
</tr>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.tee" title="itertools.tee"><code class="xref py py-func docutils literal notranslate"><span class="pre">tee()</span></code></a></p></td>
<td><p>it, n</p></td>
<td><p>it1, it2, … itn  splits one iterator into n</p></td>
<td></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.zip_longest" title="itertools.zip_longest"><code class="xref py py-func docutils literal notranslate"><span class="pre">zip_longest()</span></code></a></p></td>
<td><p>p, q, …</p></td>
<td><p>(p[0], q[0]), (p[1], q[1]), …</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">zip_longest('ABCD',</span> <span class="pre">'xy',</span> <span class="pre">fillvalue='-')</span> <span class="pre">--&gt;</span> <span class="pre">Ax</span> <span class="pre">By</span> <span class="pre">C-</span> <span class="pre">D-</span></code></p></td>
</tr>
</tbody>
</table>

<table class="docutils align-center">
<colgroup>
<col style="width: 36%">
<col style="width: 16%">
<col style="width: 48%">
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Iterator</p></th>
<th class="head"><p>Arguments</p></th>
<th class="head"><p>Results</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.product" title="itertools.product"><code class="xref py py-func docutils literal notranslate"><span class="pre">product()</span></code></a></p></td>
<td><p>p, q, … [repeat=1]</p></td>
<td><p>cartesian product, equivalent to a nested for-loop</p></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.permutations" title="itertools.permutations"><code class="xref py py-func docutils literal notranslate"><span class="pre">permutations()</span></code></a></p></td>
<td><p>p[, r]</p></td>
<td><p>r-length tuples, all possible orderings, no repeated elements</p></td>
</tr>
<tr class="row-even"><td><p><a class="reference internal" href="#itertools.combinations" title="itertools.combinations"><code class="xref py py-func docutils literal notranslate"><span class="pre">combinations()</span></code></a></p></td>
<td><p>p, r</p></td>
<td><p>r-length tuples, in sorted order, no repeated elements</p></td>
</tr>
<tr class="row-odd"><td><p><a class="reference internal" href="#itertools.combinations_with_replacement" title="itertools.combinations_with_replacement"><code class="xref py py-func docutils literal notranslate"><span class="pre">combinations_with_replacement()</span></code></a></p></td>
<td><p>p, r</p></td>
<td><p>r-length tuples, in sorted order, with repeated elements</p></td>
</tr>
</tbody>
</table>

<table class="docutils align-center">
<colgroup>
<col style="width: 43%">
<col style="width: 57%">
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Examples</p></th>
<th class="head"><p>Results</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">product('ABCD',</span> <span class="pre">repeat=2)</span></code></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">AA</span> <span class="pre">AB</span> <span class="pre">AC</span> <span class="pre">AD</span> <span class="pre">BA</span> <span class="pre">BB</span> <span class="pre">BC</span> <span class="pre">BD</span> <span class="pre">CA</span> <span class="pre">CB</span> <span class="pre">CC</span> <span class="pre">CD</span> <span class="pre">DA</span> <span class="pre">DB</span> <span class="pre">DC</span> <span class="pre">DD</span></code></p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">permutations('ABCD',</span> <span class="pre">2)</span></code></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">AB</span> <span class="pre">AC</span> <span class="pre">AD</span> <span class="pre">BA</span> <span class="pre">BC</span> <span class="pre">BD</span> <span class="pre">CA</span> <span class="pre">CB</span> <span class="pre">CD</span> <span class="pre">DA</span> <span class="pre">DB</span> <span class="pre">DC</span></code></p></td>
</tr>
<tr class="row-even"><td><p><code class="docutils literal notranslate"><span class="pre">combinations('ABCD',</span> <span class="pre">2)</span></code></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">AB</span> <span class="pre">AC</span> <span class="pre">AD</span> <span class="pre">BC</span> <span class="pre">BD</span> <span class="pre">CD</span></code></p></td>
</tr>
<tr class="row-odd"><td><p><code class="docutils literal notranslate"><span class="pre">combinations_with_replacement('ABCD',</span><span class="pre">2)</span></code></p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">AA</span> <span class="pre">AB</span> <span class="pre">AC</span> <span class="pre">AD</span> <span class="pre">BB</span> <span class="pre">BC</span> <span class="pre">BD</span> <span class="pre">CC</span> <span class="pre">CD</span> <span class="pre">DD</span></code></p></td>
</tr>
</tbody>
</table>

