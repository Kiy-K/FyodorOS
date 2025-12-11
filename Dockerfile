# FyodorOS - Production Container Image
# Multi-stage build for optimized image size

# ============================================================
# Stage 1: Builder - Compile extensions
# ============================================================
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    g++ \
    make \
    musl-dev \
    linux-headers \
    nasm \
    git

WORKDIR /build

# Copy source code
COPY . .

# Build C++ extensions (if setup_extensions.py exists)
RUN if [ -f setup_extensions.py ]; then \
        python setup_extensions.py build || echo "No extensions to build"; \
    fi

# Build Python package
RUN pip install --no-cache-dir build && \
    python -m build


# ============================================================
# Stage 2: Runtime - Minimal production image
# ============================================================
FROM python:3.11-alpine

LABEL maintainer="khoitruong071510@gmail.com"
LABEL version="0.6.0"
LABEL description="FyodorOS - The Experimental AI Microkernel"

# Install runtime dependencies
RUN apk add --no-cache \
    bash \
    curl \
    git \
    nasm \
    chromium \
    chromium-chromedriver \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    && rm -rf /var/cache/apk/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FYODOR_HOME=/root/.fyodor \
    FYODOR_CONFIG=/etc/fyodoros \
    FYODOR_INTERACTIVE=false \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PATH="/root/.local/bin:${PATH}"

# Create FyodorOS directory structure
RUN mkdir -p \
    ${FYODOR_HOME} \
    ${FYODOR_CONFIG} \
    /var/log/fyodoros \
    /tmp/fyodoros \
    /home/guest \
    /home/root

WORKDIR /fyodoros

# Copy built package from builder stage
COPY --from=builder /build/dist/*.whl /tmp/

# Install FyodorOS package
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -rf /tmp/*.whl

# Install Playwright browsers
RUN playwright install chromium --with-deps || \
    echo "Warning: Playwright browser installation failed"

# Create default configuration if needed
RUN echo "journal" > ${FYODOR_CONFIG}/services.conf

# Set up default user
RUN echo "guest:x:1000:1000:Guest User:/home/guest:/bin/sh" >> /etc/passwd && \
    echo "guest:!:19000:0:99999:7:::" >> /etc/shadow && \
    chown -R 1000:1000 /home/guest

# Create welcome message
RUN echo "Welcome to FyodorOS v0.6.0 - The Experimental AI Microkernel" > /etc/motd && \
    echo "Type 'fyodor help' for available commands" >> /etc/motd

# Expose ports (optional, for future services)
EXPOSE 8080 8443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Set entrypoint to OS init
ENTRYPOINT ["python", "-m", "fyodoros.os_init"]

# Default command (can be overridden)
CMD []
