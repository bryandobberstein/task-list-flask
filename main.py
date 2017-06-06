from flask import Flask, request, redirect, render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://todo:getitdone@localhost:3306/todo'
app.config['SQLALCHEMY_ECHO'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    completed = db.Column(db.Boolean)

    def __init__(self, name, completed = False):
        self.name = name
        self.completed = completed

@app.route("/", methods = ["GET", "POST"])
def index():
    title = "To Do"
    if request.method == "POST":
        task_to_add = request.form['task']
        if task_to_add != "":
            new_task = Task(task_to_add)
            db.session.add(new_task)
            db.session.commit()
    tasks = Task.query.filter_by(completed = False).all()
    complete_tasks = Task.query.filter_by(completed = True).all()

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

def main():
    app.run()

if __name__=="__main__":
    main()
