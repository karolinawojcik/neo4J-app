# coding=UTF-8
from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import User, get_shops, get_clients, get_workers
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route("/")
def index():
    shops = get_shops()
    return render_template("index.html", shops=shops)


@app.route("/search", methods=["POST"])
def search():
    shops = get_shops()
    usertype = request.form.get("usertype")
    shopname = request.form.get("shopname")
    if shopname and usertype:
        if usertype == "PRACOWNICY":
            users = get_workers(shopname)
        if usertype == "KLIENCI":
            users = get_clients(shopname)

    if users:
        return render_template("index.html", shops=shops, users=users, usertype=usertype, shopname=shopname)
    else:
        return render_template("index.html", shops=shops)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username = request.form["username"]
        name = request.form["name"]
        surname = request.form["surname"]
        age = request.form["age"]
        password = request.form["password"]

        user = User(username)

        if not user.register(name, surname, age, password):
            flash("Użytkownik o takiej nazwie już istnieje")
        else:
            flash("Użytkownik został dodany")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username)

        if not user.verify_password(password):
            flash("Niepoprawne hasło lub podany użytkownik nie istnieje")
        else:
            flash("Pomyślnie zalogowano")
            session["username"] = user.username
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/add_shop", methods=["POST"])
def add_shop():
    name = request.form["shopname"]
    if request.form.get("work"):
        work = True
    else:
        work = False

    if request.form.get("buy"):
        buy = True
    else:
        buy = False

    user = User(session["username"])

    if not name:
        flash("Podaj nazwę sklepu")
    else:
        user.add_shop(name, work, buy)

    return redirect(url_for("index"))


@app.route("/move_to_adding_page/<shop>")
def move_to_adding_page(shop):
    username = session.get("username")

    if not username:
        flash("Musisz być zalogowany")
        return redirect(url_for("login"))

    return render_template("add_to_my_list.html", shop=shop)


@app.route("/add_to_my_list/<shop>", methods=["POST"])
def add_to_my_list(shop):
    username = session.get("username")

    if not username:
        flash("Musisz być zalogowany")
        return redirect(url_for("login"))

    user = User(username)
    if request.form.get("work"):
        work = True
    else:
        work = False

    if request.form.get("buy"):
        buy = True
    else:
        buy = False

    user.add_to_my_list(shop, work, buy)
    return redirect(url_for("index"))


@app.route("/profile/<username>")
def profile(username):
    user = User(username)
    wherebuy = user.my_buy_shops()
    wherework = user.my_work_shops()

    return render_template("profile.html", username=username, buyshops=wherebuy, workshops=wherework)


@app.route("/logout")
def logout():
    session.pop("username")
    flash("Zostałeś wylogowany")
    return redirect(url_for("index"))
