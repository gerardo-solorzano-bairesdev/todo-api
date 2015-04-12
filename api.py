from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

todos = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@app.route('/')
def index():
    return "Hej, varlden!"

@app.route('/api/todos/', methods=['GET'])
def list_todos():
    return jsonify({'todos': todos})

@app.route('/api/todos/', methods=['POST'])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)

    todo = {
        'id': todos[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    todos.append(todo)

    return jsonify(todo), 201

@app.route('/api/todos/<int:id>', methods=['GET'])
def read_todo(id):
    todo = [t for t in todos if t['id'] == id]

    if len(todo) == 0:
        abort(404)

    return jsonify(todo[0])

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = [t for t in todos if t['id'] == id]

    if len(todo) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    todo[0]['title'] = request.json.get('title', todo[0]['title'])
    todo[0]['description'] = request.json.get('description', todo[0]['description'])
    todo[0]['done'] = request.json.get('done', todo[0]['done'])
    return jsonify(todo[0])

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = [t for t in todos if t['id'] == id]
    if len(todo) == 0:
        abort(404)
    todos.remove(todo[0])
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)