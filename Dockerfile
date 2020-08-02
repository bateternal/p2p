FROM python:3.7.5-slim
COPY . /p2p
WORKDIR /p2p
#CMD python3 main.py