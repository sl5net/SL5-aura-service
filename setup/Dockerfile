# Dockerfile
# Use a specific Ubuntu version for reproducibility
FROM ubuntu:24.04

# Set a non-interactive frontend for apt-get to prevent it from asking questions
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# --- 1. System Dependencies ---
# Install all system dependencies in a single layer to optimize caching.
# NOTE: We are NOT installing xdotool or inotify-tools, as their functionality
# is incompatible with a standard Docker container.
RUN apt-get update && apt-get install -y \
    openjdk-21-jre-headless \
    wget \
    unzip \
    portaudio19-dev \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# --- 2. Python Requirements ---
# Copy only the requirements file first to leverage Docker's build cache.
# If this file doesn't change, this layer won't be re-run.
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# --- 3. Copy Application Code ---
# Copy the rest of the application code into the container
COPY . .

# --- 4. External Tools and Models ---
# This RUN command encapsulates all the download and setup logic.
RUN echo "--> Downloading external tools and models (if missing)..." && \
    \
    # LanguageTool
    LT_VERSION="6.6" && \
    if [ ! -d "LanguageTool-${LT_VERSION}" ]; then \
      echo "    -> Downloading LanguageTool v${LT_VERSION}..." && \
      wget https://languagetool.org/download/LanguageTool-${LT_VERSION}.zip -O languagetool.zip && \
      unzip -q languagetool.zip && \
      rm languagetool.zip; \
    fi && \
    \
    # Vosk Models
    mkdir -p models && \
    if [ ! -d "models/vosk-model-en-us-0.22" ]; then \
      echo "    -> Downloading English Vosk model..." && \
      wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip -O models/en.zip && \
      unzip -q models/en.zip -d models/ && \
      rm models/en.zip; \
    fi && \
    if [ ! -d "models/vosk-model-de-0.21" ]; then \
      echo "    -> Downloading German Vosk model..." && \
      wget https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip -O models/de.zip && \
      unzip -q models/de.zip -d models/ && \
      rm models/de.zip; \
    fi && \
    \
    # --- 5. Project Configuration ---
    echo "--> Creating Python package markers (__init__.py)..." && \
    touch config/__init__.py && \
    touch config/languagetool_server/__init__.py

# --- 6. Final Setup ---
# Expose the port used by the LanguageTool server
EXPOSE 8082

# Define the command to run when the container starts.
# Note: We must override the environment variable check in the Python script.
CMD ["/bin/bash", "-c", "export DICTATION_SERVICE_STARTED_CORRECTLY=true && python3 dictation_service.py"]
