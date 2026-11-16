#!/bin/bash

echo "Starting Multi-User Q&A System Setup..."

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

echo "1. Creating Python Virtual Environment..."
python3 -m venv venv

echo "2. Activating Virtual Environment..."
source venv/bin/activate

echo "3. Installing Requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "4. Generating Sample PDF Documents..."
python generate_pdfs.py

echo "5. Starting the Streamlit Application..."
streamlit run app.py
