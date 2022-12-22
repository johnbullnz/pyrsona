## Development environment

FROM python:3.9

# Set SHELL environment variable:
ENV SHELL=bash

# Copy custom .bashrc to set colorised terminal:
COPY .bashrc /root/.bashrc

# Stop Python from generating .pyc files in the container and turn off buffering:
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# Update system packages:
RUN apt-get update && apt-get upgrade -y

# Copy onCreate.sh (triggered in devcontainer.json) and update permissions:
COPY onCreate.sh /root/onCreate.sh
RUN chmod 777 /root/onCreate.sh

# Update pip and setuptools:
RUN python3 -m pip install -U pip setuptools wheel

CMD [ "bash" ]