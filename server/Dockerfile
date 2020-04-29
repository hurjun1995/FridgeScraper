FROM python:3.7

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements to leverage Docker cache
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

# run server
ENTRYPOINT [ "python" ]
CMD ["app.py"]