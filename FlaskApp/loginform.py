from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms import IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Введите почту', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Ваше имя', validators=[DataRequired()])
    about = TextAreaField("Если вы крьер, введите кодовое слово")
    submit = SubmitField('Войти')


class NewsForm(FlaskForm):
    title = StringField('Товар', validators=[DataRequired()])
    prices = IntegerField("Стоимость")
    content = TextAreaField("Описание")
    submit = SubmitField('Применить')


class ReviewForm(FlaskForm):
    title = StringField('Оценка из 10', validators=[DataRequired()])
    content = TextAreaField("Ваш отзыв")
    submit = SubmitField('Отправить')
