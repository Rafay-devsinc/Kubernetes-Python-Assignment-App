#!/bin/bash

echo "🚀 Starting Task Management App..."
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Run: source venv/bin/activate"
    echo ""
fi

# Check if database exists
if [ ! -f "assignment.db" ]; then
    echo "📊 Creating database..."
    python3 init_db.py
    echo ""
fi

# Start the app
echo "🌐 Starting Flask app on http://127.0.0.1:5001"
echo "Press CTRL+C to stop"
echo ""
python3 app.py
