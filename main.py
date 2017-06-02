from flask import Flask, request
import os, jinja2
import cgi

app = Flask(__name__)
app.config["DEBUG"] = True

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

todo_list = []

@app.route("/", methods = ["GET", "POST"])
def index():
    title = "To Do"
    if request.method == "POST":
        task_to_add = request.form['task']
        if task_to_add != "":
            todo_list.append(task_to_add)
    template = jinja_env.get_template("todo.html")
    return template.render(title = title, task = todo_list)

def main():
    app.run()

if __name__=="__main__":
    main()
