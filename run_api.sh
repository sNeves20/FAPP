#!/usr/bin/env bash
python -m venv fapp
. fapp/bin/activate
echo "   Installing Required Files in the Virtual Environment"
pip install -r requirements.txt
echo "\n   Starting the API:"
cd API/
uvicorn api:app --reload