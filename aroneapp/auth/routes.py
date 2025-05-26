from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required   
from ..models import User
from .form import Registerationform, Loginform
from ..extensions import db

auth_arch = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')


@auth_arch.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('login successful', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('login unsuccessfull')

    return render_template('auth/login.html', form=form)


@auth_arch.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = Registerationform()
    if form.validate_on_submit():
        hash_psw = generate_password_hash(form.password.data)
        fresh_user = User(username=form.username.data, password=hash_psw)
        db.session.add(fresh_user)
        db.session.commit()
        flash('registration succefull, please login', 'success')
        return redirect(url_for("auth.login"))

    return render_template('auth/register.html', form=form)



@auth_arch.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
