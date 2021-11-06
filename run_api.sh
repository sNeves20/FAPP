#!/usr/bin/env bash
python3 -m venv fapp
. fapp/bin/activate
echo "   Installing Required Files in the Virtual Environment"
pip3 install -r requirements.txt
echo "\n   Starting the API:"
cd API/
python3 -m uvicorn api:app --reload