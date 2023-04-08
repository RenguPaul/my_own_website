# импортируем нужные модули

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

# создаём форму рисунков


class PaintForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = FileField("О работе")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')