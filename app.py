from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os
import uuid

app = Flask(__name__)
# Configure the Flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# globals
results = {}
tasks = []  # WARNING tasks is global, task is local 
pending_tasks = []
completed_tasks = []
current_endpoint = 0
user_computes = {}

@app.route('/')
def index():
    # Assign unique session ID if not already assigned
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/get_task')
def get_task():
    if len(tasks) == 0:
        return jsonify({"error": "No more tasks available"}), 404

    user_id = session['user_id']


    task = tasks.pop(0)  # Assign the next available task
    task_tuple = (task['a'], task['b'])
    pending_tasks.append(task_tuple)

    print(f"{user_id} requested task: {task}")
    print(f"pending tasks: {pending_tasks}")

    return jsonify(task)

@app.route('/cancel_task', methods=['POST'])
def cancel_task():
    task = request.json

    if not task:
        return jsonify({"error": "No task provided"}), 400

    # Convert back to tuple format if needed
    task_tuple = (task['a'], task['b'])
    
    # Add the task back to the beginning of the tasks list
    tasks.insert(0, task)
    # Remove the task from pending_tasks
    if task_tuple in pending_tasks:
        pending_tasks.remove(task_tuple)
    
    return jsonify({"message": "Task cancelled and added back to the queue"})


@app.route('/store_result', methods=['POST'])
def store_result():
    user_id = session['user_id']
    data = request.json
    print(f"data received: {data}")
    result = data['result']
    task_dict = data['task']
    task_tuple = (task_dict['a'], task_dict['b'])
    global current_endpoint
    current_endpoint = task_tuple[1]
    results[task_tuple] = result
    pending_tasks.remove(task_tuple)
    user_computes[user_id] = (task_tuple)
    print(f"Received result from {user_id}: {result}")
    return jsonify({'status': 'success'})

# Additional route to view all results (for demonstration)
@app.route('/result')
def view_results():
    total_integral = sum(results.values())

    return 'up to ' + str(current_endpoint) + ': ' + str(total_integral)

def clear_pending():
    # primitive way to clear all pending tasks (not good if someone is still working)
    while len(pending_tasks) > 0:
        task = pending_tasks[-1]
        pending_tasks.pop[-1]
        tasks.insert(0, task)

def gen_tasks(start, end, num_chunks):
    chunk_size = (end - start) / num_chunks
    current_start = start

    for _ in range(num_chunks):
        task = {"a": current_start, "b": current_start + chunk_size}
        tasks.append(task)
        current_start += chunk_size

if __name__ == '__main__':
    # configure the function and steps_per_chunk in index.html compute integral function
    # each chunk has n steps

    start = 0
    end = 10000
    num_chunks = 100

    gen_tasks(start, end, num_chunks)

    print(len(tasks))

    app.run(debug=True)
