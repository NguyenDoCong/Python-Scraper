FROM ubuntu:22.04

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
# COPY . .

# install dependencies
RUN apt-get -y update
RUN apt install -y python3-pip
# RUN pip install --upgrade pip
# RUN pip3 install playwright
# RUN pip3 install playwright==1.51.0
RUN pip3 install -r requirements.txt
RUN python3 -m playwright install
RUN python3 -m playwright install-deps 
RUN apt install -y ffmpeg

# EXPOSE 5000

# CMD ["python3", "./run.py"]
