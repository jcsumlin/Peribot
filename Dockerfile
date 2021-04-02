FROM python:3.6.13-slim
RUN mkdir -p /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get install -y ffmpeg youtube-dl python3-opencv git


COPY . /app
CMD ["python", "./main.py"]
