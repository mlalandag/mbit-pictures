FROM python:3.11

COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install -f /tmp/requirements.txt

COPY app.py /opt/

CMD ["waitress-serve", "--call", "pictures_api:create_app"]