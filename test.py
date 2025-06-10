from flask import Flask, session, request, flash, render_template, redirect, url_for
import os

from db_code import get_content, get_photo, get_user_by_id, get_user, add_user

authorized = False
registered = False

def start_site(site_id):
    session["site"] = site_id

def end_site():
    session.clear()

def main():
    #site_list = get_content()

    return render_template("main.html")

def index():
    if request.method == "GET":
        start_site(-1)
        return main()
    else:
        site_id = request.form.get("site")
        start_site(site_id)
        return redirect(url_for("main"))
    
def authorization():
    global authorized
    if request.method == "POST":
        login_input = request.form["login"]
        password_input = request.form["password"]
        user = get_user(login_input, password_input)
        session['user'] = user
        if user and user[1] == login_input:
            authorized = True
            #session['user_id'] = session['login'][0]
            return redirect(url_for("main"))
        else:
            flash("Невірний логін або пароль", "error")
            return redirect(url_for("authorization"))

    return render_template("authorization.html")

def registration():
    global registered
    if request.method == "POST":
        login = request.form.get("login")
        name = request.form.get("name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmpassword")
        about = request.form.get("about")
        #user_photo = request.form.get("photo")

        if not login or not password:
            flash("Заповніть всі поля!", "error")
            return redirect(url_for("registration"))
        
        if password == confirm_password:
            user = request.form.copy()
            add_user(user)
            return redirect(url_for("authorization"))
        else:
            flash("Паролі не співпадають!", "error")
            return redirect(url_for("registration"))

        #print(f"Введено: {login_input=}, {password_input=}")
        #print(f"Знайдено в БД: {user=}")
        

    return render_template("registration.html")

def reset_password():
    return render_template("reset_pas.html")

def profile():
    global authorized
    if request.method == "POST":
        authorized = False
        session.clear()
        return redirect(url_for("main"))

    if not authorized:
        return redirect(url_for("authorization"))

    user = get_user_by_id(session['user'][0])
    #print(user)
    if not user:
        return "Користувача не знайдено"

    a = get_photo(session['user'][0])
    #with open(f"static/{session['user'][1]}.png", "wb") as file:
    #    file.write(a)

    #photo = (f"static/{session['user'][1]}.png") if (f"static/{session['user'][1]}.png") else url_for('static', filename='no_photo.png')
    if a and a[0]:
        filename = f"{session['user'][1]}.png"
        filepath = f"static/{filename}"
        with open(filepath, "wb") as file:
            file.write(a[0])
        photo = filepath
    else:
        photo = url_for('static', filename='no_photo.png')

    return render_template(
        "profile.html",
        us_login=user[0],
        us_name=user[1],
        us_about=user[2],
        us_photo=photo
    )

#main pages

def events():
    return render_template("events.html")

def edits():
    return render_template("edits.html")

def new_pages():
    return render_template("new_pages.html")

def random():
    return render_template("random.html")

def special():
    return render_template("special.html")

def community():
    return render_template("community.html")

def knaipa():
    return render_template("knaipa.html")

def help():
    return render_template("help.html")

def media():
    return render_template("media.html")


#secondary pages

def selected_articles():
    return render_template("selected_articles.html")


folder = os.getcwd()

app = Flask(__name__, template_folder="template", static_folder="static")
app.add_url_rule("/", "index", index, methods= ["post", "get"])
app.add_url_rule("/index", "index", index, methods= ["post", "get"])
app.add_url_rule("/authorization", "authorization", authorization, methods= ["post", "get"])
app.add_url_rule("/registration", "registration", registration, methods= ["post", "get"])
app.add_url_rule("/reset-password", "reset_pas", reset_password, methods= ["post", "get"])
app.add_url_rule("/profile", "profile", profile, methods= ["post", "get"])

app.add_url_rule("/main", "main", main, methods= ["post", "get"])

app.add_url_rule("/events", "events", events, methods= ["post", "get"])
app.add_url_rule("/edits", "edits", edits, methods= ["post", "get"])
app.add_url_rule("/new-pages", "new-pages", new_pages, methods= ["post", "get"])
app.add_url_rule("/random", "random", random, methods= ["post", "get"])
app.add_url_rule("/special", "special", special, methods= ["post", "get"])
app.add_url_rule("/community", "community", community, methods= ["post", "get"])
app.add_url_rule("/knaipa", "knaipa", knaipa, methods= ["post", "get"])
app.add_url_rule("/help", "help", help, methods= ["post", "get"])
app.add_url_rule("/media", "media", media, methods= ["post", "get"])

app.add_url_rule("/selected-articles", "selected_articles", selected_articles, methods= ["post", "get"])

app.config["SECRET_KEY"] = "gbasjmlfkajgmlfsfsaf"

if __name__ == "__main__":
    app.run()
