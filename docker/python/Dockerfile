FROM python:3.7-stretch

RUN apt-get update && apt-get install -y strace curl sudo netcat && \
        pip install --upgrade pip setuptools wheel virtualenv && \
        echo "source /code/vendor/bin/activate" >> /root/.bashrc