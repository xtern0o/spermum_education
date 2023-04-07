from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    email = EmailField("Электронная почта", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired(), Length(min=2)])
    second_name = StringField("Фамилия", validators=[DataRequired(), Length(min=2)])
    invite_code = StringField("Пригласительный код")
    user_type_teacher = RadioField("Учитель")
    user_type_student = RadioField("Ученик")
    remember = BooleanField("Запомнить меня")
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Зарегистрироваться")
