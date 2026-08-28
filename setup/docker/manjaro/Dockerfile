# Use Manjaro Linux Base as stable rolling base
FROM manjarolinux/base:latest

# Initialize pacman keys and install minimum system dependencies for Aura type_watcher and dotool
RUN pacman-key --init && \
    pacman-key --populate archlinux manjaro && \
    pacman -Syu --noconfirm --needed \
    python \
    python-pip \
    git \
    inotify-tools \
    base-devel \
    go \
    sudo \
    scdoc \
    libxkbcommon && \
    pacman -Scc --noconfirm

# Build dotool from source
RUN for i in 1 2 3; do \
        git clone https://git.sr.ht/~geb/dotool /tmp/dotool && break || sleep 10; \
    done && \
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

# Initialize configuration and Python virtual environment
RUN cp -f config/settings_local.py_Example.txt config/settings_local.py || true && \
    if [ -f ./setup/manjaro_arch_setup.sh ]; then bash ./setup/manjaro_arch_setup.sh || true; fi

# Default to bash shell
CMD ["bash"]
