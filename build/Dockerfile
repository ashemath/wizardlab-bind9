FROM debian:bookworm-slim
RUN apt update && apt upgrade -y
RUN apt install -y procps python3 git host bind9 bind9-utils procps
RUN mkdir /bind
EXPOSE 53
RUN chown bind:root /etc/bind/rndc.key

