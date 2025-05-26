from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_arch = Blueprint('main', __name__, template_folder='templates')

@main_arch.route("/")
def home():
    return render_template("main/home.html")


@main_arch.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html", name=current_user.username)

