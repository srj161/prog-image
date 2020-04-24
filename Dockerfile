FROM python:3
ADD . /srv/prog-image
RUN pip install -r /srv/prog-image/requirements.txt
