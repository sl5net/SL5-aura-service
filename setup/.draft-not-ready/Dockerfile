# Use Ubuntu LTS as stable base
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

# Prepare Bootstrap Pointer (The Master Key)
RUN mkdir -p /tmp/sl5_aura && \
    chmod -R 777 /tmp/sl5_aura && \
    echo "/app" > /tmp/sl5_aura/sl5net_aura_project_root

WORKDIR /app

# Copy the repository files and set permissions
COPY --chown=runner:runner . /app
RUN rm -rf /app/.venv && chown -R runner:runner /app

USER runner

# Run diagnostics to verify user identity, directory ownership, and write permissions
RUN echo "Force build update 3" && whoami && ls -la /app

# Test if runner can manually create a python venv here in a clean directory
RUN python3 -m venv /app/.venv_test_manual && rm -rf /app/.venv_test_manual

# Initialize configuration and Python virtual environment
RUN cp -f config/settings_local.py_Example.txt config/settings_local.py || true && \
    if [ -f ./setup/ubuntu_setup.sh ]; then bash ./setup/ubuntu_setup.sh; fi

# Default to bash shell
CMD ["bash"]