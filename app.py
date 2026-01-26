from flask import Flask, render_template
from dotenv import load_dotenv
import os
from datetime import datetime
from pytz import timezone

load_dotenv()

app = Flask(__name__)

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

@app.route("/assignment")
def assignment():
    write_log("Visited Assignment Page")
    return render_template("assignment.html")

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