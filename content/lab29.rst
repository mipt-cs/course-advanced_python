Проверка гипотез и анализ правдоподобия
###############################################

:date: 2022-04-18 09:00
:summary: Классические методы машинного обучения, ч.2, модуль scikit-learn


.. default-role:: code

.. contents:: Содержание

.. role:: python(code)
   :language: python


* использованы материалы курса https://github.com/Intelligent-Systems-Phystech/psad

Введение. Библиотека statsmodels
==================================

В python для всевозможных задач статистического оценивания используется стандартная библиотека `statsmodels <https://www.statsmodels.org/dev/examples/index.html>`_
Раньше была частью scipy , выделилась в самостоятельную, чтоб сделать основным объектом классы статистических моделей. Например , `OLS - ordinary least squares <https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html#statsmodels.regression.linear_model.OLS>`_ , 
`WLS - weighted least squares <https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.WLS.html#statsmodels.regression.linear_model.WLS>`_ , 
`RecursiveLS <https://www.statsmodels.org/dev/generated/statsmodels.regression.recursive_ls.RecursiveLS.html#statsmodels.regression.recursive_ls.RecursiveLS>`_ 

Для описания матриц плана (**design matrices**) в ней используется библиотека `patsy <https://patsy.readthedocs.io/en/latest/categorical-coding.html>`_

Пример
+++++++

Код к примеру_

.. _примеру: {static}/extra/lab29/statsexample.ipynb

Пример использует так называемые `данные Герри <https://vincentarelbundock.github.io/Rdatasets/doc/HistData/Guerry.html>`_ по социальной статистике во Франции в 1830х. 

.. code-block:: ipython3

    df = sm.datasets.get_rdataset("Guerry", "HistData").data

.. code-block:: ipython3

    df.describe()


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
          <th>dept</th>
          <th>Crime_pers</th>
          <th>Crime_prop</th>
          <th>Literacy</th>
          <th>Donations</th>
          <th>Infants</th>
          <th>Suicides</th>
          <th>Wealth</th>
          <th>Commerce</th>
          <th>Clergy</th>
          <th>Crime_parents</th>
          <th>Infanticide</th>
          <th>Donation_clergy</th>
          <th>Lottery</th>
          <th>Desertion</th>
          <th>Instruction</th>
          <th>Prostitutes</th>
          <th>Distance</th>
          <th>Area</th>
          <th>Pop1831</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>count</th>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
        </tr>
        <tr>
          <th>mean</th>
          <td>46.883721</td>
          <td>19754.406977</td>
          <td>7843.058140</td>
          <td>39.255814</td>
          <td>7075.546512</td>
          <td>19049.906977</td>
          <td>36522.604651</td>
          <td>43.500000</td>
          <td>42.802326</td>
          <td>43.430233</td>
          <td>43.500000</td>
          <td>43.511628</td>
          <td>43.500000</td>
          <td>43.500000</td>
          <td>43.500000</td>
          <td>43.127907</td>
          <td>141.872093</td>
          <td>207.953140</td>
          <td>6146.988372</td>
          <td>378.628721</td>
        </tr>
        <tr>
          <th>std</th>
          <td>30.426157</td>
          <td>7504.703073</td>
          <td>3051.352839</td>
          <td>17.364051</td>
          <td>5834.595216</td>
          <td>8820.233546</td>
          <td>31312.532649</td>
          <td>24.969982</td>
          <td>25.028370</td>
          <td>24.999549</td>
          <td>24.969982</td>
          <td>24.948297</td>
          <td>24.969982</td>
          <td>24.969982</td>
          <td>24.969982</td>
          <td>24.799809</td>
          <td>520.969318</td>
          <td>109.320837</td>
          <td>1398.246620</td>
          <td>148.777230</td>
        </tr>
        <tr>
          <th>min</th>
          <td>1.000000</td>
          <td>2199.000000</td>
          <td>1368.000000</td>
          <td>12.000000</td>
          <td>1246.000000</td>
          <td>2660.000000</td>
          <td>3460.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>1.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>762.000000</td>
          <td>129.100000</td>
        </tr>
        <tr>
          <th>25%</th>
          <td>24.250000</td>
          <td>14156.250000</td>
          <td>5933.000000</td>
          <td>25.000000</td>
          <td>3446.750000</td>
          <td>14299.750000</td>
          <td>15463.000000</td>
          <td>22.250000</td>
          <td>21.250000</td>
          <td>22.250000</td>
          <td>22.250000</td>
          <td>22.250000</td>
          <td>22.250000</td>
          <td>22.250000</td>
          <td>22.250000</td>
          <td>23.250000</td>
          <td>6.000000</td>
          <td>121.383000</td>
          <td>5400.750000</td>
          <td>283.005000</td>
        </tr>
        <tr>
          <th>50%</th>
          <td>45.500000</td>
          <td>18748.500000</td>
          <td>7595.000000</td>
          <td>38.000000</td>
          <td>5020.000000</td>
          <td>17141.500000</td>
          <td>26743.500000</td>
          <td>43.500000</td>
          <td>42.500000</td>
          <td>43.500000</td>
          <td>43.500000</td>
          <td>43.500000</td>
          <td>43.500000</td>
          <td>43.500000</td>
          <td>43.500000</td>
          <td>41.500000</td>
          <td>33.000000</td>
          <td>200.616000</td>
          <td>6070.500000</td>
          <td>346.165000</td>
        </tr>
        <tr>
          <th>75%</th>
          <td>66.750000</td>
          <td>25937.500000</td>
          <td>9182.250000</td>
          <td>51.750000</td>
          <td>9446.750000</td>
          <td>22682.250000</td>
          <td>44057.500000</td>
          <td>64.750000</td>
          <td>63.750000</td>
          <td>64.750000</td>
          <td>64.750000</td>
          <td>64.750000</td>
          <td>64.750000</td>
          <td>64.750000</td>
          <td>64.750000</td>
          <td>64.750000</td>
          <td>113.750000</td>
          <td>289.670500</td>
          <td>6816.500000</td>
          <td>444.407500</td>
        </tr>
        <tr>
          <th>max</th>
          <td>200.000000</td>
          <td>37014.000000</td>
          <td>20235.000000</td>
          <td>74.000000</td>
          <td>37015.000000</td>
          <td>62486.000000</td>
          <td>163241.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>86.000000</td>
          <td>4744.000000</td>
          <td>539.213000</td>
          <td>10000.000000</td>
          <td>989.940000</td>
        </tr>
      </tbody>
    </table>
    </div>

Удалим строки с пустыми значениями с помощью dropna()

.. code-block:: ipython3

    vars = ['Department', 'Lottery', 'Literacy', 'Wealth', 'Region']

.. code-block:: ipython3

    df = df.dropna()[vars]
    df[-5:]

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
          <th>Department</th>
          <th>Lottery</th>
          <th>Literacy</th>
          <th>Wealth</th>
          <th>Region</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>80</th>
          <td>Vendee</td>
          <td>68</td>
          <td>28</td>
          <td>56</td>
          <td>W</td>
        </tr>
        <tr>
          <th>81</th>
          <td>Vienne</td>
          <td>40</td>
          <td>25</td>
          <td>68</td>
          <td>W</td>
        </tr>
        <tr>
          <th>82</th>
          <td>Haute-Vienne</td>
          <td>55</td>
          <td>13</td>
          <td>67</td>
          <td>C</td>
        </tr>
        <tr>
          <th>83</th>
          <td>Vosges</td>
          <td>14</td>
          <td>62</td>
          <td>82</td>
          <td>E</td>
        </tr>
        <tr>
          <th>84</th>
          <td>Yonne</td>
          <td>51</td>
          <td>47</td>
          <td>30</td>
          <td>C</td>
        </tr>
      </tbody>
    </table>
    </div>

Постановка задачи
+++++++++++++++++++

Будет использоваться модель обычного метода наименьших квадратов OLS. Решается задача регрессии лотерейных ставок в королевской лотерее Франции в 1820х против показателей грамотности с учётом материального достатка населения. При этом в правой части регерессионного уравнения придётся учитывать "пустые" переменные, которые тем не менее вносят неоднородность в данные по департаментам. 

План-матрицы
+++++++++++++++

Для большинства моделей из statsmodels придётся определить 2 план-матрицы - для зависимых (endogenous, response, dependent) и независимых (exogenous, independent, predictor, regressor) переменных. Регрессионные МНК коэффиценты вычисляются как обычно:

.. math::

   \beta = (X^T X)X^T y


где y имеет размер N * 1  - это данные из столбца Lottery 
X размера N * 7  - столбцы Wealth , Literacy и 4 бинарных, отвечающих за регионы. 

Используется функция dmatrices библиотеки patsy для формирования план-матриц регрессионных моделей. Там используется синтаксис языка R . 

.. code-block:: ipython3

    y, X = dmatrices('Lottery ~ Literacy + Wealth + Region', data=df, return_type='dataframe')


.. code-block:: ipython3

    y




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
          <th>Lottery</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>41.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>38.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>66.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>80.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>79.0</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
        </tr>
        <tr>
          <th>80</th>
          <td>68.0</td>
        </tr>
        <tr>
          <th>81</th>
          <td>40.0</td>
        </tr>
        <tr>
          <th>82</th>
          <td>55.0</td>
        </tr>
        <tr>
          <th>83</th>
          <td>14.0</td>
        </tr>
        <tr>
          <th>84</th>
          <td>51.0</td>
        </tr>
      </tbody>
    </table>
    <p>85 rows × 1 columns</p>
    </div>



.. code-block:: ipython3

    X




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
          <th>Intercept</th>
          <th>Region[T.E]</th>
          <th>Region[T.N]</th>
          <th>Region[T.S]</th>
          <th>Region[T.W]</th>
          <th>Literacy</th>
          <th>Wealth</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>37.0</td>
          <td>73.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>51.0</td>
          <td>22.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>13.0</td>
          <td>61.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>1.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>46.0</td>
          <td>76.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>1.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>69.0</td>
          <td>83.0</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>80</th>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>28.0</td>
          <td>56.0</td>
        </tr>
        <tr>
          <th>81</th>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>25.0</td>
          <td>68.0</td>
        </tr>
        <tr>
          <th>82</th>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>13.0</td>
          <td>67.0</td>
        </tr>
        <tr>
          <th>83</th>
          <td>1.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>62.0</td>
          <td>82.0</td>
        </tr>
        <tr>
          <th>84</th>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>47.0</td>
          <td>30.0</td>
        </tr>
      </tbody>
    </table>
    <p>85 rows × 7 columns</p>
    </div>


Важно заметить, что dmatrices 

- разделила Region на несколько индикаторных признаков ({1,0})
- добавила константу к независимым переменным (exogenous)
- возвращает pandas dataframe вместо обычного numpy array и позволяет сохранять описательные данные. 

Типичная последовательность действий
++++++++++++++++++++++++++++++++++++++++

Как правило работа со statsmodels состоит из 3 этапов :

1. выбор класса статистических моделей
2. обучение модели с помощью соответствующего метода
3. изучеие полученных коэффицентов с помощью summary()

Для МНК (OLS) это выглядит так:

.. code-block:: ipython3

    mod = sm.OLS(y, X)    # Describe model
    res = mod.fit()       # Fit model
    print(res.summary())   # Summarize model, like df.describe() 


.. parsed-literal::

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                Lottery   R-squared:                       0.338
    Model:                            OLS   Adj. R-squared:                  0.287
    Method:                 Least Squares   F-statistic:                     6.636
    Date:                Tue, 12 Apr 2022   Prob (F-statistic):           1.07e-05
    Time:                        02:44:16   Log-Likelihood:                -375.30
    No. Observations:                  85   AIC:                             764.6
    Df Residuals:                      78   BIC:                             781.7
    Df Model:                           6                                         
    Covariance Type:            nonrobust                                         
    ===============================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
    -------------------------------------------------------------------------------
    Intercept      38.6517      9.456      4.087      0.000      19.826      57.478
    Region[T.E]   -15.4278      9.727     -1.586      0.117     -34.793       3.938
    Region[T.N]   -10.0170      9.260     -1.082      0.283     -28.453       8.419
    Region[T.S]    -4.5483      7.279     -0.625      0.534     -19.039       9.943
    Region[T.W]   -10.0913      7.196     -1.402      0.165     -24.418       4.235
    Literacy       -0.1858      0.210     -0.886      0.378      -0.603       0.232
    Wealth          0.4515      0.103      4.390      0.000       0.247       0.656
    ==============================================================================
    Omnibus:                        3.049   Durbin-Watson:                   1.785
    Prob(Omnibus):                  0.218   Jarque-Bera (JB):                2.694
    Skew:                          -0.340   Prob(JB):                        0.260
    Kurtosis:                       2.454   Cond. No.                         371.
    ==============================================================================
    
    Notes:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.


.. code-block:: ipython3

    res.params




.. parsed-literal::

    Intercept      38.651655
    Region[T.E]   -15.427785
    Region[T.N]   -10.016961
    Region[T.S]    -4.548257
    Region[T.W]   -10.091276
    Literacy       -0.185819
    Wealth          0.451475
    dtype: float64



.. code-block:: ipython3

    res.rsquared




.. parsed-literal::

    0.3379508691928823


Анализ и визуализация результатов
++++++++++++++++++++++++++++++++++++

statsmodels содержит также много `тестов <https://www.statsmodels.org/dev/stats.html#residual-diagnostics-and-specification-tests>`_ для оценки качества поолученной (обученной) статистической модели.

И инструменты для отрисовки графиков приближений модели.

.. code-block:: ipython3

    sm.graphics.plot_partregress('Lottery', 'Wealth', ['Region', 'Literacy'],
       ....:                              data=df, obs_labels=False)

.. image:: {static}/extra/lab29/Untitled2_files/Untitled2_12_1.png

.. image:: {static}/extra/lab29/Untitled2_files/Untitled2_12_2.png


Множественная проверка гипотез
==================================

Слайды__

__ {static}/extra/lab29/lecture_4_mht.pdf

jupyter-notebook__

__ {static}/extra/lab29/sem4/main.ipynb




Анализ зависимостей
=======================

Слайды__

__ {static}/extra/lab29/lecture_5_corr.pdf

jupyter-notebook__

__ {static}/extra/lab29/sem5/main.ipynb


Причинность и Байесовы методы
===============================

Слайды__

__ {static}/extra/lab29/l_11_caus.pdf

jupyter-notebook__

__ {static}/extra/lab29/sem11/main.ipynb
