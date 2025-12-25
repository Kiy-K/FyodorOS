FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

# Install System Dependencies for Remastering and Building
RUN apt-get update && apt-get install -y \
    squashfs-tools \
    xorriso \
    p7zip-full \
    mtools \
    dosfstools \
    wget \
    curl \
    git \
    sudo \
    sed \
    file \
    build-essential \
    libwebkit2gtk-4.0-dev \
    libssl-dev \
    libgtk-3-dev \
    appstream \
    python3-pip \
    python3-venv \
    python3-dev \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install Rust (Stable)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Python Build Tools
RUN pip install nuitka

WORKDIR /build
