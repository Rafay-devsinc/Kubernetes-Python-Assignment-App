# Docker Python Assignment App

## Features

### Task Management System
- **Create Tasks**: Add tasks with title, description, and priority (low, medium, high)
- **Update Status**: Change task status between pending, in progress, and completed
- **Delete Tasks**: Remove tasks from the system
- **View Statistics**: Track task completion rates and priority distribution
- **PostgreSQL Integration**: All tasks are stored in a PostgreSQL database

### Application Pages
- **Home**: Landing page with application overview
- **Assignment**: Task management interface with CRUD operations
- **Statistics**: Visual dashboard showing task metrics and completion rates
- **Logs**: Application activity logs with timestamps

## Docker (Resources Task)
Resources: must understand this Repo and dockerize the app

# Instructions for Dockerizing the Python App

## Steps to Run the App Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Rafay-devsinc/Docker-Python-Assignment-App.git
   cd Docker-Python-Assignment-App
   ```

2. **Setup PostgreSQL Database**:
   - Install PostgreSQL if not already installed:
     ```bash
     # macOS
     brew install postgresql
     brew services start postgresql
     
     # Ubuntu/Debian
     sudo apt-get install postgresql postgresql-contrib
     sudo systemctl start postgresql
     ```
   
   - Create database and user:
     ```bash
     # Connect to PostgreSQL
     psql postgres
     
     # In PostgreSQL shell, run:
     CREATE DATABASE assignment_db;
     CREATE USER postgres WITH PASSWORD 'postgres';
     GRANT ALL PRIVILEGES ON DATABASE assignment_db TO postgres;
     \q
     ```

3. **Create a `.env` File**:
   - Use the provided `.env.example` file as a reference.
   - Copy the `.env.example` file to `.env` in the root directory:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your values:
     ```
     APP_NAME=Task Management App
     APP_ENV=development
     DATABASE_URL=postgresql://postgres:postgres@localhost:5432/assignment_db
     ```

4. **Install Dependencies**:
   - Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
     ```
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Initialize the Database**:
   - Create database tables:
     ```bash
     python init_db.py
     ```
   - This will create the `tasks` table in your PostgreSQL database.

5. **Run the App Locally**:
   - Start the app:
     ```bash
     python app.py
     ```
   - Open your browser and navigate to `http://127.0.0.1:5001` to test the app.

6. **Verify Everything Works**:
   - Navigate to different pages:
     - Home: `http://127.0.0.1:5001/`
     - Assignment (Task Management): `http://127.0.0.1:5001/assignment`
     - Statistics: `http://127.0.0.1:5001/stats`
     - Logs: `http://127.0.0.1:5001/logs`
   - Create a few tasks with different priorities
   - Update task statuses
   - View statistics to see task metrics
   - Check that logs are being written to the `logs/app.log` file.

---

## Steps to Dockerize the App

1. **Create a `Dockerfile` in the Root Directory**
   - Add Named volume for app.logs 
   - Add Bind volume for app updation
   - copy .env file

   
2. **Build the Docker Image**:
  

3. **Run the Docker Container**:
   

4. **Test the Dockerized App**:
   - Open your browser and navigate to `http://127.0.0.1:5001` to test the app.
   - Verify that the app works as expected and logs are being written to the `app_logs` volume.
   - When restart the container or start new container previous logs are displayed.

---

By following these steps, you will successfully dockerize the Python app and ensure it works both locally and in a Docker container. Good luck!# Docker-Python-Assignment-App
