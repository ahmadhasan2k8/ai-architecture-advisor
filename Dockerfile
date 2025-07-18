# Simple single-stage build for Jupyter notebook
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies from requirements files
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

# Create non-root user
RUN useradd -m -s /bin/bash jupyter && \
    mkdir -p /home/jupyter/work

# Copy project files
COPY --chown=jupyter:jupyter . /home/jupyter/work/

# Set working directory
WORKDIR /home/jupyter/work

# Switch to non-root user
USER jupyter

# Expose Jupyter port
EXPOSE 8888

# Configure Jupyter for classic notebook interface
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = False" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.token = 'design-patterns-2025'" >> ~/.jupyter/jupyter_notebook_config.py

# Set default command to use classic notebook interface
CMD ["sh", "-c", "echo '\n🚀 Starting Jupyter Notebook...\n' && echo '📝 Access your notebook at: http://127.0.0.1:8888/tree?token=design-patterns-2025\n' && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser"]