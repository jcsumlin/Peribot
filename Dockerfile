FROM python:alpine3.6
COPY . /app
WORKDIR /app
RUN apk update
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
RUN apk add --no-cache g++ freetype-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install -r requirements.txt
CMD python ./main.py