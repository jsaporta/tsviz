FROM python:3.11-slim-bullseye
WORKDIR /app
ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
ADD raw-data.py /app
CMD python raw-data.py
