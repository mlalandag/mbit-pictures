FROM python:3.11

WORKDIR /pictures_api

COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

COPY . /pictures_api/

CMD ["waitress-serve", "--call", "pictures_api:create_app"]