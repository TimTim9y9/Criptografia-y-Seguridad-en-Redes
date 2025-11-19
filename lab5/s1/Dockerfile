FROM ubuntu:16.04

# Apuntar a old-releases (16.04 ya está fuera de soporte)
RUN sed -i 's|archive.ubuntu.com|old-releases.ubuntu.com|g' /etc/apt/sources.list && \
    sed -i 's|security.ubuntu.com|old-releases.ubuntu.com|g' /etc/apt/sources.list

# Instalar SSH cliente y servidor
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        openssh-client \
        openssh-server \
        iputils-ping \
        bash && \
    rm -rf /var/lib/apt/lists/*

# Crear directorios de SSH
RUN mkdir -p /var/run/sshd

CMD ["tail", "-f", "/dev/null"]
