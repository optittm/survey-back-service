FROM python:3.8.8

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]