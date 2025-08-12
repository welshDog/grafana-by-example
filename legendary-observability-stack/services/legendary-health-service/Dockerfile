# 🐳💎⚡ LEGENDARY HEALTH SERVICE DOCKERFILE ⚡💎🐳
# Optimized Python container for health monitoring

FROM python:3.11-slim

# 🎯 ADHD-OPTIMIZED LABELS
LABEL maintainer="Legendary Empire <legendary@hyperfocuszone.com>"
LABEL description="Advanced health monitoring service with BROski$ rewards"
LABEL version="1.0.0"
LABEL adhd_optimized="true"

# 📁 WORKING DIRECTORY SETUP
WORKDIR /app

# 🔧 SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 📦 PYTHON DEPENDENCIES
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📁 CREATE NECESSARY DIRECTORIES
RUN mkdir -p /app/logs /app/static /app/templates

# 📄 COPY APPLICATION FILES
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/

# 👤 CREATE NON-ROOT USER (security best practice)
RUN groupadd -r legendary && useradd -r -g legendary legendary
RUN chown -R legendary:legendary /app
USER legendary

# 🌐 EXPOSE PORT
EXPOSE 8080

# 🏥 HEALTH CHECK
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 🚀 STARTUP COMMAND
CMD ["python", "app.py"]
