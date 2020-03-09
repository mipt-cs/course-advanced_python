Основы PyQt5
############

:date: 2020-04-02 09:00
:summary: Cоздание графических приложений
:status: draft

.. default-role:: code

.. contents:: Содержание

.. role:: python(code)
   :language: python

Введение
--------

.. _Qt5: https://doc.qt.io/qt-5/
.. _PyQt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/index.html

Qt5 — мощный кроссплатформенный фреймворк для разработки приложений с графическим интрефейсом. Qt5 является C++
библиотекой, а PyQt5 — ее python оберткой. В связи с этим большая часть документации по Qt5 поможет освоится с PyQt5.
Для более полного ознакомления с библиотекой оставлю ссылки на документацию Qt5_ и PyQt5_. Кроме PyQt5, есть пакет
PySide2 от разработчиков Qt. В отличии от PyQt5, он поддерживает Python 2.7, и имеет пару небольших отличии от PyQt5.

Структура Qt5
=============

.. _модулей: https://doc.qt.io/qt-5/qtmodules.html

Вся библиотека разбита на множество модулей_. Некоторые из них:

+ Qt Core — базовые неграфические классы;
+ Qt GUI — базовые классы для создания графических приложений, 2D и 3D графика;
+ Qt Widgets — расширяет Qt GUI, добавляя большой набор основных виджетов (кнопки, полосы прокрутки и тд);
+ Qt Multimedia — работа с мультимедийными объектами (аудио, видео, радио, камера).

Для использования классов из того или иного модуля необходимо подключить конкретный модуль.

.. code-block:: python

    from PyQt5.QtWidgets import QPushButton

Создание Qt приложений
----------------------

Работа Qt приложений основана на цикле событий (event loop), для создания которого используются специальные классы:

+ QtCore.QCoreApplication — создает цикл событий для неграфических приложений;
+ QtGui.QGuiApplication — позволяет работать с графическими приложениями без использования виджетов (в Qt виджеты —
  не единственный способ создания графических приложений);
+ QtWidgets.QApplication — позволяет работать с графическими приложениями с использованием виджетов.

QCoreApplication является базовым классом, QGuiApplication наследует QCoreApplication, а QApplication наследует
QGuiApplication. Кроме цикла событий, QApplication управляет инициализацией и уничтожением виджетов. В данном курсе мы
будем работать с виджетами, поэтому для создания цикла событий используем QApplication. Приложения на основе QtWidgets
имеют нативный для ОС интерфейс, тем самым внешний вид элементов, рамок окна и т.д. будет меняться от одной ОС к другой.
Кроме того виджеты поддерживают настройку стилей, о чем будет рассказано на следующем занятии.

Разберем простой пример с QApplication.

.. code-block:: python

    import sys
    from PyQt5.QtWidgets import QApplication, QLabel

    if __name__ == "__main__":
        app = QApplication(sys.argv)

        label = QLabel("Hello, world!")
        label.setFixedWidth(200)
        label.show()

        sys.exit(app.exec_())

Перед созданием каких либо графических элементов мы всегда создаем объект QApplication, передавая ему список аргументов.
Список аргументов позволяет указать путь до файла конфигурации стилей и т.д. Далее мы создаем текстовый виджет и
выставляем его размер. Метод `show()` делает окно с виджетом видимым (такое необходимо делать только для основного
виджета, все остальные по умолчанию станут видимыми вместе с основным). Метод `exec_()` запускает цикл, который
завершится вместе с закрытием окна. При завершении цикла `exec_()` вернет код ошибки.

Компоновка виджетов
-------------------

В примере выше мы просто создали один текстовый виджет и использовали как окно приложения. Обычно приложения состоят из
множества виджетов, расположенных поверх других виджетов. Виджеты всегда можно располагать, опираясь на систему
координат. Но это далеко не всегда удобный способ. Для этих целей существуют возможность автоматической компоновки
виджетов при помощи классов-компоновщиков:

+ QFormLayout — расположение элементов в два столбца (как на логин-формах);
+ QGridLayout — расположение элементов сеткой;
+ QHBoxLayout — расположение элементов в строку;
+ QVBoxLayout — расположение элементов в столбец;
+ QStackedLayout — расположение элементов стеком, где видно только один элемент.

Попробуем использовать QVBoxLayout. Базовым виджетом используем QMainWindow. Это виджет с уникальной компоновкой
элементов. Хотя в этом примере мы не будем использовать ничего, кроме центрального виджета, вместо которого можно
подставить любой другой виджет.

.. image:: {static}/images/lab21/mainwindowlayout.png
   :align: center
   :alt: Main window layout

.. code-block:: python

    import sys
    from PyQt5 import QtWidgets


    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            layout = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel("Hello, world!")
            layout.addWidget(label)
            label = QtWidgets.QLabel("I'm a simple Qt5 app")
            layout.addWidget(label)
            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)


    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)

        w = MainWindow()
        w.setFixedWidth(200)
        w.show()

        sys.exit(app.exec_())

Здесь мы создали класс-наследник от QMainWindow. Мы могли просто создать все виджеты прямо в
`if __name__ == "__main__":` части, не создавая свои классы. Но это не хороший подход с точки зрения дизайна кода,
поэтому пусть класс MainWindow сам отвечает за создание объектов поверх него. Для того, чтобы установить компоновщик в
главное окно приложения, мы создали самый базовый виджет (QWidget — базовый класс для всех виджетов), установили в него
созданный компоновщик и сделали этот виджет центральным.

В случае QGridLayout метод `addWidget()` принимает дополнительно аргументы `row`, `column`, `rowSpan`, `columnSpan`.
Первые два аргумента указывают, в какую часть сетки помещается виджет. Причем компоновщик автоматически добавляет строки
и столбцы, если их еще нет. Оставшиеся аргументы указывают сколько строк и столбцов занимает добавляемый виджет
(по умолчанию, оба аргумента равны 1).

.. code-block:: python

    # QtCore.Qt provides access to various flags, constants, etc.
    from PyQt5.QtCore import Qt

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            layout = QtWidgets.QGridLayout()
            label = QtWidgets.QLabel("Hello, world!")
            layout.addWidget(label, 0, 0, 1, 2, Qt.AlignCenter)
            label = QtWidgets.QLabel("First text")
            layout.addWidget(label, 1, 0)
            label = QtWidgets.QLabel("Second text")
            layout.addWidget(label, 1, 1)
            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

QFormLayout для добавления элементов использует метод `addRow()`, который может принимать 2 аргумента: метку и виджет.
Сама метка может быть как просто строкой (виджет будет создан автоматически) или уже готовым виджетом. Если в `addRow()`
передать только один аргумент-виджет, то он будет растянут на два столбца.

.. code-block:: python

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            # Another example of using flags. Here we say that our window doesn't has default set of buttons,
            # but only minimize and close buttons.
            super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            layout = QtWidgets.QFormLayout()
            layout.addRow("Name:", QtWidgets.QLineEdit())
            layout.addRow("E-mail:", QtWidgets.QLineEdit())
            layout.addRow("Age:", QtWidgets.QSpinBox())
            layout.addRow(QtWidgets.QPushButton("OK"))
            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

Стоит отметить, что внутрь одного компановщика можно поместить другой. Для этого используется метод `addLayout()`. Не
забудьте про дополнительные аргументы для QGridLayout. QFormLayout все еще использует `addRow()`.

Сигналы и слоты
---------------

В примере выше мы добавили виджет-кнопку, однако при нажатии ничего не происходит. Давайте привяжем к кнопке
какое-нибудь действие. Для этих целей используется система сигналов и слотов. Сигнал — уведомление о том, что произошло
определенное событие. Слоты — это функции, которые запускаются при срабатывании сигнала. Для примера рассмотрим
упрощенную систему с телеграм-каналами. Когда админ канала отправляет туда сообщение (произошло событие), система
уведомляет (срабатывает сигнал) все аккаунты-подписчики. На каждом аккаунте срабатывает функция (слот), которая пушит
уведомления на все устройства, которые используют данный аккаунт. В Qt похожая идея. Большинство событий (нажатие
кнопки, изменение размера окна и т.д.) покрыты сигналами. Причем каждый объект имеет свой набор сигналов, т.е. нажатие
разных кнопок вызовет срабатывание разных сигналов. Что еще важно, это на каждый сигнал может быть несколько слотов.
Один слот может быть соединен с множеством сигналов. Кроме того, сигнал можно соединить с другим сигналом. На рисунке
ниже приведен возможный пример связей сигнал-слот между несколькими объектами.

.. image:: {static}/images/lab21/abstract-connections.png
   :align: center
   :alt: Abstract connections

Есть еще одно важное замечание: сигнал и связанные с ним слоты должны иметь одинаковую сигнатуру, в том числе типы
аргументов (с некоторыми допущениями). Но о типах чуть позже. Для начала все таки повесим на один из сигналов кнопки
слот.

.. code-block:: python

    class MainWindow(QtWidgets.QMainWindow):
        # Here we need QApplication object to use its slot as an example,
        # so don't forget to pass it as argument in MainWindow object creation.
        def __init__(self, app):
            super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            layout = QtWidgets.QFormLayout()
            layout.addRow("Name:", QtWidgets.QLineEdit())
            layout.addRow("E-mail:", QtWidgets.QLineEdit())
            layout.addRow("Age:", QtWidgets.QSpinBox())
            button = QtWidgets.QPushButton("OK")
            button.pressed.connect(app.aboutQt)
            layout.addRow(button)
            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

Тут мы использовали слот класса QApplication. Сами по себе слоты ведут себя как обычные функции, и могут быть вызваны
вручную.

Пользовательские слоты
======================

В python сигнал также можно соединить с обычной функцией.

.. code-block:: python

    button.pressed.connect(lambda: print("OK"))

Давайте используем в этом примере для слота более осмысленную функцию. Перепишем класс MainWindow.

.. code-block:: python

    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            layout = QtWidgets.QFormLayout()
            self.name = QtWidgets.QLineEdit()
            self.email = QtWidgets.QLineEdit()
            self.age = QtWidgets.QSpinBox()
            layout.addRow("Name:", self.name)
            layout.addRow("E-mail:", self.email)
            layout.addRow("Age:", self.age)
            button = QtWidgets.QPushButton("OK")
            button.pressed.connect(self.process)
            layout.addRow(button)
            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

        def process(self):
            print("Your name is {}".format(self.name.text()))
            print("Your email is {}".format(self.email.text()))
            print("Your age is {}".format(self.age.text()))

Методы классов тоже можно использовать как слоты. Более того, слоты можно создавать в явном виде при помощи декортатора
`@pyqtSlot()`. Такое создание слотов слегка повышает производительность системы сигнал-слот. Декоратор позволяет указать
сколько аргументов принимает слот, их типы и возращаемый тип (аргумент декортатора `result`).

.. code-block:: python

    from PyQt5.QtCore import Qt, pyqtSlot
    ...
    @pyqtSlot()
    def process(self):...

Давайте создадим еще один слот с непустым списком аргументов и соединим его с другим сигналом кнопки.

.. code-block:: python

    def __init__(self):
        ...
        button.clicked.connect(f)


    @pyqtSlot(bool)
    def f(value):
        print(value)

Сигнал `clicked` посылает информацию о том, была ли поставлена на кнопку галочка (см. рисунок).

.. image:: {static}/images/lab21/windows-checkbox.png
   :align: center
   :alt: Checkbox

Для обычных кнопок состояние всегда `False`. Однако, слот может получить информацию об этом состоянии или
проигнорировать его. Например, соединив с этим сигналом слот без аргументов, ничего не сломается, просто в слот не
придет информация о состоянии кнопки. Если использовать слот с одним аргументом, то в этом аргументе будет состояние
кнопки. Если разрабатываемый на  питоне код будет импортирован в C++, при использовании декоратора важно указать
соотвествующий тип данных.

Пользовательские сигналы
========================

Для создания сигналов используется функция `pyqtSignal()`. Как и декоратор `@pyqtSlot()`, эта функция принимает
информацию об аргументах. Сигналы имеют следующие особенности:

+ Они ничего не возвращают, т.к. это не функции.
+ Сигналами могут быть атрибуты класса, отнаследованного от QObject (все виджеты происходят от него).

Давайте попробуем создать и использовать свой сигнал.

.. code-block:: python

    from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal


    class MainWindow(QtWidgets.QMainWindow):
        processed = pyqtSignal(str)

        def __init__(self):
            super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            layout = QtWidgets.QFormLayout()
            self.name = QtWidgets.QLineEdit()
            self.email = QtWidgets.QLineEdit()
            self.age = QtWidgets.QSpinBox()
            layout.addRow("Name:", self.name)
            layout.addRow("E-mail:", self.email)
            layout.addRow("Age:", self.age)
            button = QtWidgets.QPushButton("OK")
            button.pressed.connect(self.process)
            layout.addRow(button)
            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)
            self.processed.connect(self.show_info)

        @pyqtSlot()
        def process(self):
            res = "Your name is {}.\n" \
                "Your email is {}.\n" \
                "Your age is {}.".format(
                    self.name.text(),
                    self.email.text(),
                    self.age.text()
                )
            self.processed.emit(res)

        @pyqtSlot(str)
        def show_info(self, info):
            msg = QtWidgets.QMessageBox(self)
            msg.setText(info)
            msg.setWindowTitle("Welcome")
            msg.exec_()

Для вызова сигнала используется метод `emit()`, в который передаются необходимые аргументы. Далее эти аргументы будут
переданы слотам, при их вызове. Слоты вызываются в том порядке, в котором они были присоединены. К тому же
присоединенные слоты можно отсоединять методом `disconnect()`. Для этого надо передать в него либо функцию, с которой
установлено соединение, либо объект соединения, который возвращается в результате `connect()`. Если никакой слот не
указан, `disconnect()` обрывает все соединения.

Базовая 2D графика
------------------

Часто приложения не ограничиваются набором базовых виджетов, которые отображают данные фиксированных типов. Иногда надо
отображать более произвольные данные, например, видео или изображения. Так, библиотека matplotlib должна как-то
отрисовывать построенные графики. Для этих целей Qt5 имеет ряд инструментов. Один из них QPainter, который предоставляет
API для векторной графики. Поверхностями для рисования являются объекты класса QPainterDevice. QWidget является
наследником этого класса и идеально подходит для отображения произвольных данных. Сам по себе QWidget имеет максимально
простой вид — просто чистое полотно, цвет — фон окна приложения. Сама отрисовка реализуется классом QPaintEngine,
который растеризует объекты перед их отрисовкой поверх виджетов.

.. todo:
    draw example + task for it
