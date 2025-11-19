FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        openssh-client \
        iputils-ping \
        bash && \
    rm -rf /var/lib/apt/lists/*

CMD ["tail", "-f", "/dev/null"]
