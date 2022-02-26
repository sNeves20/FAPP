FROM python:3.10

ADD . /home/developer

WORKDIR /home/developer

RUN pip3 install virtualenv
RUN python3 -m venv .env
RUN . .env/bin/activate
RUN pip3 install -r requirements.txt

CMD python3 -m uvicorn api:app --reload