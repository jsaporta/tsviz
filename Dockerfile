FROM python:3.11-slim-bullseye
WORKDIR /app
ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
ADD bokeh-server.py /app
EXPOSE 5006
CMD bokeh serve --port 5006 --allow-websocket-origin='*' bokeh-server.py
