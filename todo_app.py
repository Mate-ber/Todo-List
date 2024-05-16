import json

from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anything'

def get():
    default_list = [
        'Develop Todo web application',
        'Add "add new item"',
        'Add "delete item" button'
        'Add "mark as done" button',
    ]

    try:
        with open(app.instance_path + '/todo_list.txt', 'r') as f:
            todo_from_file = json.load(f)
    except Exception as x:
        print(x)
        todo_from_file = default_list
    return todo_from_file


todo_list = get()
users = {'m': {'password': '1234', 'name': 'Zviadi'}}

# app.config('secret_key') = 'sad'


def save_to_file():
    with open(app.instance_path + '/todo_list.txt', 'w') as f:
        json.dump(todo_list, f)


def check_password(login, password):
    return users.get(login) and users[login]['password'] == password


@app.route('/')
def index():
    if not session.get('user_login'):
        return redirect(url_for('login'))
    return render_template('index.html', todo_list=todo_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_login'):
        flash('You are already logged in!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if check_password(login, password):
            session['user_login'] = login
            return redirect(url_for('index'))
        else:
            flash('User login failed.')
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_login', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        todo_item_text = request.form.get('task-text')
        todo_list.append(todo_item_text)
        save_to_file()
        return redirect(url_for('index'))
    return render_template('add_task.html')


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id: int):
    task_id = task_id - 1
    if 0 <= task_id < len(todo_list):
        task_remove = todo_list.pop(task_id)
        save_to_file()
        flash(f'Task {task_id+1} has been removed: {task_remove}')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
