FROM golang:1.19-alpine
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN go mod tidy
WORKDIR /app/cmd
ENV PRODUCTION=1
RUN go build -o main main.go
#CMD ./main