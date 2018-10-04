Структуры в Си
#####################################################################

:date: 2018-09-30 10:00
:summary: Структуры в С.
:status: published
:published: yes

.. default-role:: code

.. contents:: Содержание


Структуры в **С**
==========================

Структура — это объединение нескольких объектов, возможно, различного типа под одним именем, которое является типом структуры. В качестве объектов могут выступать переменные, массивы, указатели и другие структуры. Как вы можете заметить, структуры по своему описанию напоминают классы из курса ООП python, которые содержат только атрибуты.

Синтаксис структур в C:

.. code-block:: c
        
        struct <имя> {
            <тип1> <поле1>;
            <тип2> <поле2>;
            ...
            <типN> <полеN>;
            };


Давайте рассмотрим пример структуры, которая описывает дату:

Пример №1
---------

.. code-block:: c
        
        struct date
        {
            int day;     // 4 байта
            int month; // 4 байта
            int year;    // 4 байта
        };

Поля структуры располагаются в памяти в том порядке, в котором они объявлены:

.. image:: https://prog-cpp.ru/wp-content/uploads/2014/03/struct_date3.png
   :width: 530
   :align: center

К полям структуры можно обращаться через точку:

.. code-block:: c

        #include<stdio.h>
        #include<stdlib.h>
        
        typedef struct
        {
            int day;     // 4 байта
            int month;   // 4 байта
            int year;    // 4 байта
        } date;
        
        int main() {
            date birthday;
            birthday.day = 9;
            birthday.month = 9;
            birthday.year = 1941;
            printf("%02d %02d %04d\n", birthday.day, birthday.month, birthday.year);
        }


Упражнение №1
-------------

Напишите программу, содержащую структуру, которая хранит номер вашего факультета, группы и год зачисления.

Длинная арифметика
===================

Из второй лабораторной работы вам должно быть известно, что у каждого типа чисел в C есть максимальное и минимальное значение, обусловленные количеством выделенной оперативной памяти. Так, наибольшее значение для целочисленного типа unsigned long int составляет 4294967295. Если вы попробуете записать большее число в переменную данного типа, то произойдет переполнение. В результате переменная будет содержать не то, что вы от неё ожидаете. 

Допустим, вам надо работать с целочисленными значениями порядка 10^1000. Для этого нужно использовать длинную арифметику. В самом простом случае операции сложения, умножения и вычитания в длинной арифметике эквивалентны этим же операциям "в столбик": операции производятся поразрядно, начиная с младшего разряда. 

.. image:: http://math-prosto.ru/images/action-in-column/addition-column5.png
   :width: 114
   :align: center

Недостатком такого подхода является то, что эти операции реализуются не аппаратно, а программно, с использованием базовых аппаратных средств работы с числами меньших порядков. Иными словами, они намного медленней.

Давайте напишем программу, способную выполнять операции сложения, вычитания и деления с десятичными числами произвольной длины.

Пример №2
---------

.. code-block:: c
        
        struct big_number
        {
            int *digits;
            int sign;
            int size;
        };

Эта структура хранит указатель digits на int. В него можно будет записать массив int произвольной длинны, используя функции calloc или malloc. size хранит количество разрядов в числе, а sign - знак.

Рассмотрим функцию для зачитывания таких чисел. Эта функция зачитывает со стандартного ввода число до переноса строки.

Пример №3
---------

.. code-block:: c

        #include<stdio.h>
        #include<stdlib.h>
        
        #define MAX_NUMBER_LEN 1000
  
        typedef struct
        {
            int *digits;
            int sign;
            int size;
        } large_numbers;
        
        large_numbers input_large_numbers()
        {
            large_numbers number;
            number.sign = 1;
            
            int *buffer = (int*)calloc(MAX_NUMBER_LEN, sizeof(int));
            int size = 0;
            
            while(1)
            {
                char c;
                scanf("%c", &c);
                
                if (c == '\n') {
                    break;
                }
                
                if (size == 0 && c == '-') {
                    number.sign = -1;
                    continue;
                }
                
                if (size == 0 && c == '+') {
                    continue;
                }
                
                int p = c - '0';
                buffer[size++] = p;
            }   
            number.digits = (int*)calloc(size, sizeof(int));
            number.size = size;
            for (int i = 0; i < size; ++i) {
                number.digits[i] = buffer[size - i - 1];
            }
            
            return number;
        }


Как вы можете заметить, число хранится в реверсированном виде: младшие разряды идут первыми. Это сделано для удобства выполнения арифметических операций.

Пример №4
---------

.. code-block:: c

        void print_large_numbers(large_numbers number) {
            if (number.sign == -1) {
                printf("-");
            }
        
            for (int i = number.size - 1; i >= 0; --i) {
                printf("%d", number.digits[i]);
            }
            printf("\n");
        }
        
        int main()
        {
            large_numbers number;
        
            number = input_large_numbers();
            print_large_numbers(number);
        
            return 0;
        }

Простейшая программа, которая зачитывет и печатает число.

Упражнение №2
-------------

В такой реализации есть 2 утечки памяти. Исправьте это.





Рассмотрим функцию сложения двух big_number.

Пример №5
---------

.. code-block:: c

        int max(int a, int b) {
            if (a >= b) {
                return a;
            }
            return b;
        }
        
        int min(int a, int b) {
            if (a <= b) {
                return a;
            }
            return b;
        }
        
        large_numbers add(large_numbers lhs, large_numbers rhs) {
            large_numbers result;
            int remainder = 0;
            
            int common = min(lhs.size, rhs.size);
            int Max = max(lhs.size, rhs.size);
            
            result.digits = (int*)calloc(Max + 1, sizeof(int));
            // сложение общих разрядов
            for (int i = 0; i < common; ++i) {
                int value = lhs.sign * lhs.digits[i] + rhs.sign * rhs.digits[i] + remainder;
                result.digits[i] = value % 10;
                remainder = value / 10;
            }
            // сложение различающихся разрядов
            for (int i = common; i < lhs.size; ++i) {
                int value = lhs.sign * lhs.digits[i] + remainder;
                result.digits[i] = value % 10;
                remainder = value / 10;
            }
            for (int i = common; i < rhs.size; ++i) {
                int value = rhs.sign * rhs.digits[i] + remainder;
                result.digits[i] = value % 10;
                remainder = value / 10;
            }
            // остаток
            if (remainder == 0) {
                result.size = Max;
                result.digits = (int*)realloc(result.digits, Max*sizeof(int));
            } else {
                result.digits[Max] = remainder;
                result.size = Max + 1;      
            }
            
            return result;
        }

В такой реализации функция складывает два положительных числа.


Упражнение №3
-------------

Запустите и проверьте как работает программа. В качестве примеров можете использовать 99999999999999999999999999999999999999999999999999999999999999999999999999999999999 и 1. Не забывайте про утечки памяти.

.. code-block:: c

        int main()
        {
            large_numbers number, number2, SUM;
        
            number = input_large_numbers();
            number2 = input_large_numbers();
        
            SUM = add(number, number2);
            print_large_numbers(SUM);
        
            return 0;
        }

Упражнение №4
-------------

Напишите функцию умножения двух чисел. Не забывайте, что складывать вы уже умеете.

Упражнение №5
-------------

Исправьте функцию сложения, чтобы она корректно работала с отрицательными числами.

Упражнение №6
-------------

Исправьте функцию разности. (Если все сделано правильно, то она должна состоять из трех строк).


Информация к размышлению
========================
Кажется неудобным, что нужно постоянно вызывать free. А ведь даже не приходилось хранить массив структур big_number. Как можно автоматизировать процесс очистки памяти? Вспомните о деструкторах из курса ООП Python.

Кажется неудобным, что для сложения чисел надо вызывать отдельную фукнцию. А что делать, если за раз надо сложить 3 или 5 big_number? А что делать, если нужно сравнить 2 big_number? Вспомните о перегрузке операторов из курса ООП Python. 
