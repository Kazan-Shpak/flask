import os

from flask import Flask, render_template, send_from_directory
from werkzeug.utils import redirect, secure_filename
from forms.user import RegisterForm
from data import db_session
from data.users import User
from data.books import Books
from forms.loginform import LoginForm
from forms.book import AddForm

app = Flask(__name__, static_folder='pdf')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER' ] = 'pdf'


def main():
    db_session.global_init("db/books.db")
    app.run()


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    books = db_sess.query(Books).all()
    return render_template("index.html", books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.username.data).first()
        if user and user.hashed_password == form.password.data:
            return redirect('/index')

        return redirect(('/login'))
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addbooks', methods=['GET', 'POST'])
def addbooks():
    form = AddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        book = Books(
            title=form.title.data,
            author=form.author.data,
            path=form.file.data.filename
        )
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], form.file.data.filename)
        form.file.data.save(file_path)
        db_sess.add(book)
        db_sess.commit()
        return redirect('/index')
    return render_template('addbooks.html', title='Добавление книги', form=form)


@app.route('/register', methods=[ 'GET', 'POST' ])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            login=form.login.data,
            status="user",
            hashed_password=form.password.data
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/pdf')
@app.route('/pdf/<path:filename>', methods=[ 'GET', 'POST' ])
def download(filename):
    return send_from_directory(directory='pdf', filename=filename)


if __name__ == '__main__':
    main()
