FROM ubuntu:latest

RUN apt-get update && apt-get install -y git gcc python3-dev ca-certificates tesseract-ocr curl gnupg lsb-release && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https:/download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN apt-get update -y
RUN apt-get install -y docker.io
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

WORKDIR /
COPY ./ ./
WORKDIR /

RUN pip install -r api/requirements.txt --no-cache-dir

CMD ["make", "run"]
# Run with sudo docker run -p 443:443 --privileged=true -v /var/run/docker.sock:/var/run/docker.sock