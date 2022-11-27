FROM golang:1.19

RUN mkdir /app
COPY requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY checker_go/go.mod checker_go/go.sum ./
RUN go mod download && go mod verify

COPY . /app
WORKDIR /app

CMD gunicorn --workers 3 --bind 0.0.0.0:8000 standings.wsgi:application