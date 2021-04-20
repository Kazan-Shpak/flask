from flask import Flask, render_template, redirect

# основной класс формы
from flask_wtf import FlaskForm
# типы полей: текстовое, пароль, логич(чекбокс), кнопка
from wtforms import StringField, PasswordField, BooleanField, SubmitField
# валидатор полей (введены данные или нет)
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success') # страница удачной авторизации
    return render_template('login1.html', title='Авторизация', form=form)

@app.route('/success')
def success():
    return render_template('success.html', title='Авторизация')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')



