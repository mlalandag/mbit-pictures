FROM python:3.11

COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

COPY . /opt/

CMD ["waitress-serve", "--call", "pictures_api:create_app"]