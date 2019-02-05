Повторение синтаксиса Python. ООП. Принципы и парадигмы ООП. Объекты и классы в Python.
#######################################################################################

:date: 2018-10-29 07:30
:summary: Повторение синтаксиса Python. ООП. Принципы и парадигмы ООП. Объекты и классы в Python.
:status: published
:published: yes

.. default-role:: code

.. contents:: Содержание

Повторение синтаксиса Python
============================

Операции с целыми числами
-------------------------

.. code-block:: python
        
        2 + 5
	10 - 5
	6 * 7
	12345678 * 987654328765432318765
	3 + 5 * 4
	(3 + 5) * 4
	40 // 8
	42 // 8
	42 % 8
	239 % 10
	239 // 10
	2 ** 5
	- (42)
	+ (42)
	+-+42

Сообщения об ошибках
--------------------

.. code-block:: python
	
	-*42
	
	print('test')
	* 23
	
	5 // 0

Числа с плавающей точкой
------------------------

.. code-block:: python

        0.5 + 0.3
	5 / 2
	5 // 2
	1 / 3
	0.3 + 0.3 + 0.3
	2 ** 5
	9 ** 0.5
	5e-1
	1234e2

Переменные
----------

.. code-block:: python

	a = 3
	a
	a += 4
	a
	a
	2 * a  # выводится только последнее значение и только при работе в интерактивном режиме!

Для вывода значений в своих программах используйте функцию print(). Обратите внимание на наличие скобок при вызове функции print!

.. code-block:: python

	print(a)
	print(2 * a)

Можно выводить диалоговые сообщения при 'общении' c пользователем. Но не отправляйте в проверочную систему программы, содержащие лишний вывод

.. code-block:: python

	name = input('Enter your name: ')
	print('Hello ', name)
	
	a = int(input())
	print(a * 2)
	
	a = int(input())
	b = int(input())
	print(a * b)


Логические операции
-------------------

.. code-block:: python
        
        a = int(input())
	print(a > 0)

	a = int(input())
	print(a >= 10 and a < 100)

	a = int(input())
	print(10 <= a < 100)

	x1, x2, x3 = False, True, False
	not x1 or x2 and x3

Добавляя скобки в выражения, можно изменить порядок вычисления и значение результирующего выражения. Если не уверены в приоритете операций, смело добавляйте скобки, чтобы быть уверенными в том, что выражение вычисляется именно так, как вы хотите

.. code-block:: python

	((not x1) or x2) and x3

Условия
-------

.. code-block:: python

	a = int(input())
	b = int(input())
	print(a / b)

.. code-block:: python

	a = int(input())
	b = int(input())
	if b != 0:
    		print(a / b)
	else:
    		print('Деление невозможно')

.. code-block:: python

	a = int(input())
	b = int(input())
	if b != 0:
    		print(a / b)
	else:
    		print('Деление невозможно')
    		b = int(input('Введите ненулевое значение '))
    		print(a / b)

.. code-block:: python

	a = int(input())
	b = int(input())
	if b != 0:
    		print(a / b)
	else:
    		print('Деление невозможно')
    		b = int(input('Введите ненулевое значение '))
    		if b == 0:
        		print('Вы не справились!')
    	else:
        	print(a / b)

.. code-block:: python

	x = int(input())
	if x % 2 == 0:
    		print('Четное')
	else:
    		print('Нечетное')

Наибольшее из двух чисел

.. code-block:: python

	a = 4
	b = 7
	if a >= b:
    		print(a)
	else:
    		print(b)

Строки
------

.. code-block:: python

	a = 'string'
	b = 'another string'
	print(a, b)

.. code-block:: python

	print(a + b)  # конкатенация строк

.. code-block:: python

	print(a)
	'''
	multiline
	comment
	'''
	print(b)

.. code-block:: python
	
	print(a + '\n' + b)  # вывод в двух различных строчках
	
	'string1'

	"string2"
	
	'''multiple lines
	string'''
	
	"""multiple lines
	string with double qoutes"""

	'abc' + 'def'

	'abc' * 3

	len('abcdef')

	'abc' == '''abc'''

	'abc' < 'ac'

	'abc' > 'ab'

	print('First line', '\n\n\n', 'Last line')

	

	# это комментарий
	x = 5 # комментарий к действию
	'''
	Многострочный комментарий – это просто
	строка
	'''


Цикл While
----------

.. code-block:: python
	
	a = 5
	while a > 0:
    		print(a, end=' ')
    		a -= 1

Вывести все нечетные числа от 5 до 55

.. code-block:: python

	a = 5
	while a <= 55:
    		print(a, end=' ')
    		a += 2

Вывести треугольник из звезд

.. code-block:: python

	n = int(input())
	c = 1
	while c <= n:
    		print('*' * c)
    		c += 1

Посчитать сумму чисел от a до b

.. code-block:: python

	a = int(input())
	b = int(input())
	s = 0
	i = a
	while i <= b:
    		s += i
    		i += 1
	print(s)

Вывести произведение пяти пар чисел

.. code-block:: python

	i = 0
	while i < 5:
    		a, b = input().split()  # split() разбивает строку на части по пробелам
    		a = int(a)
    		b = int(b)
    		print(a * b)
    		i += 1

Операторы break, continue
-------------------------

.. code-block:: python

	i = 0
	while i < 5:
    		a, b = input().split()
    		a = int(a)
    		b = int(b)
    		if (a == 0) and (b == 0):
        		break # досрочно завершаем цикл
    		if (a == 0) or (b == 0):
        		continue # переходим к следующей итерации
    		print(a * b)
    		i += 1

Цикл for
--------

.. code-block:: python

	for i in 2, 3, 5:
    		print(i * i)

Вывести квадрат из звездочек

.. code-block:: python

	n = int(input())
	for i in range(n):
    		print('*' * n)

Сумма нечетных чисел на отрезке от a до b

.. code-block:: python

	a, b = input().split()
	a = int(a)
	b = int(b)
	s = 0
	for i in range(a, b + 1):
    		if i % 2 == 1:
        		s += i
	print(s)

Строки
------

.. code-block:: python

	genome = 'ATGG'
	print(genome[0])
	print(genome[1])
	print(genome[2])
	print(genome[3])
	print(genome[-1])
	print(genome[-2])
	print(genome[-3])
	print(genome[-4])


	genome = 'ATGG'
	for i in range(4):
    		print(genome[i])


	genome = 'ATTG'
	for c in genome:
    		print(c)
	
Подсчет числа символов C в строке

.. code-block:: python

	genome = input()
	cnt = 0
	for nucl in genome:
	    if nucl == 'C':
	        cnt += 1
	print(cnt)

Методы строк
------------

.. code-block:: python

	s = 'aTGcc'
	p = 'cc'

	s.upper()

	s.lower()

	s.count(p)

	s.find(p)

	s.find('A')

	s.replace('c', 'C')

	s = 'agTtcAGtc'
	s.upper().count('gt'.upper())

Срезы (slices)
--------------

.. code-block:: python

	dna = 'ATTCGGAGCT'

	dna[1]

	dna[1:4]

	dna[:4]

	dna[4:]

	dna[-4:]

	dna[1:-1]

	dna[1:-1:2]

	dna[::-1]

Списки
------

.. code-block:: python

	students = ['Ivan', 'Masha', 'Sasha']
	for student in students:
	    print("Hello, " + student + "!")

	len(students)

	students[::-1]  # индексация и срезы на списках работают также, как и со строками

	students = ['Ivan', 'Masha', 'Sasha']

	teachers = ['Oleg', 'Alex']

	students + teachers

	[0, 1] * 4

	students = ['Ivan', 'Masha', 'Sasha']
	students[1] = 'Oleg'
	print(students)

	students = ['Ivan', 'Masha', 'Sasha']

	students.append('Olga')
	print(students)

	students += ['Olga']
	print(students)

	students += ['Boris', 'Sergey']

	print(students)

	[]  # пустой список

	students = ['Ivan', 'Masha', 'Sasha']
	students.insert(1, 'Olga')
	print(students)

	students = ['Ivan', 'Masha', 'Sasha']
	students.remove('Sasha')
	print(students)


	del students[0]
	print(students)

Генерация списков
-----------------

.. code-block:: python

	a = [0] * 5
	print(a)

	a = [0 for i in range(5)]
	print(a)

	a = [i * i for i in range(5)]
	print(a)

	a = [int(i) for i in input().split()]
	print(a)

Двумерные списки
----------------

.. code-block:: python

	a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	
	a[1]

	a[1][1]

	n = 3
	a = [[0] * n] * n
	print(a)
	a[0][0] = 5
	print(a)

Объекты и классы в Python
=========================

Объектно-ориентированное программирование (ООП) — парадигма программирования, в которой основными концепциями являются понятия объектов и классов.

Класс — тип, описывающий устройство объектов. Объект — это экземпляр класса. Класс можно сравнить с чертежом, по которому создаются объекты.

Python соответствует принципам объектно-ориентированного программирования. В python всё является объектами - и строки, и списки, и словари, и всё остальное.

Но возможности ООП в python этим не ограничены. Программист может написать свой тип данных (класс), определить в нём свои методы.

Это не является обязательным - мы можем пользоваться только встроенными объектами. Однако ООП полезно при долгосрочной разработке программы несколькими людьми, так как упрощает понимание кода.

Приступим теперь собственно к написанию своих классов на python. Попробуем определить собственный класс:

.. code-block:: python

	# Пример простейшего класса, который ничего не делает
	class A:
		pass

Теперь мы можем создать несколько экземпляров этого класса:

.. code-block:: python

	a = A()
	b = A()
	a.arg = 1 # у экземпляра a появился атрибут arg, равный 1
	b.arg = 2 # а у экземпляра b - атрибут arg, равный 2
	print(a.arg)
	
	print(b.arg)
	
	c=A()
	print(c.arg) # а у этого экземпляра нет arg

Классу возможно задать собственные методы:

.. code-block:: python

	class A:
		def g(self): # self - обязательный аргумент, содержащий в себе экземпляр
			     # класса, передающийся при вызове метода,
			     # поэтому этот аргумент должен присутствовать
			     # во всех методах класса.
			return 'hello world'

	a = A()
	a.g()

.. code-block:: python

	class B:
		arg = 'Python' # Все экземпляры этого класса будут иметь атрибут arg,
			       # равный "Python"
			       # Но впоследствии мы его можем изменить
		def g(self):
			return self.arg

	b = B()
	b.g()

	B.g(b)
	
	b.arg = 'spam'
	b.g()
