FROM python:3.10

COPY . .

EXPOSE 8000

RUN python -m pip install -r requirements.txt

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]