from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from ..models import User



class Registerationform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=48)])
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=30)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("this username already exist")

class Loginform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=48)])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField("login")

