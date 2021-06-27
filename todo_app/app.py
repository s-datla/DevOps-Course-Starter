from flask import Flask, render_template, request, redirect
import todo_app.data.session_items as todoController
from todo_app.data.ViewModel import ViewModel

def create_app():
    app = Flask(__name__)
    # We specify the full path and remove the import for this config so
    # it loads the env variables when the app is created, rather than when this file is imported
    app.config.from_object('todo_app.flask_config.Config')
    
    
    @app.route('/')
    def index():
        todo_items = todoController.get_items()
        item_view_model = ViewModel(todo_items)
        return render_template('index.html',view_model=item_view_model)

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
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
