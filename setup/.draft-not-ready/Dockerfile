# Use Ubuntu 22.04 LTS as stable base
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install absolute minimum system dependencies for Aura type_watcher and dotool
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    inotify-tools \
    build-essential \
    golang-go \
    sudo \
    scdoc \
    libxkbcommon-dev \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Build dotool from source
RUN git clone https://git.sr.ht/~geb/dotool /tmp/dotool && \
    cd /tmp/dotool && \
    ./build.sh && \
    ./build.sh install && \
    rm -rf /tmp/dotool

# Create input group and non-root runner user with sudo rights
RUN groupadd -f input && \
    useradd -m -s /bin/bash runner && \
    usermod -aG input runner && \
    echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Prepare Bootstrap Pointer (The Master Key) for Aura
RUN mkdir -p /tmp/sl5_aura && \
    chmod -R 777 /tmp/sl5_aura && \
    echo "/app" > /tmp/sl5_aura/sl5net_aura_project_root

WORKDIR /app

# Copy repository files and set permissions
COPY --chown=runner:runner . /app

USER runner

# Ensure local example config is copied and run official Ubuntu setup
RUN cp -f config/settings_local.py_Example.txt config/settings_local.py || true && \
    if [ -f ./setup/ubuntu_setup.sh ]; then bash ./setup/ubuntu_setup.sh; fi

ENV DISPLAY=:99
CMD ["bash"]