# Database Operations Guide

## Database Schema

### Tasks Table
The application uses a single `tasks` table with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| title | String(200) | Task title (required) |
| description | Text | Task description (optional) |
| status | String(20) | Task status: 'pending', 'in_progress', 'completed' |
| priority | String(20) | Task priority: 'low', 'medium', 'high' |
| created_at | DateTime | Timestamp when task was created |
| updated_at | DateTime | Timestamp when task was last updated |

## Database Connection

The application connects to PostgreSQL using SQLAlchemy. Configuration is loaded from environment variables:

```python
DATABASE_URL=postgresql://username:password@host:port/database_name
```

Default: `postgresql://postgres:postgres@localhost:5432/assignment_db`

## Available Operations

### 1. Create Task
**Endpoint**: `POST /assignment`
**Parameters**:
- `title` (required): Task title
- `description` (optional): Task description
- `priority` (optional): Task priority (default: 'medium')

### 2. Update Task Status
**Endpoint**: `POST /task/update/<task_id>`
**Parameters**:
- `status`: New status ('pending', 'in_progress', 'completed')

### 3. Delete Task
**Endpoint**: `POST /task/delete/<task_id>`

### 4. View All Tasks
**Endpoint**: `GET /assignment`
Returns all tasks ordered by creation date (newest first)

### 5. View Statistics
**Endpoint**: `GET /stats`
Returns:
- Total tasks
- Count by status (pending, in progress, completed)
- Count by priority (low, medium, high)
- Completion rate
- Active tasks count

## Database Commands

### Initialize Database
Create all tables:
```bash
python init_db.py
```

### Connect to Database (PostgreSQL CLI)
```bash
psql -U postgres -d assignment_db
```

### Useful SQL Queries

View all tasks:
```sql
SELECT * FROM tasks ORDER BY created_at DESC;
```

Count tasks by status:
```sql
SELECT status, COUNT(*) FROM tasks GROUP BY status;
```

Count tasks by priority:
```sql
SELECT priority, COUNT(*) FROM tasks GROUP BY priority;
```

Delete all tasks:
```sql
TRUNCATE TABLE tasks RESTART IDENTITY;
```

## Backup and Restore

### Backup Database
```bash
pg_dump -U postgres assignment_db > backup.sql
```

### Restore Database
```bash
psql -U postgres assignment_db < backup.sql
```

## Troubleshooting

### Connection Issues
- Ensure PostgreSQL is running: `brew services list` (macOS) or `systemctl status postgresql` (Linux)
- Check credentials in `.env` file
- Verify database exists: `psql -U postgres -l`

### Table Not Found
- Run initialization script: `python init_db.py`

### Permission Denied
- Grant privileges to user:
```sql
GRANT ALL PRIVILEGES ON DATABASE assignment_db TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
```
