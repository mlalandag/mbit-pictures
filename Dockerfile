FROM python:3.11

COPY requirements.txt /tmp/

RUN pip install -f /tmp/requirements.txt

COPY app.py /opt/

CMD ["python3", "/opt/app.py"]