FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY task_manager /app

CMD ["gunicorn", "task_manager.wsgi:application", "--bind", "0.0.0.0:5000"]
