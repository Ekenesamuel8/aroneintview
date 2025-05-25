import os
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLDB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
csrf = CSRFProtect(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)



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



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('login unsuccessfull')

    return render_template('auth/login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = Registerationform()
    if form.validate_on_submit():
        hash_psw = generate_password_hash(form.password.data)
        fresh_user = User(username=form.username.data, password=hash_psw)
        db.session.add(fresh_user)
        db.session.commit()
        flash('registration succefull, please login', 'success')
        return redirect(url_for("login"))

    return render_template('auth/register.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route("/")
def home():
    return render_template("main/home.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html")


if __name__== '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)