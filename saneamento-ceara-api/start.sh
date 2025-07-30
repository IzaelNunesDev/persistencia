#!/bin/bash

# Script de inicialização para produção
set -e

echo "🚀 Iniciando API de Saneamento do Ceará..."

# Verificar se as variáveis de ambiente estão configuradas
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL não configurada, usando configuração local"
fi

# Configurar porta
export PORT=${PORT:-8000}
echo "🌐 Usando porta: $PORT"

# Executar migrações do banco de dados
echo "📊 Executando migrações do banco de dados..."
alembic upgrade head

# Iniciar a aplicação com uvicorn diretamente
echo "🌐 Iniciando servidor na porta $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT 