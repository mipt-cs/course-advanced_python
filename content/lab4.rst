Массивы в С.
#############

:date: 2018-09-17 07:06
:summary: Массивы в С
:status: draft
:published: yes

.. default-role:: code

.. contents:: Содержание

.. role:: c(code)
   :language: c

Массивы в С.
============

Массивы — структура данных, хранящая набор значений (элементов массива), идентифицируемых по индексу или набору индексов, принимающих целые (или приводимые к целым) значения из некоторого заданного непрерывного диапазона.

Работа с массивом в **С** предполагает

- определение переменной, которая будет его хранить и его размер (например, :c:`int a[10];`);
- использование синтаксиса, типа :c:`a[i]` для доступа к элементу массива за номером :c:`i`.

Данные массива располагаются в оперативной памяти последовательно а сама переменна хранит адрес первого элемента массива(т.е. элемента за номером 0), что, с учётом адресной арифметики, позволяет использовать альтернативный синтаксис для доступа к элементу массива (:c:`a[i] ≡ *(a+i)`)

**Важно**
---------

- Определить массив можно в любой момент, в том числе после того, как вы уже узнали необходимый размер массива;
- Во время компиляции и запуска, программа не проверяет произошёл ли выход за границы массива;
- Память, занимаемая массивом освобождается вместе с имени переменной
- Индексация массива начинается с **0**. То есть у массива из **5-ти** элементов можно смело использовать индексы **0, 1, 2, 3, 4**

Пример программы:

.. code-block:: c

        #include <stdio.h>

        void print_array(const int a[], int size)
        {
            printf("Array: ");
            for (int i = 0; i < size; ++i)             
            {
                printf("%d ", a[i]);
            }
            printf("\n");
        }

        int main(){
                int n, *b;
                scanf("%d", &n);        // input array size
                {                       // -- begin block --

                        int a[n];       // define array inside the block

                        for (int i = 0; i < n; a[i++] = i * i); // fill array
                        print_array(a, n);                      // print array
                        b = a;  // save array address

                }                       // -- end block --

                int a;                           // define a as integer
                scanf("%d", &a);                 // input value
                printf("n = %d\n", a);            // print it
                print_array(b, n);               // print array

                return 0;
        }

Результат работы программы:

.. code-block:: bash
        
        ./app
        5
        Array: 1 4 9 16 25
        5
        n = 5
        Array: 1 4 9 3 -182291632


Как можно видеть из примера: 

#. После окончания блока переменная :c:`a` «освободилась», и её можно использовать, как переменную другого типа (:c:`int`).
#. Если память, соответствующая некоторому массиву считается свободной — нельзя гарантировать сохранность данных и корректную работу программы
#. Чтобы контролировать неизменность массива :c:`a` в процессе *компиляции*, тип первой передаваемой функции :c:`const int a[]`


Данные пункты являются важными, поскольку такой подход не позволяет писать функции, создающие массив. Для создания таковых — необходимо использовать динамические массивы.

Динамические массивы, malloc, calloc, realloc, free.
====================================================

Функция :c:`void * malloc( size_t sizemem );` запрашивает у операционной системы выделить :c:`sizemems` байт памяти и возвращает указатель на выделенную область памяти. **Содержимое выделенной памяти не определено**.

Пример использования:

.. code-block:: c

        int *a, n;
        scanf("%d", &n);
        a = malloc(n * sizeof(int));

Поскольку размер :c:`int` заранее неизвестен, то для определения, того, сколько байт занимает один :c:`int` используется функция :c:`sizof()`. Другими словами: :c:`sizeof()` его знает, сколько памяти занимает :c:`int`. Аналогичным образом можно узнать сколько байт занимает тот или иной тип, или же конкретная переменная.

Функция :c:`сalloc()` делает то-же самое что и :c:`malloc()`, но дополнительно ещё заполняет выделенную память нулями.

**Память, выделенная программе при помощи malloc или calloc, остаётся зарезервированной за ней, вплоть до использования функции free.**

Несмотря на то, что большинство современных операционных систем «убирают» за программами «мусор» не использование функции :c:`free()` является грубой ошибкой, и в ряде (в первую очередь старых) операционных систем приведёт к утечке оперативной памяти компьютера.

.. _APP:

Пример использования:

.. code-block:: c

        #include <stdio.h>
        #include <stdlib.h>        // to using malloc, free

        void print_array(const int *a, int size)
        {
            printf("Array: ");
            int *tmp = a + size;
            for (; a != tmp; ++a)             
            {
                printf("%d ", *a);
            }
            printf("\n");
        }

        int * create_array(int size)
        {
            int *tmp;

            // allocate memory and convert void* to int*
            tmp = (int*)malloc(size * sizeof(int));
            for (int i = 0; i < size; ++i)
            {
                tmp[i] = i * i;
            };
            return tmp;
        }

        int main(){
                int n, *a;
                scanf("%d", &n);        // input array size

                a = create_array(n);    // fill array
                print_array(a, n);      // print array
                free(a);                // free memory
                a = NULL;               // nullify a
                return 0;
        }

*Обратите внимание на вариант функции для вывода массива print_array. Присутствует здесь только в качестве примера.*

В случае, если необходимо перевыделить оперативную память (уменьшить или увеличить) — используйте функцию :c:`realloc()`

Пример:

.. code-block:: c
        
        int *a;
        a = malloc(5 * sizeof(int)); // allocate memory
        // some code here
        a = realloc(a, 10 * sizeof(int)); // return new address to a

Стоит отметить, что в случае, если вы увеличиваете количество требуемой оперативной памяти функция :c:`realloc` ведёт себя примерно следующим образом:

.. code-block:: c
        
        int *a;
        a = malloc(5 * sizeof(int)); // allocate memory
        // some code here
        {
            int *tmp = malloc(10 * sizeof(int)); // alllocate new memory
            memcpy(tmp, a, 5*sizeof(int));       // copy old data
            free(a);                             // free old memory
            a = tmp;                             // copy address to a
        }

Valgrind
========

Для проверки корректности работы вашей программы с памятью в Linux, используйте программу **valgrind**. Для примера — возьмите программу APP_ выше (пусть она называется *alloc_example.c*) следуйте коду ниже:

.. code-block:: console

        $ gcc -g -o app alloc_example.c
        $ echo 5 | valgrind --leak-check=full ./app
        ==789== Memcheck, a memory error detector
        ==789== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
        ==789== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
        ==789== Command: ./a.out
        ==789==
        ==789== error calling PR_SET_PTRACER, vgdb might block
        Array: 0 1 4 9 16
        ==789==
        ==789== HEAP SUMMARY:
        ==789==     in use at exit: 0 bytes in 0 blocks
        ==789==   total heap usage: 3 allocs, 3 frees, 8,212 bytes allocated
        ==789==
        ==789== All heap blocks were freed -- no leaks are possible
        ==789==
        ==789== For counts of detected and suppressed errors, rerun with: -v
        ==789== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
        $ gcc -g -D free\(a\)=// -o app alloc_example.c
        $ echo 5 | valgrind --leak-check=full ./app
        ==1018== Memcheck, a memory error detector
        ==1018== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
        ==1018== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
        ==1018== Command: ./app
        ==1018==
        ==1018== error calling PR_SET_PTRACER, vgdb might block
        Array: 0 1 4 9 16
        ==1018==
        ==1018== HEAP SUMMARY:
        ==1018==     in use at exit: 20 bytes in 1 blocks
        ==1018==   total heap usage: 3 allocs, 2 frees, 8,212 bytes allocated
        ==1018==
        ==1018== 20 bytes in 1 blocks are definitely lost in loss record 1 of 1
        ==1018==    at 0x4C2DB8F: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        ==1018==    by 0x40071C: create_array (alloc_example.c:20)
        ==1018==    by 0x40078F: main (alloc_example.c:32)
        ==1018==
        ==1018== LEAK SUMMARY:
        ==1018==    definitely lost: 20 bytes in 1 blocks
        ==1018==    indirectly lost: 0 bytes in 0 blocks
        ==1018==      possibly lost: 0 bytes in 0 blocks
        ==1018==    still reachable: 0 bytes in 0 blocks
        ==1018==         suppressed: 0 bytes in 0 blocks
        ==1018==
        ==1018== For counts of detected and suppressed errors, rerun with: -v
        ==1018== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

В примере выше — сначала компилируется программа, а затем запускается через valgrind, при этом для того, чтобы не вводить 5 с клавиатуры во время работы программы использована комбинация ``echo 5 | valgrind --leak-check=full ./app``. valgrind показал, что никаких утечек памяти нет (``All heap blocks were freed -- no leaks are possible``).

Далее идёт компиляция той же программы, но уже с отключением функции :c:`free` внутри данного файла (``-D free\(a\)=//``). Далее идёт опять запуск ``valgrind``, который показывает утечку памяти 

``20 bytes in 1 blocks are definitely lost in loss record 1 of 1``

и показывает, что не очищена при помощи :c:`free` память, выделенная в 20-ой строке программы 

``==1018==    by 0x40071C: create_array (alloc_example.c:20)``

Упражнение №1
-------------

Напишите функции сортировки массива следующими методами:

#. Вставкой
#. Выбором
#. Пузырьком
#. Быстрая сортировка Хоара
#. Сортировка слиянием

Для заполнения исходного массива используйте:

.. code-block:: c
        
        void fill_array(int *a; int size)
        {
            for (i = 0; i < size; ++i) a[i] = rand() % 
        }

Многомерные массивы (на примере двумерного)
===========================================

Для создания двумерного массива можно воспользоваться методом, аналогичным простым массивам в **С**. :c:`int a[n][m];`

Однако надо помнить, что такой массив (как и одномерный) будет располагаться в памяти последовательно, что требует написание кода, аналогичного следующему:

.. code-block:: c

        #include <stdlib.h>
        #include <stdio.h>

        void print2array(int  a[][4], int n)
        {
                for (int i=0; i < n; ++i){
                        for (int j = 0; j < 4; ++j){
                                printf("%d ", a[i][j]);
                        }
                        printf("\n");
                }
        }

        int main()
        {
                int n;
                scanf("%d ", n);
                int a[n][4];
                for (int i=0; i < n; ++i){
                        for (int j = 0; j < 4; ++j){
                                a[i][j] = i + j;
                        }
                };

                print2array(a, n);
                return 0;
        }

В данном коде видно, что последовательное расположение элементов в памяти компьютера требует, чтобы ширина двумерного массива была известна на момент компиляции программы (в данном случае **4**).

Тем не менее — никто не запрещает сделать динамический массив динамических массивов. Классическое создание такого массива происходит следующим образом:

.. code-block:: c

        int n, m, **a;
        a = malloc(n * sizeof(int*));
        for (int i = 0; i < n; ++i){
            a[i] = malloc(m * sizeof(int));
        }

Упражнение №2
-------------

Напишите программу, включающую в себя: 

- функцию печатания на экран двумерного массива
- выделение памяти под двумерный массив
- заполнение массива по формуле :math:`a_{i,j} = i + j^2`
- освобождение всей размещённой памяти (проверка при помощи ``valgrind``)


Упрощенное выделение памяти для двумерного массива
++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: c

        int n, m, **a;
        a = (int**)malloc(n * sizeof(int*) + n * m * sizeof(int));
        for (int i = 0; i < n; ++i){
            a[i] = a[0] + n;
        }