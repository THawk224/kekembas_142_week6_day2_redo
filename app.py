from flask import Flask, jsonify, request
from tasks import tasks_list

app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    if request.args.get('completed') == 'true':
        tasks = tasks.filter_by(completed=True)
    elif request.args.get('completed') == 'false':
        tasks = tasks.filter_by(completed=False)
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return 'Task not found', 404
    return jsonify(task.to_dict())

# Create a route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks_list)

# Create a route to get a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks_list if task['id'] == task_id]
    if task:
        return jsonify(task[0])
    else:
        return jsonify({'error': 'Task not found'}), 404
    
@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    dueDate = request.json.get('dueDate')
    created_at = datetime.datetime.now()
    id = len(tasks_list) + 1

    new_task = {
        'id': id,
        'title': title,
        'description': description,
        'completed': False,
        'createdAt': created_at,
        'dueDate': dueDate,
    }
    tasks_list.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not 'title' in data or not 'description' in data:
        return 'Invalid input', 400
    task = Task(title=data['title'], description=data.get('description'), completed=False)
    if 'due_date' in data:
        task.due_date = data['due_date']
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'due_date': self.due_date.strftime('%Y-%m-%d %H:%M:%S') if self.due_date else None
        }

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    if request.args.get('completed') == 'true':
        tasks = tasks.filter_by(completed=True)
    elif request.args.get('completed') == 'false':
        tasks = tasks.filter_by(completed=False)
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return 'Task not found', 404
    return jsonify(task.to_dict())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not 'title' in data: 