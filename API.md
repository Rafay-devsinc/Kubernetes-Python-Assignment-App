# API Documentation

## Task Management Endpoints

### 1. Home Page
**URL**: `/`  
**Method**: `GET`  
**Description**: Landing page with app information  
**Response**: HTML page

---

### 2. View All Tasks
**URL**: `/assignment`  
**Method**: `GET`  
**Description**: Display all tasks with create form  
**Response**: HTML page with task list

---

### 3. Create Task
**URL**: `/assignment`  
**Method**: `POST`  
**Description**: Create a new task

**Form Parameters**:
- `title` (required, string): Task title (max 200 characters)
- `description` (optional, text): Task description
- `priority` (optional, string): Task priority - 'low', 'medium', or 'high' (default: 'medium')

**Example**:
```html
<form method="POST" action="/assignment">
    <input name="title" value="Complete project documentation" required>
    <textarea name="description">Write comprehensive docs</textarea>
    <select name="priority">
        <option value="high">High</option>
    </select>
    <button type="submit">Create Task</button>
</form>
```

**Response**: Redirect to `/assignment` with flash message

---

### 4. Update Task Status
**URL**: `/task/update/<int:task_id>`  
**Method**: `POST`  
**Description**: Update task status

**URL Parameters**:
- `task_id` (required, integer): ID of the task to update

**Form Parameters**:
- `status` (required, string): New status - 'pending', 'in_progress', or 'completed'

**Example**:
```html
<form method="POST" action="/task/update/1">
    <select name="status">
        <option value="pending">Pending</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
    </select>
</form>
```

**Response**: Redirect to `/assignment` with flash message

---

### 5. Delete Task
**URL**: `/task/delete/<int:task_id>`  
**Method**: `POST`  
**Description**: Delete a task

**URL Parameters**:
- `task_id` (required, integer): ID of the task to delete

**Example**:
```html
<form method="POST" action="/task/delete/1" onsubmit="return confirm('Are you sure?');">
    <button type="submit">Delete</button>
</form>
```

**Response**: Redirect to `/assignment` with flash message

---

### 6. View Statistics
**URL**: `/stats`  
**Method**: `GET`  
**Description**: Display task statistics and metrics

**Response**: HTML page with statistics including:
- Total tasks count
- Tasks by status (pending, in progress, completed)
- Tasks by priority (low, medium, high)
- Completion rate percentage
- Active tasks count

---

### 7. View Logs
**URL**: `/logs`  
**Method**: `GET`  
**Description**: Display application logs  
**Response**: HTML page with log entries

---

## Task Model

### Fields
- `id` (Integer): Primary key, auto-increment
- `title` (String, 200): Task title (required)
- `description` (Text): Task description (optional)
- `status` (String, 20): Current status (default: 'pending')
  - Valid values: 'pending', 'in_progress', 'completed'
- `priority` (String, 20): Task priority (default: 'medium')
  - Valid values: 'low', 'medium', 'high'
- `created_at` (DateTime): Creation timestamp (auto-generated)
- `updated_at` (DateTime): Last update timestamp (auto-updated)

---

## Flash Messages

The application uses Flask's flash messaging system for user feedback:

**Success Messages**:
- "Task created successfully!" - After creating a task
- "Task updated successfully!" - After updating task status
- "Task deleted successfully!" - After deleting a task

**Error Messages**:
- "Task title is required!" - When trying to create task without title

**Accessing in Templates**:
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

---

## Status Codes

- **200 OK**: Successful GET request
- **302 Found**: Redirect after POST request
- **404 Not Found**: Task not found (e.g., invalid task_id)

---

## Logging

All operations are logged to `logs/app.log` with Pakistan timezone timestamps:
- Page visits
- Task creation
- Task updates
- Task deletions
- Statistics views

**Log Format**:
```
2026-01-30 17:30:45.123456+05:00 - Created new task: Complete documentation
```
