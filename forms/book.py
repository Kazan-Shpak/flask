from flask_wtf import FlaskForm
from wtforms import FileField,  PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    title = StringField('Название книги', validators=[DataRequired()])
    author = StringField("Автор")
    path = StringField("Путь к файлу")
    file = FileField("Книга")
    submit = SubmitField('Добавить')
