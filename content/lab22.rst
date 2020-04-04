PyQt5: многопоточность GUI программ и дизайн интерфейса
#######################################################

:date: 2020-04-09 09:00
:summary: Cоздание графических приложений, ч.2
:status: draft

.. default-role:: code

.. contents:: Содержание

.. role:: python(code)
   :language: python

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
связать метод класса. Но можно связать лямбда-функцию, которая просто вызывает метод класса для освобождения ресурсов.

.. code-block:: python

   self.destroyed.connect(lambda: self.cleanup())

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

Прямое соединение гарантирует мгновенное срабатывание слота в том потоке, где был вызван  сигнал (считайте, что в этом
случае идет простой вызов слота как обычной функции). Соединение с очередью ставит исполнение слота в очередь. Слот
будет выполнен, как только управление вернется в цикл событий. Все это происходит в потоке, где живет объект-приемник.
Блокирующее соединение с очередью отличается тем, `emit()` блокирует исполнение потока до тех пор, пока слот не завершит
работу. Этот тип соединения должен быть использован, только если приемник живет в отдельном потоке от сигнализирующего
потока. По умолчанию используется автоматический способ. Если приемник живет в потоке, откуда исходит сигнал, то
соединеие работает по типу `DirectConnection`, иначе по типу `QueuedConnection`. Тип соединения определяется каждый раз
при срабатывании сигнала. `UniqueConnection` используется вместе с любым другим типом. Он позволяет позволяет создать
уникальное соединение, чтобы избежать дубликатов. Без него один и тот же сигнал может быть соединен с одним и тем же
слотом несолько раз.

Многопоточность
---------------

В предыдущей лабе мы рассматривали программы, где не было каких либо долгих вычислений или операций. Но вы с этим могли
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
механизмом. Основной код, который будет выполняться в потоке, пишется в виде тела метода `run()`. Этот метод будет вызван
автоматически, когда вы запустите работу потока. Важным моментом в использовании потоков является способ их останова.
QThread имеет метод `terminate()`, который принудительно завершает работу потока. Однако, его использование в общем
случае не одобряется, т.к. после такого могут оказаться неразблокированные мьютексы, неосвобожденные ресурсы, частично
записанные (а значит испорченные) участки памяти. Второй механизм останова — методы `requestInterruption()` и
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
         self.processor.iteration_passed.connect(self.bar.setValue, Qt.DirectConnection)
         self.processor.status_changed.connect(self.button.setDisabled)
         self.processor.finished.connect(lambda: self.bar.setValue(0))
         self.destroyed.connect(lambda: self.cleanup())

      def process(self):
         self.processor.start()

      def cleanup(self):
         if self.processor:
               self.processor.requestInterruption()
               self.processor.wait()


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

Также стоит отметить, что это не единственный способ работы с QThread. Другой способ использование рабочего объекта
(worker-object approach), что имеет свои плюсы.

QRunnable и QThreadPool
=======================

Пример выше — не совсем типичный пример использования QThread, хотя не является плохим решением. Обычно при
использовании QThread поток запускается и живет на всем протяжении работы программы. В данном случае нам нужен отдельный
поток на небольшой промежуток времени. Тут нам поможет класс QThreadPool, класс для управления отдельными потоками. Он
может выделять отдельные потока на исполнение каких-либо операций и возвращать себе. Любое Qt приложение имеет
глобальный пул потоков, который можно получить функцией `QThreadPool.globalInstance()`. QThreadPool работает с объектами
класса QRunnable. Это класс для выделения части кода, который может быть исполнен в отдельном потоке. Реализация кода
помещается в метод `run()`. Запуск кода происходит при помощи метода `start()` класса QThreadPool. Как только работа
QRunnable завершится, QThreadPool сам удалит объект QRunnable (по желанию автоудаление можно отключить).

Важной особенностью QRunnable является то, что он не является наследником класса QObject, т.е. не может содержать
сигналы и слоты. Для этого используется вспомогательный объект, который будет содержать сигналы и слоты. Однако, тут
есть свои подводные  камни. Если закрыть программу во время исполнения QRunnable, ProcessorWorker (а точнее скрываемый
им C++ объект QObject) может быть удален  раньше Processor. MainWindow будет ждать завершение QRunnable при помощи
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


   class ProcessorWorker(QObject):
      iteration_passed = pyqtSignal(int)
      status_changed = pyqtSignal(bool)
      finished = pyqtSignal()


   class Processor(QRunnable):
      def __init__(self, parent):
         super().__init__()
         # we need parent to protect worker
         # from beeing deleted before Processor
         self.signals = ProcessorWorker(parent)

      def run(self):
         self.signals.status_changed.emit(True)
         with open("out.txt", "w") as f:
               i = 0
               while i < MAX_ITER:
                  f.write("{}\n".format(i))
                  i += 1
                  self.signals.iteration_passed.emit(i + 1)
         self.signals.status_changed.emit(False)
         self.signals.finished.emit()
         # now we ask application do delete worker
         # since we don't need it anymore
         self.signals.deleteLater()


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
         self.destroyed.connect(lambda: self.cleanup())

      def process(self):
         processor = Processor(self)
         processor.signals.iteration_passed.connect(self.bar.setValue, Qt.DirectConnection)
         processor.signals.status_changed.connect(self.button.setDisabled)
         processor.signals.finished.connect(lambda: self.bar.setValue(0))
         self.thread_pool.start(processor)

      def cleanup(self):
         self.thread_pool.waitForDone()


   if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)

      w = MainWindow()
      w.setFixedSize(300, 150)
      w.show()

      sys.exit(app.exec_())


Библиотека concurrent
=====================

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

QtDesigner
---------

Таблицы стилей
--------------
