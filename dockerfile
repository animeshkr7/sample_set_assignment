FROM python:3.9-slim-buster

WORKDIR /
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install -e .

COPY  . .

CMD ["python" , "run_both.py"]
