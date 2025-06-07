FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    libegl1 \
    libopengl0 \
    libxcb-cursor0 \
    libfreetype6 \
    libfreetype6-dev \
    xz-utils \
    xdg-utils \
    && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["bash"]