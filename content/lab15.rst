Объектно-ориентированное программирование. Python.
##################################################

:date: 2020-09-02 19:00
:summary: Тема 15. Библиотека Pandas для работы с данными
:status: not_published

.. default-role:: code

.. role:: python(code)
   :language: python
   
.. contents::


*На основе материалов за авторством: Юрий Кашницкий (DS in KPN,
NLP-Researcher) и Екатерина Демидова (DS в Segmento).

Pandas — программная библиотека на языке Python для обработки и анализа
данных. Работа pandas с данными строится поверх библиотеки NumPy,
являющейся инструментом более низкого уровня. Предоставляет специальные
структуры данных и операции для манипулирования числовыми таблицами и
временны́ми рядами.

Главный элемент пандаса - DataFrame (датафрейм, df), с которым можно
производить необходимые преобразования. df - “таблица”, состоящая из
строк и столбцов. По умолчанию, строчки таблицы - это объекты, а столбцы
- признаки (фичи) объектов.

.. code:: python

    import pandas as pd
    import numpy as np

Создание DataFrame
------------------

.. code:: python

    d = {'feature1': [4,3,2,1,0], 'feature2': ['x', 'z', 'y', 'x', 'z'], 'feature3': [2,3,4,1,0]}
    df = pd.DataFrame(d)
    df




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>feature1</th>
          <th>feature2</th>
          <th>feature3</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>4</td>
          <td>x</td>
          <td>2</td>
        </tr>
        <tr>
          <th>1</th>
          <td>3</td>
          <td>z</td>
          <td>3</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>y</td>
          <td>4</td>
        </tr>
        <tr>
          <th>3</th>
          <td>1</td>
          <td>x</td>
          <td>1</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0</td>
          <td>z</td>
          <td>0</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    data = [['tom', 10], ['nick', 15], ['juli', 14]] 
    df = pd.DataFrame(data, columns = ['Name', 'Age'])  
    df




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Name</th>
          <th>Age</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>tom</td>
          <td>10</td>
        </tr>
        <tr>
          <th>1</th>
          <td>nick</td>
          <td>15</td>
        </tr>
        <tr>
          <th>2</th>
          <td>juli</td>
          <td>14</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    data = {'Name':['Tom', 'Jack', 'nick', 'juli'], 'marks':[99, 98, 95, 90]} 
    df = pd.DataFrame(data, index =['rank1', 'rank2', 'rank3', 'rank4'])  
    df 




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Name</th>
          <th>marks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>rank1</th>
          <td>Tom</td>
          <td>99</td>
        </tr>
        <tr>
          <th>rank2</th>
          <td>Jack</td>
          <td>98</td>
        </tr>
        <tr>
          <th>rank3</th>
          <td>nick</td>
          <td>95</td>
        </tr>
        <tr>
          <th>rank4</th>
          <td>juli</td>
          <td>90</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    data = [{'a': 1, 'b': 2, 'c':3}, {'a':10, 'b': 20}] 
    df = pd.DataFrame(data) 
    df 




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>a</th>
          <th>b</th>
          <th>c</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>2</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>10</td>
          <td>20</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    d = {'one' : pd.Series([10, 20, 30, 40], index =['a', 'b', 'c', 'd']), 
          'two' : pd.Series([10, 20, 30, 40], index =['a', 'b', 'c', 'd'])} 
    df = pd.DataFrame(d) 
    df 




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>one</th>
          <th>two</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>a</th>
          <td>10</td>
          <td>10</td>
        </tr>
        <tr>
          <th>b</th>
          <td>20</td>
          <td>20</td>
        </tr>
        <tr>
          <th>c</th>
          <td>30</td>
          <td>30</td>
        </tr>
        <tr>
          <th>d</th>
          <td>40</td>
          <td>40</td>
        </tr>
      </tbody>
    </table>
    </div>



.. raw:: html

   <center>

Первичный анализ данных с Pandas
----------
.. raw:: html

   </center>

`Pandas <http://pandas.pydata.org>`__ — это библиотека Python,
предоставляющая широкие возможности для анализа данных. С ее помощью
очень удобно загружать, обрабатывать и анализировать табличные данные с
помощью SQL-подобных запросов. В связке с библиотеками ``Matplotlib`` и
``Seaborn`` появляется возможность удобного визуального анализа
табличных данных.

Данные, с которыми работают датсаентисты и аналитики, обычно хранятся в
виде табличек — например, в форматах ``.csv``, ``.tsv`` или ``.xlsx``.
Для того, чтобы считать нужные данные из такого файла, отлично подходит
библиотека Pandas.

Основными структурами данных в Pandas являются классы ``Series`` и
``DataFrame``. Первый из них представляет собой одномерный
индексированный массив данных некоторого фиксированного типа. Второй -
это двухмерная структура данных, представляющая собой таблицу, каждый
столбец которой содержит данные одного типа. Можно представлять её как
словарь объектов типа ``Series``. Структура ``DataFrame`` отлично
подходит для представления реальных данных: строки соответствуют
признаковым описаниям отдельных объектов, а столбцы соответствуют
признакам.

.. code:: python

    pd.read_csv('beauty.csv', nrows=2)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage;exper;union;goodhlth;black;female;married;service;educ;looks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>5.73;30;0;1;0;1;1;1;14;4</td>
        </tr>
        <tr>
          <th>1</th>
          <td>4.28;28;0;1;0;1;1;0;12;3</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    #help(pd.read_csv)
    path_to_file = 'beauty.csv'
    data = pd.read_csv(path_to_file, sep=';')
    
    print(data.shape)
    #df.tail()
    data.head()


.. parsed-literal::

    (1260, 10)
    



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>5.73</td>
          <td>30</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>4</td>
        </tr>
        <tr>
          <th>1</th>
          <td>4.28</td>
          <td>28</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.96</td>
          <td>35</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>10</td>
          <td>4</td>
        </tr>
        <tr>
          <th>3</th>
          <td>11.57</td>
          <td>38</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>16</td>
          <td>3</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11.42</td>
          <td>27</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
        </tr>
      </tbody>
    </table>
    </div>



Мы считали данные по модельному бизнесу 80-90е года в США

.. code:: python

    type(data)




.. parsed-literal::

    pandas.core.frame.DataFrame



.. code:: python

    #data.shape
    len(data)




.. parsed-literal::

    1260



Чтобы посмотреть общую информацию по датафрейму и всем признакам,
воспользуемся методом info:

.. code:: python

    data.info()


.. parsed-literal::

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1260 entries, 0 to 1259
    Data columns (total 10 columns):
    wage        1260 non-null float64
    exper       1260 non-null int64
    union       1260 non-null int64
    goodhlth    1260 non-null int64
    black       1260 non-null int64
    female      1260 non-null int64
    married     1260 non-null int64
    service     1260 non-null int64
    educ        1260 non-null int64
    looks       1260 non-null int64
    dtypes: float64(1), int64(9)
    memory usage: 98.6 KB
    

int64 и float64 — это типы признаков. Видим, что 1 признак — float64 и 9
признаков имеют тип int64.

Метод describe показывает основные статистические характеристики данных
по каждому числовому признаку (типы int64 и float64): число
непропущенных значений, среднее, стандартное отклонение, диапазон,
медиану, 0.25 и 0.75 квартили.

.. code:: python

    data.describe()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>count</th>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
          <td>1260.000000</td>
        </tr>
        <tr>
          <th>mean</th>
          <td>6.306690</td>
          <td>18.206349</td>
          <td>0.272222</td>
          <td>0.933333</td>
          <td>0.073810</td>
          <td>0.346032</td>
          <td>0.691270</td>
          <td>0.273810</td>
          <td>12.563492</td>
          <td>3.185714</td>
        </tr>
        <tr>
          <th>std</th>
          <td>4.660639</td>
          <td>11.963485</td>
          <td>0.445280</td>
          <td>0.249543</td>
          <td>0.261564</td>
          <td>0.475892</td>
          <td>0.462153</td>
          <td>0.446089</td>
          <td>2.624489</td>
          <td>0.684877</td>
        </tr>
        <tr>
          <th>min</th>
          <td>1.020000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>5.000000</td>
          <td>1.000000</td>
        </tr>
        <tr>
          <th>25%</th>
          <td>3.707500</td>
          <td>8.000000</td>
          <td>0.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>12.000000</td>
          <td>3.000000</td>
        </tr>
        <tr>
          <th>50%</th>
          <td>5.300000</td>
          <td>15.000000</td>
          <td>0.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>12.000000</td>
          <td>3.000000</td>
        </tr>
        <tr>
          <th>75%</th>
          <td>7.695000</td>
          <td>27.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>13.000000</td>
          <td>4.000000</td>
        </tr>
        <tr>
          <th>max</th>
          <td>77.720000</td>
          <td>48.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>17.000000</td>
          <td>5.000000</td>
        </tr>
      </tbody>
    </table>
    </div>



Посмотрим на признак “exper” - рабочий стаж

.. code:: python

    data['exper'].head()
    #data.exper.head() # 2-ой вариант




.. parsed-literal::

    0    30
    1    28
    2    35
    3    38
    4    27
    Name: exper, dtype: int64



Как описывалось ранее - тип данных в колонке является Series, что по
сути является проиндексированным массивом

.. code:: python

    type(data['exper'])




.. parsed-literal::

    pandas.core.series.Series



loc и iloc
----------

С помощью loc и iloc - можно из начального датафрейма зафиксировать
определённые интервал строк и интересующих столбцов и работать/смотреть
только их

.. code:: python

    #data.loc[1:5, ['wage']]
    data.wage.loc[1:5]




.. parsed-literal::

    1     4.28
    2     7.96
    3    11.57
    4    11.42
    5     3.91
    Name: wage, dtype: float64



.. code:: python

    #data.iloc[0,1] # первое число - номер столбца (начинается с 0). Второе - индекс строчки
    data['wage'].iloc[1:5]




.. parsed-literal::

    1     4.28
    2     7.96
    3    11.57
    4    11.42
    Name: wage, dtype: float64



Условия
-------

Посмотрим на наш датафрейм, на соответствие какому-то условию

.. code:: python

    (data['exper'] >= 15)




.. parsed-literal::

    0        True
    1        True
    2        True
    3        True
    4        True
            ...  
    1255     True
    1256    False
    1257     True
    1258     True
    1259     True
    Name: exper, Length: 1260, dtype: bool



Посмотрим только те строки, в датафрейме, которые удовлетворяют
определённому условию, и выведем первые 5 из них

.. code:: python

    data[(data['female'] == 1) & (data['black'] == 1)].head(10)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>44</th>
          <td>4.95</td>
          <td>20</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>14</td>
          <td>3</td>
        </tr>
        <tr>
          <th>85</th>
          <td>10.12</td>
          <td>40</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>10</td>
          <td>3</td>
        </tr>
        <tr>
          <th>110</th>
          <td>3.37</td>
          <td>36</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>13</td>
          <td>3</td>
        </tr>
        <tr>
          <th>148</th>
          <td>7.21</td>
          <td>20</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>17</td>
          <td>3</td>
        </tr>
        <tr>
          <th>167</th>
          <td>2.81</td>
          <td>14</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>13</td>
          <td>3</td>
        </tr>
        <tr>
          <th>211</th>
          <td>2.88</td>
          <td>7</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>13</td>
          <td>4</td>
        </tr>
        <tr>
          <th>497</th>
          <td>7.07</td>
          <td>8</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>13</td>
          <td>3</td>
        </tr>
        <tr>
          <th>499</th>
          <td>3.89</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>16</td>
          <td>4</td>
        </tr>
        <tr>
          <th>504</th>
          <td>6.54</td>
          <td>8</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>13</td>
          <td>3</td>
        </tr>
        <tr>
          <th>507</th>
          <td>7.69</td>
          <td>16</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>13</td>
          <td>3</td>
        </tr>
      </tbody>
    </table>
    </div>



Посмотрим только те строки, которые удовлетворяют условию и выведем
значение определённого столбца

.. code:: python

    data[data['female'] == 1]['wage'].head(10)




.. parsed-literal::

    0      5.73
    1      4.28
    2      7.96
    5      3.91
    8      5.00
    9      3.89
    10     3.45
    18    10.44
    19     7.69
    44     4.95
    Name: wage, dtype: float64



.. code:: python

    data[(data['female'] == 0) & (data['married'] == 1)].head(10)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>3</th>
          <td>11.57</td>
          <td>38</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>16</td>
          <td>3</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11.42</td>
          <td>27</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
        </tr>
        <tr>
          <th>6</th>
          <td>8.76</td>
          <td>12</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
        </tr>
        <tr>
          <th>11</th>
          <td>4.03</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>4</td>
        </tr>
        <tr>
          <th>12</th>
          <td>5.14</td>
          <td>19</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>17</td>
          <td>2</td>
        </tr>
        <tr>
          <th>14</th>
          <td>7.99</td>
          <td>12</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>4</td>
        </tr>
        <tr>
          <th>15</th>
          <td>6.01</td>
          <td>17</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>4</td>
        </tr>
        <tr>
          <th>16</th>
          <td>5.16</td>
          <td>7</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>17</td>
          <td>3</td>
        </tr>
        <tr>
          <th>17</th>
          <td>11.54</td>
          <td>12</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>17</td>
          <td>4</td>
        </tr>
        <tr>
          <th>21</th>
          <td>6.79</td>
          <td>19</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>3</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # Метод describe для сложного условия
    data[(data['female'] == 0) & (data['married'] == 1)].describe()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>count</th>
          <td>658.000000</td>
          <td>658.000000</td>
          <td>658.000000</td>
          <td>658.000000</td>
          <td>658.000000</td>
          <td>658.0</td>
          <td>658.0</td>
          <td>658.000000</td>
          <td>658.000000</td>
          <td>658.000000</td>
        </tr>
        <tr>
          <th>mean</th>
          <td>7.716778</td>
          <td>22.136778</td>
          <td>0.308511</td>
          <td>0.937690</td>
          <td>0.037994</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.194529</td>
          <td>12.495441</td>
          <td>3.164134</td>
        </tr>
        <tr>
          <th>std</th>
          <td>4.798763</td>
          <td>11.714753</td>
          <td>0.462230</td>
          <td>0.241902</td>
          <td>0.191327</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.396139</td>
          <td>2.716007</td>
          <td>0.655469</td>
        </tr>
        <tr>
          <th>min</th>
          <td>1.050000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.000000</td>
          <td>5.000000</td>
          <td>1.000000</td>
        </tr>
        <tr>
          <th>25%</th>
          <td>4.810000</td>
          <td>12.000000</td>
          <td>0.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.000000</td>
          <td>12.000000</td>
          <td>3.000000</td>
        </tr>
        <tr>
          <th>50%</th>
          <td>6.710000</td>
          <td>20.500000</td>
          <td>0.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.000000</td>
          <td>12.000000</td>
          <td>3.000000</td>
        </tr>
        <tr>
          <th>75%</th>
          <td>8.890000</td>
          <td>32.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.000000</td>
          <td>13.000000</td>
          <td>4.000000</td>
        </tr>
        <tr>
          <th>max</th>
          <td>41.670000</td>
          <td>48.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>1.000000</td>
          <td>17.000000</td>
          <td>5.000000</td>
        </tr>
      </tbody>
    </table>
    </div>



Посчитаем средние значения из тех данных, что удовлетворяют условию

.. code:: python

    data[data['female'] == 1]['wage'].mean(), data[data['female'] == 0]['wage'].mean() # .std, .min, .max, .count




.. parsed-literal::

    (4.299357798165136, 7.3688228155339734)



Вывод медианного значения, для данных, удовлетворяющих сложному условию

.. code:: python

    data[(data['female'] == 0) & (data['married'] == 1)]['wage'].median(), \
    data[(data['female'] == 0) & (data['married'] == 0)]['wage'].median()




.. parsed-literal::

    (6.710000000000001, 5.0649999999999995)



.. code:: python

    data['wage'].nunique()




.. parsed-literal::

    520



Ниже приводятся примеры использования метода groupby для отображения
информации по сгруппированному признаку

.. code:: python

    data.groupby('looks').wage.count()




.. parsed-literal::

    looks
    1     13
    2    142
    3    722
    4    364
    5     19
    Name: wage, dtype: int64



.. code:: python

    for look, sub_df in data.drop(['goodhlth'],axis=1).groupby('looks'):
        print(look)
        print(sub_df.head())
        print()


.. parsed-literal::

    1
          wage  exper  union  black  female  married  service  educ  looks
    28    8.35     41      0      0       0        1        1    16      1
    200   3.75     36      0      0       0        0        0    12      1
    248  10.99     40      0      0       0        1        0    12      1
    327   1.65     24      0      0       1        0        1    13      1
    751   7.93     39      1      0       0        1        0    12      1
    
    2
        wage  exper  union  black  female  married  service  educ  looks
    12  5.14     19      0      0       0        1        1    17      2
    33  8.17     18      0      0       0        1        0    16      2
    35  9.62     37      0      0       0        1        0    13      2
    37  7.69     10      1      0       0        1        0    13      2
    57  6.56     17      0      0       0        1        0    13      2
    
    3
        wage  exper  union  black  female  married  service  educ  looks
    1   4.28     28      0      0       1        1        0    12      3
    3  11.57     38      0      0       0        1        1    16      3
    4  11.42     27      0      0       0        1        0    16      3
    5   3.91     20      0      0       1        1        0    12      3
    6   8.76     12      0      0       0        1        0    16      3
    
    4
        wage  exper  union  black  female  married  service  educ  looks
    0   5.73     30      0      0       1        1        1    14      4
    2   7.96     35      0      0       1        0        0    10      4
    7   7.69      5      1      0       0        0        0    16      4
    10  3.45      3      0      0       1        0        0    12      4
    11  4.03      6      0      0       0        1        0    16      4
    
    5
          wage  exper  union  black  female  married  service  educ  looks
    26   14.84     29      0      0       0        0        1    13      5
    27   19.08     17      0      0       0        0        0    17      5
    76   23.32     15      0      0       0        1        1    17      5
    112   6.11      7      0      0       1        1        0    12      5
    316   3.92     12      0      0       0        1        1    12      5
    
    

.. code:: python

    for look, sub_df in data.groupby('looks'):
        print(look)
        print(sub_df['wage'].median())
        print()


.. parsed-literal::

    1
    3.46
    
    2
    4.595000000000001
    
    3
    5.635
    
    4
    5.24
    
    5
    4.81
    
    

.. code:: python

    for look, sub_df in data.groupby('looks'):
        print(look)
        print(round(sub_df['female'].mean(), 3))
        print()


.. parsed-literal::

    1
    0.385
    
    2
    0.38
    
    3
    0.323
    
    4
    0.374
    
    5
    0.421
    
    

.. code:: python

    for look, sub_df in data.groupby(['looks', 'female']):
        print(look)
        print(sub_df['goodhlth'].mean())
        print()


.. parsed-literal::

    (1, 0)
    0.75
    
    (1, 1)
    1.0
    
    (2, 0)
    0.9431818181818182
    
    (2, 1)
    0.9259259259259259
    
    (3, 0)
    0.9304703476482618
    
    (3, 1)
    0.9012875536480687
    
    (4, 0)
    0.9649122807017544
    
    (4, 1)
    0.9411764705882353
    
    (5, 0)
    1.0
    
    (5, 1)
    1.0
    
    

С помощью .agg метод groupby может применять различные функции к данным,
что он получает

.. code:: python

    data.groupby('looks')[['wage', 'exper']].max()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
        </tr>
        <tr>
          <th>looks</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td>10.99</td>
          <td>41</td>
        </tr>
        <tr>
          <th>2</th>
          <td>26.24</td>
          <td>45</td>
        </tr>
        <tr>
          <th>3</th>
          <td>38.86</td>
          <td>48</td>
        </tr>
        <tr>
          <th>4</th>
          <td>77.72</td>
          <td>47</td>
        </tr>
        <tr>
          <th>5</th>
          <td>23.32</td>
          <td>32</td>
        </tr>
      </tbody>
    </table>
    </div>



Декартово произведение признаков из столбцов и их отображение

.. code:: python

    pd.crosstab(data['female'], data['married'])




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th>married</th>
          <th>0</th>
          <th>1</th>
        </tr>
        <tr>
          <th>female</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>166</td>
          <td>658</td>
        </tr>
        <tr>
          <th>1</th>
          <td>223</td>
          <td>213</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    pd.crosstab(data['female'], data['looks'])




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th>looks</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
        </tr>
        <tr>
          <th>female</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>8</td>
          <td>88</td>
          <td>489</td>
          <td>228</td>
          <td>11</td>
        </tr>
        <tr>
          <th>1</th>
          <td>5</td>
          <td>54</td>
          <td>233</td>
          <td>136</td>
          <td>8</td>
        </tr>
      </tbody>
    </table>
    </div>



Создание нового признака из наложения дополнительных условий на основе
старых данных

.. code:: python

    data['exp'] = (data['exper'] >=15).astype(int)
    data.head(10)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
          <th>exp</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>5.73</td>
          <td>30</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>4</td>
          <td>1</td>
        </tr>
        <tr>
          <th>1</th>
          <td>4.28</td>
          <td>28</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
          <td>1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.96</td>
          <td>35</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
        </tr>
        <tr>
          <th>3</th>
          <td>11.57</td>
          <td>38</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>16</td>
          <td>3</td>
          <td>1</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11.42</td>
          <td>27</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
          <td>1</td>
        </tr>
        <tr>
          <th>5</th>
          <td>3.91</td>
          <td>20</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
          <td>1</td>
        </tr>
        <tr>
          <th>6</th>
          <td>8.76</td>
          <td>12</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
          <td>0</td>
        </tr>
        <tr>
          <th>7</th>
          <td>7.69</td>
          <td>5</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>16</td>
          <td>4</td>
          <td>0</td>
        </tr>
        <tr>
          <th>8</th>
          <td>5.00</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
          <td>0</td>
        </tr>
        <tr>
          <th>9</th>
          <td>3.89</td>
          <td>12</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
          <td>0</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    new = data[data['female'] == 1]
    new.to_csv('new.csv', index=False)
    new.head()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>5.73</td>
          <td>30</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>4</td>
        </tr>
        <tr>
          <th>1</th>
          <td>4.28</td>
          <td>28</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.96</td>
          <td>35</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>10</td>
          <td>4</td>
        </tr>
        <tr>
          <th>5</th>
          <td>3.91</td>
          <td>20</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
        </tr>
        <tr>
          <th>8</th>
          <td>5.00</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    data['wage'].sort_values(ascending=False).head(3)




.. parsed-literal::

    602    77.72
    269    41.67
    415    38.86
    Name: wage, dtype: float64



.. code:: python

    data['is_rich'] = (data['wage'] > data['wage'].quantile(.75)).astype('int64')

.. code:: python

    data['wage'].quantile(.75)




.. parsed-literal::

    7.695



.. code:: python

    data.head()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
          <th>exp</th>
          <th>is_rich</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>5.73</td>
          <td>30</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>4</td>
          <td>1</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>4.28</td>
          <td>28</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
          <td>1</td>
          <td>0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.96</td>
          <td>35</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
        </tr>
        <tr>
          <th>3</th>
          <td>11.57</td>
          <td>38</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>16</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11.42</td>
          <td>27</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    data['rubbish'] = .56 * data['wage'] + 0.32 * data['exper']
    data.head()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>wage</th>
          <th>exper</th>
          <th>union</th>
          <th>goodhlth</th>
          <th>black</th>
          <th>female</th>
          <th>married</th>
          <th>service</th>
          <th>educ</th>
          <th>looks</th>
          <th>exp</th>
          <th>is_rich</th>
          <th>rubbish</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>5.73</td>
          <td>30</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>4</td>
          <td>1</td>
          <td>0</td>
          <td>12.8088</td>
        </tr>
        <tr>
          <th>1</th>
          <td>4.28</td>
          <td>28</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>12</td>
          <td>3</td>
          <td>1</td>
          <td>0</td>
          <td>11.3568</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.96</td>
          <td>35</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>15.6576</td>
        </tr>
        <tr>
          <th>3</th>
          <td>11.57</td>
          <td>38</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>16</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
          <td>18.6392</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11.42</td>
          <td>27</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>16</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
          <td>15.0352</td>
        </tr>
      </tbody>
    </table>
    </div>



Домашнее задание будет во 2ой части
