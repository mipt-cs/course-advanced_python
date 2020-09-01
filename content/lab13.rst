Краткий справочник Git
###############################

:date: 2019-12-02 09:00
:summary: Краткий справочник Git
:status: draft

.. default-role:: code

.. contents:: Содержание


.. role:: python(code)
   :language: python


Введение Git
============
**Git** — распределённая система контроля версий: система, записывающая изменения в файл или набор файлов в течение времени и позволяющая вернуться позже к определённой версии. Для контроля версий файлов в этой книге в качестве примера будет использоваться исходный код программного обеспечения, хотя на самом деле вы можете использовать контроль версий практически для любых типов файлов.

Если вы графический или web-дизайнер и хотите сохранить каждую версию изображения или макета (скорее всего, захотите), система контроля версий (далее СКВ) — как раз то, что нужно. Она позволяет вернуть файлы к состоянию, в котором они были до изменений, вернуть проект к исходному состоянию, увидеть изменения, увидеть, кто последний менял что-то и вызвал проблему, кто поставил задачу и когда и многое другое. Использование СКВ также значит в целом, что, если вы сломали что-то или потеряли файлы, вы спокойно можете всё исправить. В дополнение ко всему вы получите всё это без каких-либо дополнительных усилий.

Схема работы с git
===================

.. raw:: html

	<svg style="zoom:0.7" height="631.0390625" version="1.1" width="331.4296875" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="overflow: hidden; position: relative; left: -0.5px; top: -0.5px;" viewBox="0 0 331.4296875 631.0390625" preserveAspectRatio="xMidYMid meet"><desc style="">Created with Raphaël 2.3.0</desc><defs style=""><path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style=""></path><marker id="raphael-marker-endblock33-objz59qu" markerHeight="3" markerWidth="3" orient="auto" refX="1.5" refY="1.5" style=""><use xlink:href="#raphael-marker-block" transform="rotate(180 1.5 1.5) scale(0.6,0.6)" stroke-width="1.6667" fill="black" stroke="none" style=""></use></marker><marker id="raphael-marker-endblock33-objq3ve1" markerHeight="3" markerWidth="3" orient="auto" refX="1.5" refY="1.5" style=""><use xlink:href="#raphael-marker-block" transform="rotate(180 1.5 1.5) scale(0.6,0.6)" stroke-width="1.6667" fill="black" stroke="none" style=""></use></marker><marker id="raphael-marker-endblock33-obj418xl" markerHeight="3" markerWidth="3" orient="auto" refX="1.5" refY="1.5" style=""><use xlink:href="#raphael-marker-block" transform="rotate(180 1.5 1.5) scale(0.6,0.6)" stroke-width="1.6667" fill="black" stroke="none" style=""></use></marker><marker id="raphael-marker-endblock33-obj2mune" markerHeight="3" markerWidth="3" orient="auto" refX="1.5" refY="1.5" style=""><use xlink:href="#raphael-marker-block" transform="rotate(180 1.5 1.5) scale(0.6,0.6)" stroke-width="1.6667" fill="black" stroke="none" style=""></use></marker><marker id="raphael-marker-endblock33-obj71q0x" markerHeight="3" markerWidth="3" orient="auto" refX="1.5" refY="1.5" style=""><use xlink:href="#raphael-marker-block" transform="rotate(180 1.5 1.5) scale(0.6,0.6)" stroke-width="1.6667" fill="black" stroke="none" style=""></use></marker><marker id="raphael-marker-endblock33-obj439wq" markerHeight="3" markerWidth="3" orient="auto" refX="1.5" refY="1.5" style=""><use xlink:href="#raphael-marker-block" transform="rotate(180 1.5 1.5) scale(0.6,0.6)" stroke-width="1.6667" fill="black" stroke="none" style=""></use></marker></defs><rect x="0" y="0" width="292.796875" height="36" rx="20" ry="20" fill="#ffffff" stroke="#000000" style="" stroke-width="3" class="flowchart" id="A" transform="matrix(1,0,0,1,10.6953,22.8047)"></rect><text x="10" y="18" text-anchor="start" stroke="none" fill="#000000" style=" text-anchor: start;" id="At" class="flowchartt" transform="matrix(1,0,0,1,10.6953,22.8047)" stroke-width="1"><tspan dy="5" style="">Создание или клонирование репозитория</tspan></text><rect x="0" y="0" width="251.765625" height="36" rx="0" ry="0" fill="#ffffff" stroke="#000000" style="" stroke-width="3" class="flowchart" id="B" transform="matrix(1,0,0,1,31.2109,131.6094)"></rect><text x="10" y="18" text-anchor="start" stroke="none" fill="#000000" style=" text-anchor: start;" id="Bt" class="flowchartt" transform="matrix(1,0,0,1,31.2109,131.6094)" stroke-width="1"><tspan dy="5" style="">Создание, редактирование файлов</tspan></text><rect x="0" y="0" width="216.875" height="69.609375" rx="0" ry="0" fill="#ffffff" stroke="#000000" style="" stroke-width="3" class="flowchart" id="C" transform="matrix(1,0,0,1,48.6563,223.6094)"></rect><text x="10" y="34.8046875" text-anchor="start" stroke="none" fill="#000000" style=" text-anchor: start;" id="Ct" class="flowchartt" transform="matrix(1,0,0,1,48.6563,223.6094)" stroke-width="1"><tspan dy="-11.796875" style="">Загрузка изменений других</tspan><tspan dy="16.8" x="10" style="">пользователей из удалённого
	</tspan><tspan dy="16.8" x="10" style="">репозитория (pull)</tspan></text><rect x="0" y="0" width="249.984375" height="52.8125" rx="0" ry="0" fill="#ffffff" stroke="#000000" style="" stroke-width="3" class="flowchart" id="D" transform="matrix(1,0,0,1,32.1016,357.6172)"></rect><text x="10" y="26.40625" text-anchor="start" stroke="none" fill="#000000" style=" text-anchor: start;" id="Dt" class="flowchartt" transform="matrix(1,0,0,1,32.1016,357.6172)" stroke-width="1"><tspan dy="-3.40625" style="">Подготовка изменений к фиксации
	</tspan><tspan dy="16.8" x="10" style="">новой версии репозитория (stage)</tspan></text><rect x="0" y="0" width="302.1875" height="36" rx="0" ry="0" fill="#ffffff" stroke="#000000" style="" stroke-width="3" class="flowchart" id="E" transform="matrix(1,0,0,1,6,483.2344)"></rect><text x="10" y="18" text-anchor="start" stroke="none" fill="#000000" style=" text-anchor: start;" id="Et" class="flowchartt" transform="matrix(1,0,0,1,6,483.2344)" stroke-width="1"><tspan dy="5" style="">Фиксация изменений репозитория (commit)</tspan></text><rect x="0" y="0" width="292.671875" height="36" rx="0" ry="0" fill="#ffffff" stroke="#000000" style="" stroke-width="3" class="flowchart" id="F" transform="matrix(1,0,0,1,10.7578,592.0391)"></rect><text x="10" y="18" text-anchor="start" stroke="none" fill="#000000" style=" text-anchor: start;" id="Ft" class="flowchartt" transform="matrix(1,0,0,1,10.7578,592.0391)" stroke-width="1"><tspan dy="5" style="">Загрузка изменений в репозиторий (push)</tspan></text><path fill="none" stroke="#000000" d="M157.09375,58.8046875C157.09375,58.8046875,157.09375,111.23699628561735,157.09375,127.11005851563823" stroke-width="3" marker-end="url(#raphael-marker-endblock33-objz59qu)" style=""></path><path fill="none" stroke="#000000" d="M157.09375,167.609375C157.09375,167.609375,157.09375,205.81014585494995,157.09375,219.10953531763516" stroke-width="3" marker-end="url(#raphael-marker-endblock33-objq3ve1)" style=""></path><path fill="none" stroke="#000000" d="M157.09375,293.21875C157.09375,293.21875,157.09375,338.48307161591947,157.09375,353.1144099507528" stroke-width="3" marker-end="url(#raphael-marker-endblock33-obj418xl)" style=""></path><path fill="none" stroke="#000000" d="M157.09375,410.4296875C157.09375,410.4296875,157.09375,462.86199628561735,157.09375,478.73505851563823" stroke-width="3" marker-end="url(#raphael-marker-endblock33-obj2mune)" style=""></path><path fill="none" stroke="#000000" d="M157.09375,519.234375C157.09375,519.234375,157.09375,571.6666837856174,157.09375,587.5397460156382" stroke-width="3" marker-end="url(#raphael-marker-endblock33-obj71q0x)" style=""></path><path fill="none" stroke="#000000" d="M303.4296875,610.0390625C303.4296875,610.0390625,328.4296875,600.0390625,328.4296875,600.0390625C328.4296875,600.0390625,328.4296875,96.609375,328.4296875,96.609375C328.4296875,96.609375,157.09375,96.609375,157.09375,96.609375C157.09375,96.609375,157.09375,117.65244674682617,157.09375,127.10538913309574" stroke-width="3" marker-end="url(#raphael-marker-endblock33-obj439wq)" style=""></path></svg>


Основные команды git
========================

Создание пустого git репозитория в папке `<dir>`. Если `<dir>` не задана — пустой репозиторий инициализируется в текущей папке (`<dir> = .`). Все базы данных для работы `git` создаются в «скрытой» папке `<dir>/.git`. Такой репозиторий хранит локальную историю версий рабочей директории.

.. code-block:: bash

    $ git init <dir>

Создание простого пустого git репозитория в папке `<dir>`. Если `<dir>` не задана — пустой репозиторий инициализируется в текущей папке (`<dir> = .`). При таком варианте создания репозитория, папка `<dir>` содержит исключительно историю версий. Такой вариант создания репозитория необходимо использовать для совместного использования созданного репозитория. **Репозиторий не содержит «рабочей» версии, позволяющей работать с проектом непосредственного в рабочей папке.**

.. code-block:: bash

    $ git init --bare <dir>

Создаёт копию git репозитория `<rep>` в папке `<dir>`. Если имя папки `<dir>` не задано — имя папки выбирается автоматически на основании `<rep>`.

.. code-block:: bash

    $ git clone <rep> <dir>

**Примеры использования:**

	Клонирование локального репозитория:

	.. code-block:: bash

		$ git clone /path/to/repository/directory


	Клонирование удалённого интернет репозитория:

	.. code-block:: bash

		$ git clone https://github.com/path/to/repository

	Клонирование удалённого репозитория по протоколу `ssh`:

	.. code-block:: bash

		$ git clone ssh://<username>@<address>/path/to/repository/directory

Fork репозитория — создание собственной копии репозитория, позволяющего производить разработку своего приложения отдельно от владельца «основного» репозитория

.. code-block:: bash

	$ git clone --bare <rep>


**Настройка git**

После создания (клонирования) репозитория, необходимо настроить информацию, о том, кто будет работать с ним работать. Для этого необходимо сообщить информацию об имени и почте пользователя. Данная информацию может быть сохранена локально — сохраняется только для данного репозитория и глобальной — информация сохраняется для текущего пользователя ОС (Windows, Linux, OS) и её не надо будет заново вводить для последующих репозиториев.

.. code-block:: bash

	$ git config --global user.name="Тут имя"
	$ git config --global user.email="Почта"

или

.. code-block:: bash

	$ git config --local user.name="Тут имя"
	$ git config --local user.email="Почта"

**Работа с репозиторием**

Отметить изменения в файле `<filename>` — изменения, сделанные в файле, подготавливаются для их фиксации как отдельной версии в репозитории.

.. code-block:: bash

	$ git add <filename>

Отметить изменения во всех доступных файлах репозитория:

.. code-block:: bash

	$ git add *

Отменить действие команды `add` для `<filename>`

.. code-block:: bash

	$ git reset -- <filename>

Зафиксировать все подготовленные, с использованием `git add`, изменения

.. code-block:: bash

	$ git commit -m "commit message"

Посмотреть текущее состояние репозитория

.. code-block:: bash

	$ git status

Откатить все изменения, сделанные после фиксации (`commit`)

.. code-block:: bash

	$ git checkout -- .

**Взаимодействие с внешним репозиторием**

Загрузить из внешнего репозитория все изменения. **Возможно потребуется разрешение конфликтов, если файл был изменён различными пользователями**

.. code-block:: bash

	$ git pull

Выгрузить, зафиксированные на вашем компьютере, версии (коммиты) в удалённом репозиторий. Если Вы не выполнили операцию `pull`, системы выдаст соответствующую ошибку.

.. code-block:: bash

	$ git push

Ветки git
=========

Git позволяет проводить разработку проекта в отдельной ветке, независимо от других пользователей, загружая изменения в основную ветку `master` только после тщательной проверки и доработки всех изменений внутри отдельно созданной ветки.

Чтобы создать ветку `<branch_name>` необходимо выполнить команду.

.. code-block:: bash

	$ git branch <branch_name>

В случае, если `<branch_name>` не задан, будет выведен список существующих веток. **Создав новую ветку, вы остаётесь в старой.**

Переключение на ветку `<branch_name>` осуществляется по команде

.. code-block:: bash

	$ git checkout <branch_name>

Создать и сразу переключиться на новую ветку `<branch_name>` можно по команде

.. code-block:: bash

	$ git checkout -b <branch_name>


Для того, чтобы объединить ветки (например, присоединить `<branch_name>` в главную ветку `master`). Необходимо переключиться на основную ветку (`master`), и присоединить к ней (`merge`) другую ветку (`<branch_name>`). В примере ниже, создаётся отдельная ветка `hotfix_123`. После решения проблемы фиксируются все изменения в данной ветке, после чего происходит присоединение ветки с hotfix-ом в основную ветку (`master`)

.. code-block:: bash

	$ git checkout -b hotfix_123
	...
	$ git add *
	$ git commimt -m "HOTFIX for #ISSUE-123"
	$ git checkout master
	$ git merge hotfix

**.gitignore**

Для того, чтобы быстро зафиксировать все сделанные изменения, удобно использовать команду `add *`, но такая команда может поместить в репозиторий те файлы, изменение которых Вы не хотите отслеживать (например, служебные файлы питона `.pyc`). Информацию о таковых удобно поместить в файл `.gitignore` (**имя файла начинается с точки**), тогда `add *` не будет «подхватывать» новые файлы из заданных папок (с заданным именем, расширением, пр.).

Github
======

Крупнейшим веб-сервисом для хостинга IT-проектов и их совместной разработки на основании технологии `git`, является сайт `Github`__. Он целиком построен на `git` и поддерживает все перечисленные команды, дополняя их различными возможностями. К таковым возможностям относятся: Issues — назначение заданий пользователям с описанием задачи, которую необходимо решить; Push Request — не являясь владельцем репозитория и не имея возможности напрямую отправлять изменения в репозиторий (или же просто в основную `master` ветку), у пользователя github есть возможность запросить осуществление команды `merge <ваша_репозиторий/ваша_ветка> <целевая_ветка_репозитория>` у привилегированного пользователя, имеющего полный доступ к репозиторию. В случае положительного ответа, предложенные Вами изменения «вольются» в основной проект.

__ https://github.com/


Задание
=======

#. Зарегистрироваться в github__, если Вы ещё не зарегистрированы
#. Разбиться на группы по два человека для выполнения семестрового проекта
#. Один человек из каждой группы создаёт **приватный** репозиторий для проекта на python (см. рисунок ниже)
#. Владелец репозитория даёт доступ к нему второму студенту и преподавателю
#. Каждый студент создаёт свою ветку, в которой ведёт дальнейшую разработку своей части проекта до конца семестра, отправляя в `master` рабочие версии файлов.
#. До следующей пары придумать семестровый проект и дать его короткое описание в файле README Вашего совместного проекта

**ограничения на размеры групп, темы проектов, сроки, уточняйте у своего преподавателя**

__ https://github.com

.. image:: {filename}/images/lab13/img1.png
  :width: 80%
  :align: center

.. image:: {filename}/images/lab13/img2.png
  :width: 80%
  :align: center
