FROM python:3.9

WORKDIR /code

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000