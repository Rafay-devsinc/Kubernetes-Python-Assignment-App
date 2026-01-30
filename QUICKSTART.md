# Quick Start Guide

## ✅ All Dependencies Installed!

The application is now configured to use **SQLite** (no PostgreSQL setup needed for development).

## 🚀 Run the Application

### Option 1: Using the start script
```bash
./start.sh
```

### Option 2: Manual start
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # if not already activated

# Initialize database (first time only)
python3 init_db.py

# Start the app
python3 app.py
```

## 🌐 Access the Application

Open your browser and visit:
- **Home**: http://127.0.0.1:5001/
- **Task Management**: http://127.0.0.1:5001/assignment
- **Statistics**: http://127.0.0.1:5001/stats
- **Logs**: http://127.0.0.1:5001/logs

## 📝 Test the Features

1. **Create a task**:
   - Go to `/assignment`
   - Fill in the form with a title, description, and priority
   - Click "Create Task"

2. **Update task status**:
   - Use the dropdown in any task card to change status
   - It auto-saves on selection

3. **View statistics**:
   - Go to `/stats`
   - See task counts, completion rate, and priority distribution

4. **Delete a task**:
   - Click the "Delete" button on any task card
   - Confirm the deletion

## 🗄️ Database

- **Type**: SQLite (file-based, no server needed)
- **Location**: `assignment.db` in the project root
- **Tables**: `tasks` with full CRUD operations

## 🔄 Switch to PostgreSQL Later (Optional)

If you want to use PostgreSQL later:

1. **Start PostgreSQL** (via Docker):
   ```bash
   docker run -d \
     --name postgres-assignment \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=assignment_db \
     -p 5432:5432 \
     postgres:14-alpine
   ```

2. **Update .env**:
   ```bash
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/assignment_db
   ```

3. **Reinitialize database**:
   ```bash
   python3 init_db.py
   ```

## 🛑 Stop the Application

Press `CTRL+C` in the terminal where the app is running.

## 📋 Notes

- SQLite is perfect for development and testing
- All features work identically with SQLite or PostgreSQL
- Database file is portable - you can copy `assignment.db` to backup your data
- Logs are stored in `logs/app.log`
