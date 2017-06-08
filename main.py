from flask import Flask, flash, request, redirect, render_template, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://todo:getitdone@localhost:3306/todo'
app.config['SQLALCHEMY_ECHO'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Onn7Opjufsyi"

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(30))
    tasks = db.relationship("Task", backref = "owner")

    def __init__(self, email, password):
        self.email = email
        self.password = password

def password_verify(password, verify):
    if len(password) != len(verify):
        return False
    for i in range(len(password)):
        if password[i] != verify[i]:
            return False

    return True

@app.before_request
def require_login():
    allowed_routes = ["login", "register"]
    if request.endpoint not in allowed_routes and "email" not in session:
        return redirect("/login")

@app.route("/", methods = ["GET", "POST"])
def index():
    title = "To Do"
    owner = User.query.filter_by(email = session["email"]).first()
    if request.method == "POST":
        task_to_add = request.form['task']
        if task_to_add != "":
            new_task = Task(task_to_add, owner)
            db.session.add(new_task)
            db.session.commit()
    tasks = Task.query.filter_by(completed = False, owner = owner).all()
    complete_tasks = Task.query.filter_by(completed = True, owner = owner).all()

    return render_template("todo.html", title = title, task = tasks, complete_tasks = complete_tasks)

@app.route("/delete_task", methods = ["POST"])
def delete_task():
    task_to_delete = int(request.form["task_id"])
    task = Task.query.get(task_to_delete)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect("/")

@app.route("/add_task", methods = ["POST"])
def add_task():
    task_to_add = int(request.form["task_add"])
    task = Task.query.get(task_to_add)
    task.completed = False
    db.session.add(task)
    db.session.commit()

    return redirect("/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    email = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email = email).first()
        if user and user.password == password:
            session["email"] = email
            flash("Login successful", "success")
            return redirect("/")
        else:
            flash("Incorrect email or password", "error")

    return render_template("login.html", title = "Login", email = email)

@app.route("/logout")
def logout():
    del session["email"]
    flash("Logged out", "success")
    return redirect("/login")

@app.route("/register", methods = ["POST", "GET"])
def register():
    email = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        verify = request.form["verify"]
        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email already registered", "error")
        elif not password_verify(password, verify):
            flash("Password and verify do not match", "error")
        else:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session["email"] = email
            flash("Registration successful", "success")
            return redirect("/")

    return render_template("register.html", title = "Register", email = email)

def main():
    app.run()

if __name__=="__main__":
    main()
