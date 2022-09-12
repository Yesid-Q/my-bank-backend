FROM python:3.10.6-alpine3.15

WORKDIR /src/app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]