from flask import Flask, session, request, flash, render_template, redirect, url_for
import os

from db_code import get_content, get_user, add_user

authorized = False
registered = False

def start_site(site_id):
    session["site"] = site_id

def end_site():
    session.clear()

def site_form():
    site_list = get_content()

    return render_template("main.html", site_list= site_list)

def index():
    if authorized:
        if request.method == "GET":
            start_site(-1)
            return site_form()
        else:
            site_id = request.form.get("site")
            start_site(site_id)
            return redirect(url_for("test"))
    else:
        return redirect(url_for("authorization"))
    

def authorization():
    global authorized
    if request.method == "POST":
        login_input = request.form.get("login")
        password_input = request.form.get("password")
        #print(f"Введено: {login_input=}, {password_input=}")

        user = get_user(login_input, password_input)
        #print(f"Знайдено в БД: {user=}")

        if user and user[1] == login_input:
            authorized = True
            return redirect(url_for("index"))
        else:
            flash("Невірний логін або пароль", "error")
            return redirect(url_for("authorization"))

    return render_template("authorization.html")

def registration():
    global registered
    if request.method == "POST":
        user = request.form.copy()
        add_user(user)
        print(user)
        session['user_photo'] = user[4]
        login = request.form.get("login")
        password = request.form.get("password")

        if not login or not password:
            flash("Це поле обов'язкове", "error")
            return redirect(url_for("registration"))
        #login_input = request.form.get("login")
        #name_input = request.form.get("name")
        #password_input = request.form.get("password")
        #confirm_password_input = request.form.get("confirm_password")
        #image_input = request.form.get("image")
        #about_input = request.form.get("about")
        #print(f"Введено: {login_input=}, {password_input=}")

        #print(f"Знайдено в БД: {user=}")

        #if login_input == pass:
        #    pass

        #else:
        #    flash("Заповніть це поле", "error")
        #    return redirect(url_for("registration"))

        return redirect(url_for("authorization"))
        #else:
        #    flash("Паролі не співпадають", "error")
        #    return redirect(url_for("registration"))

    return render_template("registration.html")

#def profile():
#    if not session.get("authorized"):
#        return redirect(url_for("authorization"))

    #user_id = session.get("user_id")
    #open()
    #user = curs.execute("SELECT login, name, about, photo FROM user WHERE id=?", (user_id,)).fetchone()
    #close()
    #return render_template("profile.html", user=user)

folder = os.getcwd()

app = Flask(__name__, template_folder="template", static_folder="static")
app.add_url_rule("/", "index", index, methods= ["post", "get"])
app.add_url_rule("/index", "index", index, methods= ["post", "get"])
app.add_url_rule("/authorization", "authorization", authorization, methods= ["post", "get"])
app.add_url_rule("/registration", "registration", registration, methods= ["post", "get"])

app.config["SECRET_KEY"] = "gbasjmlfkajgmlfsfsaf"

if __name__ == "__main__":
    app.run()
