Создание Web сайтов на Python. flask
##################################################

:date: 2021-03-23 16:29
:summary: flask blueprints


.. default-role:: code

.. contents:: Содержание

.. role:: python(code)
   :language: python

.. role:: bash(code)
   :language: bash

.. raw:: html

    <style>
    td, th{
        border-style:dashed solid;
        border-width:1px;
        border-color:rgba(0,0,0,0.5);
    }
    </style>


Введение
--------
В предыдущей работе, вы познакомились с основами использования flask. В данной работе, рассмотрим способы обмена данными между flask и браузером, использование чертежей.

Обмен данными между flask и браузером
-------------------------------------

Передать информацию странице сайта можно по средствам особого вида url и при помощи особых методов запроса данных.

Передача по url
===============

Некоторая, написанная вами функция, может принимать параметры, передаваемые flask по средствам обработки строки запроса.
В примере ниже, функция `get_user_info` будет запускаться для адресов `/user` и `/user/<int:N>`.
Текст `<int:N>` (*без пробелов*) показывает flask, что после `/user/` должно быть целое число (`int`), которое необходимо передать функции под именем `N`.
Если тип не задан, то передаётся строка.
Поскольку, в случае `/user` никакое `N` не передаётся, то необходимо определить значение `N` «по умолчанию».

.. code:: python

    @bp.route("/user")
    @bp.route("/user/<int:N>")
    def get_user_info(N=-1):
        if N < 0:
            return Response(status=503)
        else:
            return render_template("user_info.html", user_n=N)

`return Response(status=503)` возвращает браузеру информацию, что переданы некорректные данные (ошибка 503).

*узнать url можно по url_for('get_user_info', N=2)*

HTML формы
==========

Рассмотрим следующий `html` блок, определяющий блок ввода данных:

.. code:: html

    <form method="post" action='{{ url_for('login') }}'>
      <label for="username">Username</label>
      <input name="username" id="username" required>
      <label for="password">Password</label>
      <input type="password" name="password" id="password" required>
      <input type="submit" value="Log In">
    </form>


Браузер отобразит её следующим образом

.. raw:: html

    <form method="post" style="text-align:center;padding:10px;border:1px solid black; background-color:white;">
      <label for="username">Username</label>
      <input type="username" name="username" required> <br/>
      <label for="password">Password</label>
      <input type="password" name="password" required> <br/>
      <input type="submit" value="Log In">
    </form>

`<input type="submit" value="Log In">` создаёт кнопку, инициирующую отправку данных.
Обрабатывать данные будет функция `login`, указанная в параметре `action=`.
Данные будут переданы по именам, заданным в параметрах `name` — `username` и `password`.
Для доступа к ним необходимо использовать `flask.request`.
Метод передачи данных — `POST`. Альтернативный вариант (передача данных в строке url) — `GET`.

Пример функции, обрабатывающей запрос от данной формы:

.. code:: python

    @app.route("/login", methods=("GET", "POST"))
    def login():

        if request.method == "POST":
            # переходим сюда, если были переданы данные
            username = request.form["username"]
            password = request.form["password"]
            db = get_db() # берём информацию о базе данных (функция определена отдельно)
            error = None
            user = db.execute(
                "SELECT * FROM user WHERE username = ?", (username,)
            ).fetchone() # получаем запись из базы данных

            if user is None:
                error = "Incorrect username."
            elif not check_password_hash(user["password"], password): # проверяем пароль
                error = "Incorrect password."

            if error is None:
                # отчищаем информацию о текущей сессии взаимодействия браузера
                # и сохраняем информацию о текущем пользователе на сервере
                # получить доступ к данной информации можно в любой функции через flask.session
                session.clear()
                session["user_id"] = user["id"]
                return redirect(url_for("index")) # перенаправляем пользователя на главную страницу

        return render_template("auth/login.html")

*P.S. существуют ещё методы `PUT`, `PATCH`, `DELETE` использование которых из браузера возможно по средствам javascript*

Использование blueprints
------------------------

Поскольку помещать весь функционал вашего web сайта в один файл `__init__.py` не самая здравая идея, возникает вопрос, как можно разделить функционал сайта на отдельные файлы.
Для этой функции необходимо использовать механизм чертежей (blueprint).

Blueprint создаётся по аналогии с простым сайтом `flask` и подключается к основному сайту.
Для демонстрации, воспользуемся примером__ с сайта__


__  {static}/extras/lab20/flaskr.zip
__  https://flask.palletsprojects.com/en/1.1.x/tutorial/

Файл `__init__.py` выглядит следующим образом:


.. code:: python

    import os

    from flask import Flask

    def create_app(test_config=None):
        # Создаём сайт flask

        app = Flask(__name__, instance_relative_config=True)

        # конфигурация сайта по умолчанию
        app.config.from_mapping(
            SECRET_KEY="dev", # ключ шифрования сессии (необходимо менять при релизе сайта)
            DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"), # информация о базе данных пользователя
        )

        app.config.from_pyfile("config.py", silent=True) # обновляем настройки из файла (если он есть)

        try:
            os.makedirs(app.instance_path) # создаём instance директорию (вдруг её нет)
        except OSError:
            pass

        # загружаем файл работы с базой данных db.py
        from flaskr import db

        db.init_app(app)  #  подключаем базу данных к сайту, дабы иметь к ней доступ отовсюду

        # Загружаем чертежи страниц
        from flaskr import auth, blog

        app.register_blueprint(auth.bp) #  регистрируем их на нашем сайте
        app.register_blueprint(blog.bp) #

        # определяем главную страницу сайта.
        # можно воспользоваться @app.route("/")

        app.add_url_rule("/", endpoint="blog.index")

        return app

Здесь простая главная страница сайта с подключением и регистрацией blueprint-ов

Теперь посмотрим на `auth.py`:

.. code:: python

    # много разных импортов

    from flaskr.db import get_db # импортируем функцию get_db для доступа к базе данных

    # создаём blueprint, передавая ему имя ``auth`` и подключением на сайт к ``/auth``
    bp = Blueprint("auth", __name__, url_prefix="/auth")


    def login_required(view):
        """Декоратор требующий пользователя залогиниться"""
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for("auth.login"))
            return view(**kwargs)
        return wrapped_view


    @bp.before_app_request
    def load_logged_in_user():
        """
        если пользователь залогинился,
        то вся информация о нём будет храниться в ``flask.g.user``
        доступ к flask.g имеется у любой flask функции
        """
        user_id = session.get("user_id")

        if user_id is None:
            g.user = None
        else:
            g.user = (
                get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
            )


    @bp.route("/register", methods=("GET", "POST"))
    def register():
        # Регистрация нового пользователя по адресу /auth/register
        # /auth берётся из Blueprint("auth", __name__, url_prefix="/auth")

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            db = get_db()
            error = None

            # тут надо проверить данные на корректность

            if error is None:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                return redirect(url_for("auth.login"))

        return render_template("auth/register.html")


    @bp.route("/login", methods=("GET", "POST"))
    def login():
        # эта функция рассмотрена выше

    @bp.route("/logout")
    @login_required  # данная страница работает только если пользователь залогинился
    def logout():
        """Clear the current session, including the stored user id."""
        session.clear()
        return redirect(url_for("index"))


И, конечно, необходимо рассмотреть `db.py`


.. code:: python

    # тут импорты

    def get_db():
        # функция получения доступа к базе данных
        if "db" not in g:
            # если это первый запрос на подключение то подключаемся
            g.db = sqlite3.connect(
                current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

        return g.db


    def close_db(e=None):
        '''прописываем отключение'''
        db = g.pop("db", None)

        if db is not None:
            db.close()


    def init_db():
        """Здесь функция очистки базы данных и её создания по файлу ``schema.sql``"""
        db = get_db()

        with current_app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf8"))


    # ниже
    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        init_db()
        click.echo("Initialized the database.")


    def init_app(app):
        """Процесс подключения базы к сайту
        """
        app.teardown_appcontext(close_db) # необходимо закрыть базу данных по закрытию сайта
        app.cli.add_command(init_db_command) # подключаем команду flask


Обратим внимание на блок ниже

.. code:: python

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        init_db()
        click.echo("Initialized the database.")

Фактически, мы видим процесс создания пустой базы данных, но с подключением её на `cli` команду `init-db`.
данная конструкция (вместе с `app.cli.add_command(init_db_command)`) позволяет провести операцию создания базы данных
из командной строки:

.. code:: bash

    $ echo Определяем параметры сайта
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ echo инициализируем пустую базу данных
    $ flask init-db
    $ echo запускаем сайт
    $ flask run

Естественно, что запускать инициализацию базы данных необходимо только один раз (иначе она постоянно будет обнуляться).


Блочная структура папки templates
=================================

При создании html templates сайта, естественно, когда общий для всех страниц сайта шаблон описан только в одном файле.
Все остальные шаблоны только модифицируют базовый шаблон.

Рассмотрим `base.html` из примера выше

.. code:: html

    <!doctype html>
    <title>{% block title %}{% endblock %} - Flaskr</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <nav>
      <h1><a href="{{ url_for('blog.index') }}">Flaskr</a></h1>
      <ul>
        {% if g.user %}
          <li><span>{{ g.user['username'] }}</span>
          <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
        {% else %}
          <li><a href="{{ url_for('auth.register') }}">Register</a>
          <li><a href="{{ url_for('auth.login') }}">Log In</a>
        {% endif %}
      </ul>
    </nav>
    <section class="content">
      <header>
        {% block header %}{% endblock %}
      </header>
      {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
      {% endfor %}
      {% block content %}{% endblock %}
    </section>

Здесь, сайт определяет блоки `title`, `header` и `content`, общую для всех страниц навигацию `<nav> ... </nav>` и блок сообщений сервера:

.. code:: html

      {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
      {% endfor %}

Такие сообщения определяются при помощи `flask.flush(message)`. При этом имя пользователя и кнопка `Log Out` выводяться только тогда, когда есть информация о пользователе в `flask.g.user`:

.. code:: html

        {% if g.user %}
          <li><span>{{ g.user['username'] }}</span>
          <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
        {% else %}
          <li><a href="{{ url_for('auth.register') }}">Register</a>
          <li><a href="{{ url_for('auth.login') }}">Log In</a>
        {% endif %}

При этом, содержимое блоков определяется, как в `auth/login.html`

.. code:: html

    {% extends 'base.html' %}

    {% block header %}
      <h1>{% block title %}Log In{% endblock %}</h1>
    {% endblock %}

    {% block content %}
      <form method="post">
        <label for="username">Username</label>
        <input name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <input type="submit" value="Log In">
      </form>
    {% endblock %}

Здесь, за основу берётся `base.html` (команда `extends`) и определяется содержимое блоков `header`, `title` (определяется внутри `header`) и `content` с формой `POST` запроса к текущей странице.

Задача
======

#. Скачайте себе и запустите сайт из обучения flask.
#. Допишите в таблицу пользователей поля с email-ом пользователя и его уровенем доступа (админ или простой пользователь)
#. Напишите свой модуль, позволяющий администратору изменять информацию обо всех пользователях сайта
