# Dockerfile para API Gerador de Propostas Solar
# Porta: 3493

FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instalar dependências do sistema para matplotlib, reportlab e health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libffi-dev \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache de camadas)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para arquivos temporários
RUN mkdir -p /tmp/propostas && chmod 777 /tmp/propostas

# Expor porta
EXPOSE 3493

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3493/api/v1/health || exit 1

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3493"]
