PyQt5: многопоточность GUI программ и дизайн интерфейса
#######################################################

:date: 2020-04-09 09:00
:summary: Cоздание графических приложений, ч.2
:status: draft

.. default-role:: code

.. contents:: Содержание

.. role:: python(code)
   :language: python

Полезные ссылки
---------------

.. _Qt5: https://doc.qt.io/qt-5/
.. _PyQt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/index.html
.. _PySide2: https://doc.qt.io/qtforpython-5/index.html

Напомню, что полезно обращаться к документации библиотеки: Qt5_, PyQt5_, PySide2_.

Уничтожение объектов
--------------------

Прежде чем перейти к рассмотрению основных тем, остановимся на вопросе уничтожения объектов. Вы знаете, что когда для
какого-либо объекта счетик ссылок станет равным нулю, объект будет уничтожен сборщиком мусора. Иногда, при уничтожении
объекта, нам надо освобождать ресурсы. И кажется, что для этих целей можно использовать магический метод `__del__`,
который вызывается при уничтожении объекта. Отчасти это не так. Разработчики питона не гарантируют вызов этого метода
для объектов, которые были живы на момент завершения интерпретатора. Что еще хуже, мы работаем с C++ библиотекой. C++
объекты живут отдельной жизнью, мы же с вами работаем с Python оберткой. Когда мы закрываем приложение, то все объкты
должны быть уничтожены, QCoreApplication в том числе. Однако QCoreApplication должен быть уничтожен после того, как
уничтожены все объекты QObject. Тем самым уничтожение QCoreApplication объекта спровоцирует уничтожение других QObject
объектов. Но это касается только C++ объектов, Python обертка все еще может жить. И когда дело дойдет до ее уничтожения,
`__del__()` может обратиться к объектам, которые уже были уничтожены, что приведет к падению программы. Поэтому, при
работе с Qt используйте сигнал `destroyed`, который есть у QObject. Этот сигнал срабатывает непосредственно перед
удалением C++ объекта, что позволит корректно освободить ресурсы. Но и тут есть один момент. С этим сигналом нельзя
связать метод этого же класса (что логично, т.к. происходит удаление этого самого объекта).
Но можно связать лямбда-функцию, которая освобождает ресурсы.

Типы соединения
---------------

Сегодня мы будем работать с несколькими потоками и не можем не затронуть подробности в системе сигналов и слотов. До
этого мы соединяли сигналы со слотами, не указывая никаких аргументов. На самом деле `connect()` принимает еще один
аргумент, способ соединения. Их всего пять:

+ AutoConnection
+ DirectConnection
+ QueuedConnection
+ BlockingQueuedConnection
+ UniqueConnection

Прямое соединение гарантирует мгновенное срабатывание слота в том потоке, где был вызван сигнал (считайте, что в этом
случае идет простой вызов слота как обычной функции). Соединение с очередью ставит исполнение слота в очередь. Слот
будет выполнен, как только управление вернется в цикл событий. Все это происходит в потоке, где живет объект-приемник.
Блокирующее соединение с очередью отличается тем, `emit()` блокирует исполнение потока до тех пор, пока слот не завершит
работу. Этот тип соединения должен быть использован, только если приемник живет в отдельном потоке от сигнализирующего
потока. По умолчанию используется автоматический способ. Если приемник живет в потоке, откуда исходит сигнал, то
соединение работает по типу `DirectConnection`, иначе по типу `QueuedConnection`. Тип соединения определяется каждый раз
при срабатывании сигнала. `UniqueConnection` используется вместе с любым другим типом. Он позволяет позволяет создать
уникальное соединение, чтобы избежать дубликатов. Без него один и тот же сигнал может быть соединен с одним и тем же
слотом несколько раз.

Многопоточность
---------------

В предыдущей лабе мы рассматривали программы, где не было каких-либо долгих вычислений или операций. Но вы с этим могли
столкнуться при решениий дополнительной части задания №2. Если вы поставите высокое качество (т.е. будете генерировать
большое кол-во дополнительных точек для построения графика), программе потребуется некоторе время на проведение всех
вычислений. И на это время программа перестанет отвечать на запросы (нажатие на кнопки мышью и т.д.). Рассмотрим другой
пример. Ниже представлена программа, в которой есть две кнопки. Start запускает длительный процесс (в данном примере
просто итерация в цикле с записью в файл), About открывает окно "About Qt". При нажатии на Start вы запустите цикл
(прогресс можно увидеть в QProgressBar). Пока идет работа цикла, попробуйте нажать на кнопку About. Программа просто
не реагирует на ваши запросы, даже на попытки закрыть окно.

.. code-block:: python

   import sys
   from PyQt5 import QtWidgets
   from PyQt5.QtCore import Qt, pyqtSignal

   MAX_ITER = 1000000


   class MainWindow(QtWidgets.QMainWindow):
      iteration_passed = pyqtSignal(int)

      def __init__(self):
         super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
         vlayout = QtWidgets.QVBoxLayout()
         widget = QtWidgets.QWidget()
         widget.setLayout(vlayout)
         self.setCentralWidget(widget)
         self.bar = QtWidgets.QProgressBar()
         self.bar.setMinimum(0)
         self.bar.setMaximum(MAX_ITER)
         self.iteration_passed.connect(self.bar.setValue)
         vlayout.addWidget(self.bar)
         self.button = QtWidgets.QPushButton("Start")
         self.button.pressed.connect(self.process)
         vlayout.addWidget(self.button)
         button = QtWidgets.QPushButton("About")
         button.pressed.connect(app.aboutQt)
         vlayout.addWidget(button)

      def process(self):
         self.button.setDisabled(True)
         with open("out.txt", "w") as f:
               for i in range(MAX_ITER):
                  f.write("{}\n".format(i))
                  self.iteration_passed.emit(i+1)
         self.button.setDisabled(False)


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.setFixedSize(300, 150)
      w.show()

      sys.exit(app.exec_())

На самом деле ваши запросы отправляются в очередь событий и будут обработаны, когда управление верентся в цикл событий.
Становится понятно, что цикл событий, в котором обрабатываются запросы на работу с интерфейсом, не должен нагружаться
такими длительными операциями. Здесь в работу вступает многопоточность. Как вам было рассказано в предыдущем семестре,
одним из назначений многопоточности является отделение длительных операций от работы графического интерфейса приложений.
Python и PyQt5 предоставляют ряд способов для решения представленной выше проблемы. Каждый из способов имеет свои
плюсы и минусы.

QThread
=======

Первый способ — просто создать отдельный поток, и запустить его в исполнение. Для этого используется класс QThread. Да,
мы могли бы использовать класс Thread из библиотеки threading. Однако, QThread является наследником QObject, что
позволяет нам использовать главную фишку Qt5 — сигналы и слоты. На самом деле внутри все равно используется одинаковый
механизм работы с потоками, который зависит от операционной системы, QThread и Thread — просто обертка над этим
механизмом. Основной код, который будет выполняться в потоке, пишется в виде тела метода `run()`. Этот метод будет
вызван автоматически, когда вы запустите работу потока. Важным моментом в использовании потоков является способ их
останова. QThread имеет метод `terminate()`, который принудительно завершает работу потока. Однако, его использование в
общем случае не одобряется, т.к. после такого могут оказаться неразблокированные мьютексы, неосвобожденные ресурсы,
частично записанные (а значит испорченные) участки памяти. Второй механизм останова — методы `requestInterruption()` и
`isInterruptionRequested()`. Первый выставляет флаг, который говорит, что пора завершать работу. Второй возвращает
значение этого флага. Тем самым для цикла внутри `run()` одним из критериев останова будет равенство этого флага True,
т.е. пора завершать работу. Третий подход — методы `exit()` и `quit()`, которые используются при работе потока с циклом
событий. Для того, чтобы дождаться завершения потока, используйте метод `wait()`.

.. code-block:: python

   import sys
   from PyQt5 import QtWidgets
   from PyQt5.QtCore import Qt, QThread, pyqtSignal

   MAX_ITER = 1000000


   class Processor(QThread):
      iteration_passed = pyqtSignal(int)
      status_changed = pyqtSignal(bool)

      def run(self):
         self.status_changed.emit(True)
         with open("out.txt", "w") as f:
               i = 0
               while not self.isInterruptionRequested() and i < MAX_ITER:
                  f.write("{}\n".format(i))
                  i += 1
                  self.iteration_passed.emit(i + 1)
         self.status_changed.emit(False)


   class MainWindow(QtWidgets.QMainWindow):
      process = Signal()

      def __init__(self):
         super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
         vlayout = QtWidgets.QVBoxLayout()
         widget = QtWidgets.QWidget()
         widget.setLayout(vlayout)
         self.setCentralWidget(widget)
         self.bar = QtWidgets.QProgressBar()
         self.bar.setMinimum(0)
         self.bar.setMaximum(MAX_ITER)
         self.bar.setValue(0)
         vlayout.addWidget(self.bar)
         self.button = QtWidgets.QPushButton("Start")
         self.button.pressed.connect(self.process)
         vlayout.addWidget(self.button)
         button = QtWidgets.QPushButton("About")
         button.pressed.connect(app.aboutQt)
         vlayout.addWidget(button)
         self.processor = Processor(self)
         self.process.connect(self.processor.start)
         self.processor.iteration_passed.connect(self.bar.setValue, Qt.DirectConnection)
         self.processor.status_changed.connect(self.button.setDisabled)
         self.processor.finished.connect(lambda: self.bar.setValue(0))
         self.destroyed.connect(self.processor.requestInterruption)
         self.destroyed.connect(self.processor.wait)


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.setFixedSize(300, 150)
      w.show()

      sys.exit(app.exec_())

Прежде чем перейти к другим способам, необходимо рассмотреть несколько важных моментов в примере выше. Первое — метод
`cleanup()`. Помните, что потоки — это ресурсы, которые необходимо освобождать корректно. В случае Qt, за поток отвечает
объект класса QThread. Как только объект будет уничтожен, то работа потока будет завершена принудительно. Ситуация
примерно такая же, как с методом `terminate()`. Даже если бы исполнение потока не прекращалось бы, объект QThread (а
значит и QObject часть) все равно был бы уничтожен. Тогда видимый из этого потока self указывал бы на уже освобожденную
память, да и сигналы не могут работать без QObject. Данный метод показывает пример освобождения ресурсов при уничтожении
C++ объекта, как было рассказано выше.

Второе — соединение сигнала `iteration_passed`. В примере выше мы используем прямое соединение, чтобы вызывать
обновление полосы прогресса непосредственно в нашем отдельном потоке. Иначе частые запросы просто заспамят очередь
запросов в основном потоке, и мы получим похожую проблему, чтобы была до разделения программы на два потока. Для
теста попробуйте убрать этот аргумент и посмотрите на результат.

Worker-object approach
======================

Подход с наследованием QThread имеет большой минус — созданный объект такого класса принадлежит тому потоку, в котором
он был создан. Соответственно, все его слоты будут выполняться в этом самом потоке. Если необходимо перенести выполнение
слотов в новый поток, за который отвечает наш объект, то нужно использовать рабочий объект (worker-object approach).

.. code-block:: python

   import sys
   from PyQt5 import QtWidgets
   from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal

   MAX_ITER = 1000000


   class Processor(QObject):
      iteration_passed = pyqtSignal(int)
      status_changed = pyqtSignal(bool)
      finished = pyqtSignal()

      def do_work(self):
         self.status_changed.emit(True)
         with open("out.txt", "w") as f:
               i = 0
               while i < MAX_ITER:
                  f.write("{}\n".format(i))
                  i += 1
                  self.iteration_passed.emit(i + 1)
         self.status_changed.emit(False)
         self.finished.emit()


   class MainWindow(QtWidgets.QMainWindow):
      process = pyqtSignal()

      def __init__(self):
         super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
         vlayout = QtWidgets.QVBoxLayout()
         widget = QtWidgets.QWidget()
         widget.setLayout(vlayout)
         self.setCentralWidget(widget)
         self.bar = QtWidgets.QProgressBar()
         self.bar.setMinimum(0)
         self.bar.setMaximum(MAX_ITER)
         self.bar.setValue(0)
         vlayout.addWidget(self.bar)
         self.button = QtWidgets.QPushButton("Start")
         self.button.pressed.connect(self.process)
         vlayout.addWidget(self.button)
         button = QtWidgets.QPushButton("About")
         button.pressed.connect(app.aboutQt)
         vlayout.addWidget(button)
         self.thread = QThread(self)
         # Worker-object must have no parent
         self.processor = Processor()
         self.processor.moveToThread(self.thread)
         self.thread.finished.connect(self.processor.deleteLater)
         self.process.connect(self.processor.do_work)
         self.processor.iteration_passed.connect(self.bar.setValue, Qt.DirectConnection)
         self.processor.status_changed.connect(self.button.setDisabled)
         self.processor.finished.connect(lambda: self.bar.setValue(0))
         self.destroyed.connect(self.thread.quit)
         self.destroyed.connect(self.thread.wait)
         self.thread.start()


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.setFixedSize(300, 150)
      w.show()

      res = app.exec_()
      sys.exit(res)

Важным моментом является то, что рабочий объект не должен иметь родителя при создании. Это является важным условием
для использование метода `moveToThread()`. Обратите внимание, что для завершения потока используется метод `quit()`,
так как оригинальный QThread работает на основе цикла событий.

QRunnable и QThreadPool
=======================

Обычно при использовании QThread поток запускается и живет на всем протяжении работы программы. В данном случае нам нужен
отдельный поток на небольшой промежуток времени. Тут нам поможет класс QThreadPool, класс для управления отдельными потоками. Он
может выделять отдельные потока на исполнение каких-либо операций и возвращать себе. Любое Qt приложение имеет
глобальный пул потоков, который можно получить функцией `QThreadPool.globalInstance()`. QThreadPool работает с объектами
класса QRunnable. Это класс для выделения части кода, который может быть исполнен в отдельном потоке. Реализация кода
помещается в метод `run()`. Запуск кода происходит при помощи метода `start()` класса QThreadPool. Как только работа
QRunnable завершится, QThreadPool сам удалит объект QRunnable (по желанию автоудаление можно отключить).

Важной особенностью QRunnable является то, что он не является наследником класса QObject, т.е. не может содержать
сигналы и слоты. Для этого используется вспомогательный объект, который будет содержать сигналы и слоты. Однако, тут
есть свои подводные камни. Если закрыть программу во время исполнения QRunnable, ProcessorWorker (а точнее скрываемый
им C++ объект QObject) может быть удален раньше Processor. MainWindow будет ждать завершение QRunnable при помощи
метода `waitForDone()` класса QThreadPool. Пока QRunnable не завершится, есть возможность, что он обратится к сигналам
от ProcessorWorker, чей C++ объект уже уничтожен. Привязав ProcessorWorker к MainWindow, мы обезапасим себя от такого,
т.к. объект ProcessorWorker будет готов к удалению после того, как его родитель будет готов к этому (т.е. после
завершения метода `cleanup()`). Главное, надо не забыть попросить приложение принудительно удалить объект (метод
`deleteLater()`), когда он станет не нужен. После завершения QRunnable, он сам будет автоматически удален, что нельзя
сказать про ProcessorWorker, привязанный к MainWindow. Таким образом мы удалим ProcessorWorker после смерти QRunnable,
но раньше завершения программы.

Другой особенностью QRunnable является отсутвие встроенных методов останова его работы. Однако это можно легко сделать,
сымитировав методы `requestInterruption()` и `isInterruptionRequested()` класса QThread. В примере ниже это не сделано,
но для вас это не должно составить труда.

.. code-block:: python

   import sys
   from PyQt5 import QtWidgets
   from PyQt5.QtCore import Qt, QRunnable, QThreadPool, QObject, pyqtSignal

   MAX_ITER = 1000000


   # Here we use multiple inheritence
   # to use signal/slot mechanism
   # from QRunnable
   class Processor(QRunnable, QObject):
      iteration_passed = pyqtSignal(int)
      status_changed = pyqtSignal(bool)
      finished = pyqtSignal()

      def __init__(self, parent):
         # Since we use multiple inheritence
         # it's more convenient to use
         # this syntax to call __init__ function
         QRunnable.__init__(self)
         QObject.__init__(self, parent)

      def run(self):
         self.status_changed.emit(True)
         with open("out.txt", "w") as f:
               i = 0
               while i < MAX_ITER:
                  f.write("{}\n".format(i))
                  i += 1
                  self.iteration_passed.emit(i + 1)
         self.status_changed.emit(False)
         self.finished.emit()


   class MainWindow(QtWidgets.QMainWindow):
      def __init__(self):
         super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
         vlayout = QtWidgets.QVBoxLayout()
         widget = QtWidgets.QWidget()
         widget.setLayout(vlayout)
         self.setCentralWidget(widget)
         self.bar = QtWidgets.QProgressBar()
         self.bar.setMinimum(0)
         self.bar.setMaximum(MAX_ITER)
         self.bar.setValue(0)
         vlayout.addWidget(self.bar)
         self.button = QtWidgets.QPushButton("Start")
         self.button.pressed.connect(self.process)
         vlayout.addWidget(self.button)
         button = QtWidgets.QPushButton("About")
         button.pressed.connect(app.aboutQt)
         vlayout.addWidget(button)
         self.thread_pool = QThreadPool(self)
         self.destroyed.connect(self.thread_pool.waitForDone)

      def process(self):
         processor = Processor(self)
         processor.iteration_passed.connect(self.bar.setValue, Qt.DirectConnection)
         processor.status_changed.connect(self.button.setDisabled)
         processor.finished.connect(lambda: self.bar.setValue(0))
         processor.setAutoDelete(True)
         self.thread_pool.start(processor)


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.setFixedSize(300, 150)
      w.show()

      sys.exit(app.exec_())

Библиотека concurrent
=====================

Еще один поход подразумевает использование стандартных инструментов Python, например библиотека concurrent.
Оттуда нам понадобится ThreadPoolExecutor и его метод `submit()`. Данный метод запускает на исполнение функцию или
метод, и возвращает футуру, если нужно от этой функции получить возвращаемый результат. Плюсом этого подхода является
возможность запускать произвольные функции и методы. Например, запустив метод нашего класса MainWindow, мы получаем код,
работающий в отдельном потоке, и не теряем возможность использовать сигналы.

.. code-block:: python

   import sys
   from concurrent.futures import ThreadPoolExecutor
   from PyQt5 import QtWidgets
   from PyQt5.QtCore import Qt, pyqtSignal

   MAX_ITER = 1000000

   class MainWindow(QtWidgets.QMainWindow):
      iteration_passed = pyqtSignal(int)
      status_changed = pyqtSignal(bool)
      finished = pyqtSignal()

      def __init__(self):
         super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
         vlayout = QtWidgets.QVBoxLayout()
         widget = QtWidgets.QWidget()
         widget.setLayout(vlayout)
         self.setCentralWidget(widget)
         self.bar = QtWidgets.QProgressBar()
         self.bar.setMinimum(0)
         self.bar.setMaximum(MAX_ITER)
         self.bar.setValue(0)
         vlayout.addWidget(self.bar)
         self.button = QtWidgets.QPushButton("Start")
         self.button.pressed.connect(self.process)
         vlayout.addWidget(self.button)
         button = QtWidgets.QPushButton("About")
         button.pressed.connect(app.aboutQt)
         vlayout.addWidget(button)
         self.thread_pool = ThreadPoolExecutor()
         self.iteration_passed.connect(self.bar.setValue, Qt.DirectConnection)
         self.status_changed.connect(self.button.setDisabled)
         self.finished.connect(lambda: self.bar.setValue(0))

      def process(self):
         self.thread_pool.submit(self.run)

      def run(self):
         self.status_changed.emit(True)
         with open("out.txt", "w") as f:
               i = 0
               while i < MAX_ITER:
                  f.write("{}\n".format(i))
                  i += 1
                  self.iteration_passed.emit(i + 1)
         self.status_changed.emit(False)


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.setFixedSize(300, 150)
      w.show()

      sys.exit(app.exec_())

Кроме concurrent можно попробовать воспользоваться asyncio, но я лично сам это не тестировал :)

Упражнение №1
=============

Напишите программу, которая представляет собой простенький чат-клиент. Для реализации можете использовать любой способ
распараллеливания. Ваша программа должна поддерживать прием/отправку текстовых сообщений по сети. При запуске должно
появляться диалоговое окно, в котором нужно указать имя/никнейм и IP собеседника. Чтобы не писать еще одну отдельную
программу, в диалогом окне должна быть возможность запустить программу как сервер (например, поставить галочку в
QCheckBox). В таком случае указывать IP собеседника не надо. для сетевых взаимодействий можете использовать встроенные
средства, сторонние библиотеки или модуль QtNetwork.

QtDesigner
----------

Библиотека Qt5 в дополнение имеет достаточно хороший вспомогательный инструмент -- QtDesigner. Это GUI программа для
прототипирования графического интерфейса приложения с возможностью настройки свойств виджетов. Обычно, QtDesigner
поставляется в виде одного из режимов QtCreator (C++ IDE, на текующий момент уже добавлена поддержка питона). Однако,
есть специальные пакеты, которые содержат отдельные Qt5 инструменты. Для пользователей Windows это пакет pyqt5-tools.
Для Linux (и, возможно, Mac OS) можно поставить системный пакет qtcreator через менеджер пакетов. Кроме того, всегда
можно скачать последнюю версию QtCreator с оф. сайта.

При прототипировании QtDesigner генерирует \*.ui файл. Этот файл внутри представляет собой обычный XML файл, который
необходимо конвертировать в код на языке Python. Предположим, что мы GUI из примеров для многопоточности спроектировали
и сохранили как mainwindow.ui_. Для конвертации ui файла необходимо использовать модуль uic.

.. _mainwindow.ui: {static}/extra/lab22/mainwindow.ui

.. code-block:: python

   from PyQt5 import uic

   Ui_MainWindow, _ = uic.loadUiType("mainwindow.ui")

Функция `loadUiType()` возвращает два класса: настроенный класс формы и базовый класс. В общем случае такое название
класса противоречит PEP8, но в данной ситуации это устоявшийся паттерн. Другой способ конвертации — утилита pyuic5,
которая идет в составе библиотеки. Она из ui файла генерирует py файл, который дальше просто надо импортировать в
проект.

.. code-block:: bash

   $ pyuic5 -o ui_mainwindow.py mainwindow.ui

.. code-block:: python

   from ui_mainwindow import Ui_MainWindow

Заметьте, что pyuic5 всегда генерирует название класса вида `Ui_` + класс основного виджета, отсюда и пошло
использование таких паттернов для названий классов из ui файлов. Но на генерации кода все не заканчивается. Во-первых,
созданный класс не отнаследован от Qt классов, соответственно не может быть использован как полноценный виджет.
Во-вторых, в любом случае класс требовал бы доработки (дополнительная настройка свойств виджетов, реализация основных
процессов и т.д.). Есть два способа интергрировать созданный класс в код. Для примера будем использовать все тот же код
из многопоточности.

Первый способ подразумевает композицию.

.. code-block:: python

   import sys
   from PyQt5 import QtWidgets, uic
   from PyQt5.QtCore import Qt, QRunnable, QThreadPool, QObject, pyqtSignal

   MAX_ITER = 1000000

   # Load ui file
   Ui_MainWindow, _ = uic.loadUiType("mainwindow.ui")
   # Or you can use pyuic5 + import insted of this


   class Processor(QRunnable, QObject):
      iteration_passed = pyqtSignal(int)
      status_changed = pyqtSignal(bool)
      finished = pyqtSignal()

      def __init__(self, parent):
         QRunnable.__init__(self)
         QObject.__init__(self, parent)

      def run(self):
         self.status_changed.emit(True)
         with open("out.txt", "w") as f:
               i = 0
               while i < MAX_ITER:
                  f.write("{}\n".format(i))
                  i += 1
                  self.iteration_passed.emit(i + 1)
         self.status_changed.emit(False)
         self.finished.emit()


   class MainWindow(QtWidgets.QMainWindow):
      def __init__(self):
         super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

         # We create Ui_MainWindow's instance as MainWindow attribute
         self.ui = Ui_MainWindow()
         # This is a mandatory step for GUI initialization
         self.ui.setupUi(self)
         # Now access to all widgets from *.ui file
         # is provided via self.ui attribute
         self.ui.bar.setMaximum(MAX_ITER)
         self.ui.start_button.pressed.connect(self.process)
         self.ui.about_button.pressed.connect(app.aboutQt)
         self.thread_pool = QThreadPool.globalInstance()
         self.destroyed.connect(self.thread_pool.waitForDone)

      def process(self):
         processor = Processor(self)
         processor.iteration_passed.connect(self.ui.bar.setValue, Qt.DirectConnection)
         processor.status_changed.connect(self.ui.start_button.setDisabled)
         processor.finished.connect(lambda: self.ui.bar.setValue(0))
         self.thread_pool.start(processor)


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.show()

      sys.exit(app.exec_())

Обратите внимаение, что названия объектов-виджетов такое, как было задано в QtDesigner.

Второй способ подразумевает использовать множественное наследование.

.. code-block:: python

   import sys
   from PyQt5 import QtWidgets, uic
   from PyQt5.QtCore import Qt, QRunnable, QThreadPool, QObject, pyqtSignal
   # Let's try this approach
   from ui_mainwindow import Ui_MainWindow

   MAX_ITER = 1000000


   class Processor(QRunnable, QObject):
      ration_passed = pyqtSignal(int)
      status_changed = pyqtSignal(bool)
      finished = pyqtSignal()

      def __init__(self, parent):
         QRunnable.__init__(self)
         QObject.__init__(self, parent)

      def run(self):
         self.status_changed.emit(True)
         with open("out.txt", "w") as f:
               i = 0
               while i < MAX_ITER:
                  f.write("{}\n".format(i))
                  i += 1
                  self.iteration_passed.emit(i + 1)
         self.status_changed.emit(False)
         self.finished.emit()


   class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
      def __init__(self):
         super().__init__(flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
         # This step is still mandatory!
         self.setupUi(self)
         # But now all widgets are our attributes,
         # instead of self.ui
         self.bar.setMaximum(MAX_ITER)
         self.start_button.pressed.connect(self.process)
         self.about_button.pressed.connect(app.aboutQt)
         self.thread_pool = QThreadPool.globalInstance()
         self.destroyed.connect(self.thread_pool.waitForDone)

      def process(self):
         processor = Processor(self)
         processor.iteration_passed.connect(self.bar.setValue, Qt.DirectConnection)
         processor.status_changed.connect(self.start_button.setDisabled)
         processor.finished.connect(lambda: self.bar.setValue(0))
         self.thread_pool.start(processor)


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.show()

      sys.exit(app.exec_())

На этом отличия в работе с QtDesigner заканчиваются. Если в вашем проекте несколько окон, то под каждое окно можно
делать свой уникальный прототип. Иногда выгоднее сделать один более общий прототип и использовать его для первоначальной
настройки похожих окон с доработкой уже из кода программы. Кроме того, можно проектировать не целые окна, а отдельные
виджеты.

Упражнение №2
=============

Используя QtDesigner, спроектируйте графический интерфейс вашей программы из упраженения №1. Постарайтесь по максимуму
настроить в нем свойства виджетов, их компоновку. При необходимости из дизайнера можно соединять сигналы и слоты.
Измените вашу программу на использование полученного ui файла.

Таблицы стилей
--------------

По умолчанию, приложения на основе QtWidgets имеют нативный для вашей операционной системы стиль. Сама библиотека имеет
набор предустановленных стилей. Вы можете запустить вашу программу с опцией `-style Windows`, чтобы выставить стиль
Windows не зависимо от ОС. Если данный стиль не доступен, программа вывдет предупреждение и список доступных стилей. При
помощи подобных аргументов можно выставлять некоторые настройки программы, и это главная причина передавать sys.argv
при создании объекта QApplication. Полный список аргументов можно найти в документации к QCoreApplication,
QGuiApplication и QApplication.

Однако, на это кастомизация внешнего вида программы не заканчивается. Внешний вид виджетов можно настраивать при помощи
таблицы стилей. В лабе по Flask вы уже познакомились с синтакисом CSS. Таблицы стилей основаны на CSS, тут вам надо
будет просто применить уже полученные знания. Таблицы стиля можно использовать двумя способами: задавать стиль напрямую
в коде или использовать `*.css` файл.

Первый способ подразумевает использование метода `setStyleSheet()`. Данный метод принимает на вход корректный CSS
текст и устанавливает стиль для данного виджета и всех дочерних виджетов. Т.е. применив стиль к центральному виджету, мы
можем подйствовать на все виджеты данного окна. Воспользуемся примерами из многопоточности. Применив стиль к
`self.button`, мы изменим внешний вид только одной конкретной кнопки. Добавьте данную строку в метод `__init__()`
главного окна:

.. code-block:: python

   self.button.setStyleSheet("QPushButton { background-color: red; border: none; }")

В результате должна измениться кнопка с надписью Start, в то время как кнопка About должна быть прежней. Теперь замените
это строку на строку ниже и запустите:

.. code-block:: python

   widget.setStyleSheet("QPushButton { background-color: red; border: none; }")

Теперь изменения коснулись всех кнопок, которые расположены на центральном виджете. Применив при этом другой стиль к
конкретной кнопке, мы перекроем более общий стиль.

Второй способ подразумевает написание `*.css` файла. Подключить такой файл можно аргументом
`-stylesheet path/to/css/file`.

.. _`Qt Style Sheets Reference`: https://doc.qt.io/qt-5/stylesheet-reference.html
.. _`Qt Style Sheets`: https://doc.qt.io/qt-5/stylesheet.html

Каждый виджет поддерживает свои аргументы, каждый аргумент имеет свой тип. Подробно перечислять это все я здесь не буду,
за подробным списком обращайтесь к `Qt Style Sheets Reference`_. Полный обзор данной системы можно прочитать в разделе
`Qt Style Sheets`_. Мы рассмотрим подробнее некоторые особенности в таблицах стилей.

Начнем с селекторов. Селектор -- элемент синтаксиса, который фильтрует подходящие классы. Qt поддерживает все селекторы,
определенные в CSS версии 2. Например:

+ `*` -- соответствует всем виджетам;
+ `QPushButton` -- соответствует QPushButton и его подклассам;
+ `QPushButton[flat="false"]` -- соответствует объектам QPushButton с указанным значением свойства;
+ `.QPushButton` -- соответствует строго QPushButton (т.е. не соответствует подклассам);
+ `QPushButton#ok_button` -- соответствует объектам QPushButton с идентификатором ok_button;
+ `QDialog QPushButton` -- соответствует всем QPushButton, которые являются потомками QDialog;
+ `QDialog > QPushButton` -- соответствует тем QPushButton, которые являются непосредственными потомками QDialog.

Кроме того, селекторы позволяют выбирать отдельные элементы составных виджетов. Например, QComboBox (выпадающий список)
содержит элемент в виде кнопки со стрелочкой, которую можно редактировать отдельно.

.. code-block:: CSS

   QComboBox::drop-down { image: url(dropdown.png) }

Селекторы могут содержать псевдо-состояния, которые ограничивают применение стиля к виджетам на основе их состояния.
Например, следующий стиль меняет QPushButton, только когда на него наведен указатель мыши.

.. code-block:: CSS

   QPushButton:hover { color: white }

Псевдо-состояния можно отрицать:

.. code-block:: CSS

   QPushButton:!hover { color: white }

Связывать через логическое И:

.. code-block:: CSS

   QCheckBox:hover:checked { color: white }

Связывать через логическое ИЛИ:

.. code-block:: CSS

   QCheckBox:hover, QCheckBox:checked { color: white }

Псевдо-состояния применимы и к отдельным элементам составных виджетов.

Следующее, что надо рассмотреть, это так называемая Box Model. Большая часть виджетов может быть представлена следующим
видом:

.. image:: {static}/images/lab22/stylesheet-boxmodel.png
   :align: center
   :alt: Box Model

Margins представляют собой обычные поля, которые ограничивают область отрисовки виджета. Borders задают видимые границы
виджета. Padding задает отступы содержимого от границ виджета. По умолчанию, поля, границы и отступы имеют нулевой
размер.

.. _`Qt Style Sheets Examples`: https://doc.qt.io/qt-5/stylesheet-examples.html

На этом можно окончить рассмотрение особенностей таблиц стилей. Рекомендую просмотреть `Qt Style Sheets Examples`_, там
большое количество примеров с картинками.

Упражнение №3
=============

Продолжаем изменять программу из первого упражнения. Спроектируйте для себя какой-нибудь стиль приложения, старясь
придерживаться его для всех используемых вами виджетов. Напишите один css файл и подцепите его в проект.
