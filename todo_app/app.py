from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config
import todo_app.data.session_items as todoController

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    todo_items = todoController.get_items()
    return render_template('index.html', todo_items=todo_items)

@app.route('/', methods=['POST'])
def add_new_todo():
    if 'submit' in request.form and 'title' in request.form:
        title = request.form['title']
        if todoController.add_item(title):
            return redirect('/')
    return render_template('error.html')

@app.route('/move/<id>')
def moveToDo(id):
    if id:
        item = todoController.get_item(id)
        if not item == None:
            if todoController.save_item(item):
                return redirect('/')
    return render_template('error.html')
            

if __name__ == '__main__':
    app.run()
