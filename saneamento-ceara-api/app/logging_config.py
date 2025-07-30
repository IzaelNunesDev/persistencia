import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    """
    Configura o sistema de logging da aplicação
    """
    # Criar diretório de logs se não existir
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar formato dos logs
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remover handlers existentes para evitar duplicação
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # Handler para arquivo com rotação
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'api.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # Handler para erros
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)
    
    # Configurar loggers específicos
    loggers_to_configure = [
        'app',
        'sqlalchemy.engine',
        'uvicorn',
        'fastapi'
    ]
    
    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.propagate = True
    
    # Logger específico para SQLAlchemy (mais verboso)
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.WARNING)
    
    return root_logger

def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado para o módulo especificado
    """
    return logging.getLogger(name)

def log_request(request_id: str, method: str, url: str, status_code: int, duration: float):
    """
    Log específico para requisições HTTP
    """
    logger = get_logger('app.requests')
    level = logging.INFO if status_code < 400 else logging.WARNING
    logger.log(level, f"Request {request_id}: {method} {url} - {status_code} ({duration:.3f}s)")

def log_database_operation(operation: str, table: str, duration: float, success: bool):
    """
    Log específico para operações de banco de dados
    """
    logger = get_logger('app.database')
    level = logging.INFO if success else logging.ERROR
    status = "SUCCESS" if success else "ERROR"
    logger.log(level, f"DB {operation} on {table} - {status} ({duration:.3f}s)") 