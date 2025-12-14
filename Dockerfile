# Stage 1: Builder
FROM python:3.10-slim AS builder

# Install system dependencies for Nuitka compilation
RUN apt-get update && apt-get install -y \
    gcc \
    ccache \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the entire repository
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Step A: Compile C++ Extensions (CRITICAL: Must be before Nuitka)
RUN python setup_extensions.py build_ext --inplace

# Step B: Build the kernel (Nuitka)
# This outputs to /app/src-tauri/bin/fyodor-kernel
RUN python scripts/build_kernel.py

# Stage 2: Runtime
FROM python:3.10-slim AS runtime

# Create a non-root user for security
RUN useradd -m -s /bin/bash fyodor

WORKDIR /app

# Create the .fyodor config directory with correct permissions
RUN mkdir -p /home/fyodor/.fyodor && \
    chown -R fyodor:fyodor /home/fyodor

# Copy the compiled binary (FIXED PATH)
# removed "gui/" prefix
COPY --from=builder --chown=fyodor:fyodor /app/src-tauri/bin/fyodor-kernel /app/fyodor-kernel

# Switch to non-root user
USER fyodor

# Expose port
EXPOSE 8000

# Entrypoint configuration
# Uses JSON syntax to handle SIGTERM correctly
ENTRYPOINT ["/app/fyodor-kernel", "serve", "--host", "0.0.0.0", "--port", "8000"]
