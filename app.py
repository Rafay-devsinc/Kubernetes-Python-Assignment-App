from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime
from pytz import timezone

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
# Use SQLite as fallback for development if DATABASE_URL is not set
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///assignment.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Task {self.title}>'

APP_NAME = os.getenv("APP_NAME", "Docker Demo App")
APP_ENV = os.getenv("APP_ENV", "development")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def write_log(message):
    pakistan_time = datetime.now(timezone('Asia/Karachi'))
    with open(f"{LOG_DIR}/app.log", "a") as f:
        f.write(f"{pakistan_time} - {message}\n")

@app.route("/")
def home():
    write_log("Visited Home Page")
    return render_template("index.html")

@app.route("/assignment", methods=['GET', 'POST'])
def assignment():
    write_log("Visited Assignment Page")
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        
        if title:
            new_task = Task(title=title, description=description, priority=priority)
            db.session.add(new_task)
            db.session.commit()
            write_log(f"Created new task: {title}")
            flash('Task created successfully!', 'success')
        else:
            flash('Task title is required!', 'error')
        
        return redirect(url_for('assignment'))
    
    # Get all tasks
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("assignment.html", tasks=tasks)

@app.route("/task/update/<int:task_id>", methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    status = request.form.get('status')
    
    if status:
        task.status = status
        db.session.commit()
        write_log(f"Updated task {task_id} status to {status}")
        flash('Task updated successfully!', 'success')
    
    return redirect(url_for('assignment'))

@app.route("/task/delete/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    write_log(f"Deleted task: {title}")
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('assignment'))

@app.route("/stats")
def stats():
    total_tasks = Task.query.count()
    pending_tasks = Task.query.filter_by(status='pending').count()
    in_progress_tasks = Task.query.filter_by(status='in_progress').count()
    completed_tasks = Task.query.filter_by(status='completed').count()
    
    high_priority = Task.query.filter_by(priority='high').count()
    medium_priority = Task.query.filter_by(priority='medium').count()
    low_priority = Task.query.filter_by(priority='low').count()
    
    statistics = {
        'total': total_tasks,
        'pending': pending_tasks,
        'in_progress': in_progress_tasks,
        'completed': completed_tasks,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority
    }
    
    write_log("Viewed task statistics")
    return render_template("stats.html", stats=statistics)

@app.route("/logs")
def logs():
    try:
        with open(f"{LOG_DIR}/app.log", "r") as f:
            log_content = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        log_content = ["No logs available."]
    return render_template("logs.html", logs=log_content)

@app.context_processor
def inject_env_variables():
    return {
        "app_name": os.getenv("APP_NAME", ""),
        "app_env": os.getenv("APP_ENV", "")
    }

@app.before_request
def reload_env_variables():
    load_dotenv()  # Reload the .env file before every request to reflect changes

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)