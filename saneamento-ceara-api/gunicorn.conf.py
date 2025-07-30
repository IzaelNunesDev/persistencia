# Configuração do Gunicorn para produção
import multiprocessing
import os

# Obter porta do ambiente ou usar 8000 como padrão
PORT = int(os.getenv("PORT", 8000))

# Configurações básicas
bind = f"0.0.0.0:{PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "saneamento-ceara-api"

# Preload app
preload_app = True

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190 