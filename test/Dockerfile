FROM ubuntu:latest
RUN mkdir -p /test
RUN apt-get update && apt-get install netcat -y
COPY . .
CMD netcat -4 server 12345 < test_message.txt