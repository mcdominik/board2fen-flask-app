# syntax=docker/dockerfile:1
# start by pulling the python image
FROM python:3.9-slim-buster
ADD . /chess-flask
WORKDIR /chess-flask


# RUN pip install board_to_fen flask flask-wtf flask-uploaded

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
# WORKDIR /app

# RUN apt-get update && apt-get install -y python3-opencv
# RUN pip install opencv-python
# RUN apt-get update && apt-get install -y --no-install-recommends \
#         libgl1 \
#         libglib2.0-0
# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /app


# configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

CMD ["python", "app.py" ]
