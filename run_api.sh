python -m venv fapp
source fapp/bin/activate
pip install -r requirements.txt
cd API/
uvicorn api:app --reload