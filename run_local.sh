#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting Flask application..."
echo "Open your browser and go to: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py


