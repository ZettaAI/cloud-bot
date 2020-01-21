FROM python:3
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./requirements.txt
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    && apt-get -y install git iproute2 \
    procps lsb-release \
    curl apt-transport-https \
    build-essential libboost-dev \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
COPY . ./
CMD ["supervisord", "-c", "supervisord.conf"]