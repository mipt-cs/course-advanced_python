Основы PyQt5
############

:date: 2021-03-30 09:00
:summary: Cоздание графических приложений, ч. 1


.. default-role:: code

.. contents:: Содержание

.. role:: python(code)
   :language: python

Введение
--------

.. _Qt5: https://doc.qt.io/qt-5/
.. _PyQt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/index.html
.. _PySide2: https://doc.qt.io/qtforpython-5/index.html

Qt5 — мощный кроссплатформенный фреймворк для разработки приложений с графическим интрефейсом. Qt5 является C++
библиотекой, а PyQt5 — ее python оберткой. В связи с этим большая часть документации по Qt5 поможет освоится с PyQt5.
Для более полного ознакомления с библиотекой оставлю ссылки на документацию Qt5_ и PyQt5_. Кроме PyQt5, есть пакет
PySide2_ от разработчиков Qt. В отличии от PyQt5, он поддерживает Python 2.7, и имеет пару небольших отличий от PyQt5.
Но в основном PySide2 и PyQt5 похожи, т.к. основаны на одной библиотеке, поэтому документация PySide2 тоже может
быть полезна.

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
`@pyqtSlot()` в PyQt5 или `@Slot()` в PySide2. Такое создание слотов слегка повышает производительность системы сигнал-слот. Декоратор позволяет указать
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
кнопки. Если разрабатываемый на питоне код будет импортирован в C++, при использовании декоратора важно указать
соответствующий тип данных.

Пользовательские сигналы
========================

Для создания сигналов используется функция `pyqtSignal()` в PyQt5 или `Signal()` в PySide2. Как и декоратор слота,
эта функция принимает информацию об аргументах. Сигналы имеют следующие особенности:

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

Обратите внимание на слот `show_info()`. При создании QMessageBox мы передаем self как аргумент. Тем самым мы явно
указываем, что предком является наше окно. В таком случае при открытии QMessageBox будет расположен по центру нашего
окна. Диалоговые окна являюстя модальными, т.е. блокируют все окна-предки.

*Примечание: в macOS есть некоторые особенности при создании диалоговых окон. В некоторых случаях модальность может не
работать, поэтому обращайтесь к документации.*

Упражнение №1
=============

Напишите программу, которая использует логин форму при запуске. Основное окно программы должно содержать какие-нибудь
виджеты, которые должны быть заблокированы, пока открыты любые диалоговые окна. При запуске основного окна запускается
окно логина. При верной паре логин/пароль появляется окно с уведомлением об успехе, после закрытия которого появляется
возможность работать с основным окном. При неверной паре появляется окно с уведомлением об ошибке и программа
завершается. Закрытие окна логина вручную приводит к завершению программы. Для создания логин формы успользуйте QDialog,
для окон с уведомлениями — QMessageBox.

*Дополнительно: после неверной пары программа не завершается, а дается возможность ввести логин/пароль заново.*

Базовая 2D графика
------------------

Часто приложения не ограничиваются набором базовых виджетов, которые отображают данные фиксированных типов. Иногда надо
отображать произвольные данные, например, видео или изображения. Также библиотека matplotlib должна как-то
отрисовывать построенные графики. Для этих целей Qt5 имеет ряд инструментов. Один из них QPainter, который предоставляет
API для векторной графики. Поверхностями для рисования являются объекты класса QPaintDevice. QWidget является
наследником этого класса и идеально подходит для отображения произвольных данных. Сам по себе QWidget имеет максимально
простой вид — просто чистое полотно, цвет — фон окна приложения. Сама отрисовка реализуется классом QPaintEngine,
который растеризует объекты перед их отрисовкой поверх виджетов.

Для примера попробуем написать своеобразный "генератор модерн арта", который позволит ознакомится с некоторыми основными
принципами работы с QPainter. Как было сказано выше, нам понадобится QPaintDevice. Для этого используем QWidget, от
которого мы отнаследуем свой виджет для отрисовки. Код мы вынесем в отдельный файл, чтобы не городить кучу кода в одном
файле.

.. code-block:: python

    from abc import ABC, abstractmethod
    import random
    import time

    from PyQt5.QtWidgets import QWidget
    # We need QtGui for drawing related classes
    # and QtCore for some non-widget classes
    from PyQt5 import QtGui, QtCore

    # Seed initialization with "random" number
    random.seed(time.time())


    class Shape(ABC):
        """
        Base class for shapes, that we want to draw
        """
        def __init__(self, x, y, pen, brush):
            self.x = x
            self.y = y
            self.pen = pen
            self.brush = brush

        @abstractmethod
        def draw(self, painter):
            painter.setPen(self.pen)
            painter.setBrush(self.brush)


    class Circle(Shape):
        def __init__(self, x, y):
            super().__init__(x, y,
                            QtGui.QPen(QtGui.QColor(0, 0, 0), 2),
                            QtGui.QBrush(QtGui.QColor(100, 200, 100)))

        def draw(self, painter):
            super().draw(painter)
            painter.drawEllipse(self.x, self.y, 20, 20)


    class Square(Shape):
        def __init__(self, x, y):
            super().__init__(x, y,
                            QtGui.QPen(QtGui.QColor(255, 0, 0)),
                            QtGui.QBrush(QtGui.QColor(255, 0, 0)))

        def draw(self, painter):
            super().draw(painter)
            painter.drawRect(self.x, self.y, 20, 20)


    class Triangle(Shape):
        def __init__(self, x, y):
            super().__init__(x, y,
                            QtGui.QPen(QtGui.QColor(0, 0, 0)),
                            QtGui.QBrush(QtGui.QColor(100, 200, 200)))

        def draw(self, painter):
            super().draw(painter)
            poly = QtGui.QPolygon([
                QtCore.QPoint(self.x, self.y),
                QtCore.QPoint(self.x + 10, self.y + 20),
                QtCore.QPoint(self.x - 10, self.y + 20)
            ])
            painter.drawPolygon(poly)


    class ImageWidget(QWidget):
        """
        This is our canvas-widget
        """
        def __init__(self):
            super().__init__()
            # Here we store all shapes, that need to be drawn
            self.__shapes = []

        def add_object(self, name):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            if name == "square":
                obj = Square(x, y)
            elif name == "circle":
                obj = Circle(x, y)
            elif name == "triangle":
                obj = Triangle(x, y)
            else:
                raise RuntimeError("unknown shape")
            self.__shapes.append(obj)
            self.update()

        def clear(self):
            self.__shapes = []
            self.update()

        # Actual drawing happens here
        def paintEvent(self, _):
            painter = QtGui.QPainter(self)
            for obj in self.__shapes:
                obj.draw(painter)

Как видно из предоставленного кода, для отрисовки используется специальный метод `paintEvent()`. Внутри этого метода
создается объект класса QPainter. QPainter принимает один аргумент — объект класса QPaintDevice. Важно знать, что
отрисовка на виджете не может происходить вне `paintEvent()`. Как можно заметить, `paintEvent()` кроме self принимает
еще один аргумент event, который позволяет узнать некоторые подробности события и управлять событием. Метод `update()`
запрашивает вызов `paintEvent()`, который будет вызван как только управление вернется в цикл событий. Теперь отрисовка
объектов. QPainter поддерживает ряд примитив, для которых есть специальные методы:

- drawArc — дуга;
- drawChord — хорда с отсеченной дугой;
- drawConvexPolygon — выпуклый многоугольник;
- drawEllipse — эллипс;
- drawLine — отрезок;
- drawPie — сектор;
- drawPoint — точка;
- drawPolygon — произвольный многоугольник;
- drawPolyline — ломаная;
- drawRect — прямоугольник.

На этом список не заканчивается, есть еще ряд примитив. Кроме того, QPainter поддерживает отрисовку глифов, картинок,
текста. Далее, обратите внимание на два класса: QPen и QBrush. QPen отвечает за стиль контуров и текста, а QBrush — за
заливку. По умолчанию заливка прозрачная, а контуры черные, толщиной в 1 пиксель. Заданные QPen и QBrush находятся в
памяти QPainter до их смены или удаления объекта QPainter. Для установки цвета используется класс QColor. Его
конструктор принимает аргументы в формате RGB, но сам по себе класс может работать и с другими цветовыми моделями
(CMYK, HSL, HSV). Последнее, что надо отметить, это система координат. Начало кординат расположено в левом верхнем углу,
ось абсцисс направлена вправо, ось ординат направлена вниз. При необходимости систему координат можно поменять при
помощи преобразований.

Чтобы наконец посмотреть, как работают хотя бы некоторые базовые вещи, перепишем код главного окна.

.. code-block:: python

    import sys
    from PyQt5 import QtWidgets
    # QtCore.Qt provides access to various flags, constants, etc.
    from PyQt5.QtCore import Qt
    # Don't forget to import your canvas-widget
    from imagewidget import ImageWidget


    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
            vlayout = QtWidgets.QVBoxLayout()
            widget = QtWidgets.QWidget()
            widget.setLayout(vlayout)
            self.setCentralWidget(widget)
            img_widget = ImageWidget()
            vlayout.addWidget(img_widget)
            hlayout = QtWidgets.QHBoxLayout()
            vlayout.addLayout(hlayout)
            button = QtWidgets.QPushButton("Square")
            button.pressed.connect(lambda: img_widget.add_object("square"))
            hlayout.addWidget(button)
            button = QtWidgets.QPushButton("Circle")
            button.pressed.connect(lambda: img_widget.add_object("circle"))
            hlayout.addWidget(button)
            button = QtWidgets.QPushButton("Triangle")
            button.pressed.connect(lambda: img_widget.add_object("triangle"))
            hlayout.addWidget(button)
            button = QtWidgets.QPushButton("Clear")
            button.pressed.connect(img_widget.clear)
            hlayout.addWidget(button)
            hlayout.addStretch()


    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)

        w = MainWindow()
        w.setWindowTitle("ModernArt generator")
        w.setFixedSize(300, 350)
        w.show()

        sys.exit(app.exec_())

Упражнение №2
=============

Напишите программу, которая будет отрисовывать график функции. Пусть вашей функцией будет полином какой-нибудь степени,
но не берите слишком большую степень. Программа должна поддерживать возможность изменения коэффициентов полинома прямо
во время работы программы. Например, я беру полином 5 степень, мне надо задавать 5 коэффициентов. Для этого можно
использовать 5 объектов QLineEdit (каждый под свой коэффициент), или один QLineEdit и перечислять коэффициенты через
запятую. Проявите фантазию. По нажатию кнопки OK программа должна отрисовать график для заданных коэффициентов.

*Дополнительно: используйте QSlider для изменения качества сглаживания вашего графика. Попробуйте поиграть с другими
функциями: синус, косинус, логарифм и тд.*
