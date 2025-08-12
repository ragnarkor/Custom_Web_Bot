#!/bin/bash

# Start Smart Play Bot Scheduler
echo "Starting Smart Play Bot Scheduler..."

# Check if virtual environment exists
if [ ! -d "../Smart_Play_Bot/venv" ]; then
    echo "Virtual environment not found in ../Smart_Play_Bot/venv"
    echo "Please create virtual environment first"
    exit 1
fi

# Activate virtual environment
source ../Smart_Play_Bot/venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Start scheduler
echo "Launching scheduler..."
python scheduler.py
