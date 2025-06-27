from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# File to store todos (acts as our "database")
TODOS_FILE = 'todos.json'

def load_todos():
    """Load todos from JSON file"""
    if os.path.exists(TODOS_FILE):
        try:
            with open(TODOS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_todos(todos):
    """Save todos to JSON file"""
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/')
def index():
    """Serve the main page with embedded CSS and JS"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do List App</title>
    <style>
        /* Reset and Base Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        /* Header */
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 30px 20px;
        }

        header h1 {
            font-size: 2.5em;
            font-weight: 300;
            margin: 0;
        }

        /* Main Content */
        main {
            padding: 30px;
        }

        /* Todo Input Section */
        .todo-input-section {
            margin-bottom: 30px;
        }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        #todoInput {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e1e8ed;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
        }

        #todoInput:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        #addBtn {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 80px;
        }

        #addBtn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        #addBtn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* Filter Section */
        .filter-section {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 30px;
        }

        .filter-btn {
            padding: 10px 20px;
            border: 2px solid #e1e8ed;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
            font-weight: 500;
        }

        .filter-btn:hover {
            border-color: #667eea;
            color: #667eea;
        }

        .filter-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: transparent;
        }

        /* Todo List */
        .todo-list {
            list-style: none;
            margin-bottom: 30px;
        }

        .todo-item {
            display: flex;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid #f0f0f0;
            transition: all 0.3s ease;
        }

        .todo-item:hover {
            background: #f8f9fa;
            margin: 0 -15px;
            padding-left: 15px;
            padding-right: 15px;
            border-radius: 10px;
        }

        .todo-item.completed {
            opacity: 0.6;
        }

        .todo-item.completed .todo-text {
            text-decoration: line-through;
            color: #888;
        }

        .todo-checkbox {
            width: 20px;
            height: 20px;
            border: 2px solid #ddd;
            border-radius: 50%;
            margin-right: 15px;
            cursor: pointer;
            position: relative;
            transition: all 0.3s ease;
            flex-shrink: 0;
        }

        .todo-checkbox:hover {
            border-color: #667eea;
        }

        .todo-checkbox.checked {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: #667eea;
        }

        .todo-checkbox.checked::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 12px;
            font-weight: bold;
        }

        .todo-text {
            flex: 1;
            font-size: 16px;
            line-height: 1.4;
            word-wrap: break-word;
            cursor: pointer;
        }

        .todo-text:hover {
            color: #667eea;
        }

        .todo-actions {
            display: flex;
            gap: 10px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .todo-item:hover .todo-actions {
            opacity: 1;
        }

        .todo-btn {
            padding: 8px 12px;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .edit-btn {
            background: #17a2b8;
            color: white;
        }

        .edit-btn:hover {
            background: #138496;
            transform: translateY(-1px);
        }

        .delete-btn {
            background: #dc3545;
            color: white;
        }

        .delete-btn:hover {
            background: #c82333;
            transform: translateY(-1px);
        }

        /* Todo Footer */
        .todo-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 20px;
            border-top: 1px solid #e1e8ed;
        }

        .todo-stats {
            color: #666;
            font-size: 14px;
        }

        .clear-btn {
            padding: 10px 20px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .clear-btn:hover {
            background: #c82333;
            transform: translateY(-1px);
        }

        .clear-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        /* Edit Mode */
        .todo-edit-input {
            flex: 1;
            padding: 8px 15px;
            border: 2px solid #667eea;
            border-radius: 20px;
            font-size: 16px;
            outline: none;
            margin-right: 10px;
        }

        .save-btn {
            background: #28a745;
            color: white;
        }

        .save-btn:hover {
            background: #218838;
        }

        .cancel-btn {
            background: #6c757d;
            color: white;
        }

        .cancel-btn:hover {
            background: #5a6268;
        }

        /* Utility Classes */
        .hidden {
            display: none;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
            font-style: italic;
        }

        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            border: 1px solid #f5c6cb;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }

        .empty-state h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
            color: #333;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                margin: 0;
                border-radius: 0;
                min-height: 100vh;
            }
            
            header h1 {
                font-size: 2em;
            }
            
            main {
                padding: 20px;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            .filter-section {
                flex-wrap: wrap;
            }
            
            .todo-footer {
                flex-direction: column;
                gap: 15px;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📝 My To-Do List</h1>
        </header>
        
        <main>
            <!-- Add Todo Form -->
            <div class="todo-input-section">
                <div class="input-group">
                    <input type="text" id="todoInput" placeholder="What needs to be done?" maxlength="100">
                    <button id="addBtn" onclick="addTodo()">Add</button>
                </div>
            </div>
            
            <!-- Filter Buttons -->
            <div class="filter-section">
                <button class="filter-btn active" onclick="filterTodos('all', this)">All</button>
                <button class="filter-btn" onclick="filterTodos('active', this)">Active</button>
                <button class="filter-btn" onclick="filterTodos('completed', this)">Completed</button>
            </div>
            
            <!-- Todo List -->
            <div class="todos-section">
                <ul id="todoList" class="todo-list">
                    <!-- Todos will be inserted here by JavaScript -->
                </ul>
            </div>
            
            <!-- Todo Stats and Actions -->
            <div class="todo-footer">
                <div class="todo-stats">
                    <span id="todoCount">0 items left</span>
                </div>
                <div class="todo-actions">
                    <button id="clearCompleted" onclick="clearCompleted()" class="clear-btn">
                        Clear Completed
                    </button>
                </div>
            </div>
        </main>
        
        <!-- Loading indicator -->
        <div id="loading" class="loading hidden">Loading...</div>
        
        <!-- Error message -->
        <div id="errorMessage" class="error-message hidden"></div>
    </div>
    
    <script>
        // Global variables
        let todos = [];
        let currentFilter = 'all';
        let editingId = null;

        // DOM elements
        const todoInput = document.getElementById('todoInput');
        const todoList = document.getElementById('todoList');
        const todoCount = document.getElementById('todoCount');
        const addBtn = document.getElementById('addBtn');
        const clearCompletedBtn = document.getElementById('clearCompleted');
        const loadingDiv = document.getElementById('loading');
        const errorDiv = document.getElementById('errorMessage');

        // Initialize app
        document.addEventListener('DOMContentLoaded', function() {
            loadTodos();
            setupEventListeners();
        });

        // Event listeners
        function setupEventListeners() {
            // Add todo on Enter key press
            todoInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    addTodo();
                }
            });
            
            // Enable/disable add button based on input
            todoInput.addEventListener('input', function() {
                addBtn.disabled = !todoInput.value.trim();
            });
        }

        // API functions
        async function apiCall(url, options = {}) {
            try {
                showLoading(true);
                const response = await fetch(url, {
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    },
                    ...options
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Something went wrong');
                }
                
                return await response.json();
            } catch (error) {
                showError(error.message);
                throw error;
            } finally {
                showLoading(false);
            }
        }

        // Load todos from server
        async function loadTodos() {
            try {
                todos = await apiCall('/api/todos');
                renderTodos();
                updateStats();
            } catch (error) {
                console.error('Failed to load todos:', error);
            }
        }

        // Add new todo
        async function addTodo() {
            const text = todoInput.value.trim();
            if (!text) return;
            
            try {
                const newTodo = await apiCall('/api/todos', {
                    method: 'POST',
                    body: JSON.stringify({ text })
                });
                
                todos.push(newTodo);
                todoInput.value = '';
                addBtn.disabled = true;
                renderTodos();
                updateStats();
                hideError();
            } catch (error) {
                console.error('Failed to add todo:', error);
            }
        }

        // Toggle todo completion
        async function toggleTodo(id) {
            const todo = todos.find(t => t.id === id);
            if (!todo) return;
            
            try {
                const updatedTodo = await apiCall(`/api/todos/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({ completed: !todo.completed })
                });
                
                // Update local todos array
                const index = todos.findIndex(t => t.id === id);
                todos[index] = updatedTodo;
                
                renderTodos();
                updateStats();
            } catch (error) {
                console.error('Failed to toggle todo:', error);
            }
        }

        // Delete todo
        async function deleteTodo(id) {
            try {
                await apiCall(`/api/todos/${id}`, {
                    method: 'DELETE'
                });
                
                // Remove from local array
                todos = todos.filter(t => t.id !== id);
                renderTodos();
                updateStats();
            } catch (error) {
                console.error('Failed to delete todo:', error);
            }
        }

        // Clear completed todos
        async function clearCompleted() {
            if (!todos.some(t => t.completed)) return;
            
            try {
                await apiCall('/api/todos/clear-completed', {
                    method: 'DELETE'
                });
                
                // Remove completed todos from local array
                todos = todos.filter(t => !t.completed);
                renderTodos();
                updateStats();
            } catch (error) {
                console.error('Failed to clear completed todos:', error);
            }
        }

        // Filter todos
        function filterTodos(filter, button) {
            currentFilter = filter;
            
            // Update filter buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            button.classList.add('active');
            
            renderTodos();
        }

        // Get filtered todos
        function getFilteredTodos() {
            switch (currentFilter) {
                case 'active':
                    return todos.filter(t => !t.completed);
                case 'completed':
                    return todos.filter(t => t.completed);
                default:
                    return todos;
            }
        }

        // Render todos
        function renderTodos() {
            const filteredTodos = getFilteredTodos();
            
            if (filteredTodos.length === 0) {
                renderEmptyState();
                return;
            }
            
            todoList.innerHTML = filteredTodos.map(todo => createTodoHTML(todo)).join('');
        }

        // Create HTML for a todo item
        function createTodoHTML(todo) {
            return `
                <li class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
                    <div class="todo-checkbox ${todo.completed ? 'checked' : ''}" 
                         onclick="toggleTodo(${todo.id})"></div>
                    <div class="todo-text">${escapeHtml(todo.text)}</div>
                    <div class="todo-actions">
                        <button class="todo-btn delete-btn" onclick="deleteTodo(${todo.id})">Delete</button>
                    </div>
                </li>
            `;
        }

        // Render empty state
        function renderEmptyState() {
            const messages = {
                all: {
                    title: "No todos yet!",
                    text: "Add your first todo above to get started."
                },
                active: {
                    title: "No active todos!",
                    text: "All your todos are completed. Great job! 🎉"
                },
                completed: {
                    title: "No completed todos!",
                    text: "Complete some todos to see them here."
                }
            };
            
            const message = messages[currentFilter];
            todoList.innerHTML = `
                <div class="empty-state">
                    <h3>${message.title}</h3>
                    <p>${message.text}</p>
                </div>
            `;
        }

        // Update stats
        function updateStats() {
            const activeTodos = todos.filter(t => !t.completed).length;
            const completedTodos = todos.filter(t => t.completed).length;
            
            todoCount.textContent = `${activeTodos} ${activeTodos === 1 ? 'item' : 'items'} left`;
            
            // Enable/disable clear completed button
            clearCompletedBtn.disabled = completedTodos === 0;
        }

        // Utility functions
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function showLoading(show) {
            loadingDiv.classList.toggle('hidden', !show);
        }

        function showError(message) {
            errorDiv.textContent = message;
            errorDiv.classList.remove('hidden');
            
            // Auto-hide error after 5 seconds
            setTimeout(hideError, 5000);
        }

        function hideError() {
            errorDiv.classList.add('hidden');
        }
    </script>
</body>
</html>
    '''

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    todos = load_todos()
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    """Add a new todo"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Todo text is required'}), 400
    
    todos = load_todos()
    
    # Create new todo with unique ID
    new_todo = {
        'id': len(todos) + 1,
        'text': data['text'].strip(),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    todos.append(new_todo)
    save_todos(todos)
    
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo (toggle completion or edit text)"""
    data = request.get_json()
    todos = load_todos()
    
    # Find the todo
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    # Update fields if provided
    if 'completed' in data:
        todo['completed'] = data['completed']
    if 'text' in data:
        todo['text'] = data['text'].strip()
    
    save_todos(todos)
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    todos = load_todos()
    
    # Filter out the todo to delete
    updated_todos = [t for t in todos if t['id'] != todo_id]
    
    if len(updated_todos) == len(todos):
        return jsonify({'error': 'Todo not found'}), 404
    
    save_todos(updated_todos)
    return jsonify({'message': 'Todo deleted successfully'})

@app.route('/api/todos/clear-completed', methods=['DELETE'])
def clear_completed():
    """Delete all completed todos"""
    todos = load_todos()
    active_todos = [t for t in todos if not t['completed']]
    save_todos(active_todos)
    return jsonify({'message': 'Completed todos cleared'})

if __name__ == '__main__':
    print("Starting Todo App...")
    print("Visit: http://127.0.0.1:8080")
    app.run(debug=True, host='127.0.0.1', port=8080)