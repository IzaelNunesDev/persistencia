#!/bin/bash

# Script de inicialização para produção
set -e

echo "🚀 Iniciando API de Saneamento do Ceará..."

# Verificar se as variáveis de ambiente estão configuradas
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL não configurada, usando configuração local"
fi

# Executar migrações do banco de dados
echo "📊 Executando migrações do banco de dados..."
alembic upgrade head

# Iniciar a aplicação
echo "🌐 Iniciando servidor..."
exec gunicorn app.main:app -c gunicorn.conf.py 