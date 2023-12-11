FROM python:3.8-slim-buster



COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./app
WORKDIR ./app/service
ENV PYTHONPATH /app
CMD ["gunicorn", "--workers=12", "--threads=6", "--bind", "0.0.0.0:80", "application:run_app()"]