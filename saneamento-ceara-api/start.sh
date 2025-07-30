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

# Verificar se o banco está vazio e carregar dados se necessário
echo "🔍 Verificando se o banco precisa de dados iniciais..."
python -c "
import sys
sys.path.append('.')
from app.database import SessionLocal
from app import models

db = SessionLocal()
try:
    # Verificar se há municípios
    municipio_count = db.query(models.Municipio).count()
    print(f'Municípios encontrados: {municipio_count}')
    
    if municipio_count == 0:
        print('Banco vazio detectado. Carregando dados iniciais...')
        import subprocess
        subprocess.run(['python', 'scripts/load_data.py'], check=True)
        subprocess.run(['python', 'scripts/create_prestadores.py'], check=True)
        subprocess.run(['python', 'scripts/enhance_municipios.py'], check=True)
        print('✅ Dados carregados com sucesso!')
    else:
        print('✅ Banco já possui dados.')
finally:
    db.close()
"

# Iniciar a aplicação com uvicorn diretamente
echo "🌐 Iniciando servidor na porta $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT 