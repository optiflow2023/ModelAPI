FROM python:3.8-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./model.pkl /app/
COPY ./api.py /app/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
