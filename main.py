#импортируем нужные модули и части кода для работы программы

from flask import Flask
from data import db_session
from data.users import User
from data.news import News
from flask import render_template
from flask import redirect
from templates.forms.user import RegisterForm
from templates.forms.user import LoginForm
from flask_login import LoginManager
from flask_login import login_user
from flask_login import current_user
from flask_login import login_required
from templates.forms.news import NewsForm
from templates.forms.paintings import PaintForm
import json
import shutil
import requests
from flask import request
from sqlalchemy import orm
from sqlalchemy.orm import Session
import os
from flask import send_from_directory
from flask import url_for
from werkzeug.utils import secure_filename
from pathlib import Path

# получаем с помощью API картинку из яндекс карт
response = requests.get('https://static-maps.yandex.ru/1.x/?l=map&pt=55.741251,%20' +
                        '37.591851~55.762260,%2037.622152~' +
                        '55.776693,%2037.626076~55.735610,%2037.585687~' +
                        '55.746432,%2037.606689&size=450,%20450')
# инициализируем приложение, а также подключаем нужные инструменты

app = Flask(__name__, template_folder="templates")
login_manager = LoginManager()
login_manager.init_app(app)

# функция работы сайта, в которой прописывается её конфигурация


def main():
    db_session.global_init("db/NewDataBase.db")
    app.config['SECRET_KEY'] = 'My_SeCReT_KEY'
    app.config['UPLOAD_FOLDER'] = '/static/img'
    app.run()

# основная страница сайта


@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)

# поле регистрации сайта


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

# поле авторизации сайта


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

# поле добавления  постов


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('records.html', title='Добавление '
                                                 'новости',
                           form=form)

# поле просмотра галерей Москвы


@app.route('/exhibitions', methods=['GET', 'POST'])
def show_exhibitions():
    return f'''<!DOCTYPE 
    html>
<html 
lang="en">
<head>
    <meta charset="UTF-8">
    <title
    >Места, 
    которые 
    стоит 
    посетить
    </title>
     <style 
     type="text/css">
   P.fig {
    'text-align: center; /* Выравнивание по центру */'
   }
  </style>
</head>
<body>
    <h1>Места, 
    которые 
    стоит 
    посетить</h1>
        <p>
        <img 
        src={'https://static-maps.yandex.ru/1.x/?l=map&pt=' +
                '37.626076,55.776693~' +
                '37.602876,55.757783~' +
                '37.585687,55.735610' +
                '&size=300,300&spn=0.001,0.01'}>
        </p>
        <p>Так 
        как 
        очень 
        много 
        достопримечательностей, 
        связанных 
        с 
        искусством 
        в 
        Москве, 
        то 
        возьмём 
        все 
        самые 
        интересные 
        картинные 
        галереи 
        города.</p>
        
        <p>
        В 
        самом 
        верху 
        располагается 
        на 
        карте 
        Третьяковская 
        галерея 
        -
        легендарное 
        место.
        </p>
         <p>
         Подойдёт 
         для 
         всех 
         любителей 
         изобразительного 
         творчества.
         </p>
         <p>
         Чуть 
         ниже 
         находится
         Галеев 
         галерея.
         </p> 
         <p>
         В 
         ней 
         тоже 
         поисходят 
         выставки
         и 
         довольно 
         часто.
         </p>
         <p>
         Оставшийся 
         объект - 
         галерея
         "АРТЕФАКТ", 
         которая 
         больше 
         подходит 
         для 
         любителей
         неклассического 
         творчества
         .
         </p>
         <form 
         action="/index" 
         method="post" >
         <button 
         type="submit" 
         value="Войти" 
         aria-setsize="10px"
         >
         Вернуться назад
         </button>
         </form>
            <h2>
            Вернуться 
            на 
            главную 
            страницу 
            (кнопка 
            выше)
            </h2>
</body>
</html>
'''

# поле добавления рисунков


@app.route('/paintings', methods=['POST', 'GET'])
def add_painting():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html 
                        lang="en">
                          <head>
                            <meta 
                            charset="utf-8">
                            <meta 
                            name="viewport" 
                            content="width=device-width, 
                            initial-scale=1, 
                            shrink-to-fit=no">
                             <link 
                             rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link 
                            rel="stylesheet" 
                            type="text/css" 
                            href="{url_for('static', filename='css/style.css')}"
                            />
                            <title>
                            Загрузить 
                            рисунок
                            </title>
                          </head>
                          <body>
                            <h1>
                            Загрузить рисунок (поместите его в папку Изображения перед тем, как выберите его)
                            </h1>
                            <form 
                            method="post" 
                            enctype="multipart/form-data">
                               <div 
                               class="form-group">
                                    <label 
                                    for="photo">
                                    Выберите файл
                                    </label>
                                    <input 
                                    type="file"
                                     class="form-control-file" 
                                     id="photo" 
                                     name="file">
                                </div>
                                <button 
                                type="submit" 
                                class="btn btn-primary">
                                Отправить
                                </button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        file = request.files['file']
        file.save(f'{file.filename}')
        shutil.copy(f'/{os.path.abspath(file.filename)[3:]}', '/New_Website_Project/static/img')
        return redirect("/index")

# просмотр рисунков пользователей


@app.route('/gallery', methods=['GET'])
def show_gallery():
    p = Path("static/img")
    listoko = []
    for x in p.rglob("*"):
        listoko.append(f'<img src="{x}">')
    return f'''{'</br>'.join(listoko)}
<form 
         action="/index" 
         method="пуе" >
         <button type="submit" value="Войти" 
         aria-setsize="100px">вернуться на главную страницу</button></form>
            <h2>Вернуться 
            на 
            главную 
            страницу 
            (кнопка выше)</h2>'''

# страница информации о сайте


@app.route('/about', methods=['GET', 'POST'])
def talk_about_us():
    return '''
    <style>
    p{
    font-size: 40pt;
    }
    h1{
    font-size: 70pt;
    }
    button{
    font-size: 30pt;
    }
    </style>
    <h1>
    О
    НАС
    </h1>
<p>Данный 
ресурс 
представляет 
собой 
информационную 
площадку, 
связанную 
с 
творческим 
времяпрепровождением, 
а 
именно 
- 
рисованием.</p> 
<p>В 
нём 
можно 
задать 
интересующие 
вас 
вопросы, 
узнать, 
куда 
можно 
сходить,
        и, 
        может 
        быть, 
        получить 
        новые 
        знания.
</p>
<p>Надеемся, 
что 
вы 
сможете  
проявить 
себя 
и 
найти 
единомышленников 
в 
любимом 
деле.
</p>
<form action="/index" method="get" >
<button type="submit" 
value="Войти" 
aria-setsize="1000px">
Вернуться 
на 
главную
 страницу
 </button>
 </form>
 '''

# функция загрузки пользователей


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

# запуск программы


if __name__ == '__main__':
    main()
