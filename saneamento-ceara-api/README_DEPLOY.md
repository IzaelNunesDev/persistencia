# Deploy da API de Saneamento do Ceará - Cloud Render

## 📋 Pré-requisitos

- Conta no [Cloud Render](https://render.com)
- Repositório Git com o código da API
- Dados do banco PostgreSQL

## 🚀 Deploy no Cloud Render

### 1. Preparação do Repositório

Certifique-se de que os seguintes arquivos estão no repositório:

```
saneamento-ceara-api/
├── app/
├── alembic/
├── requirements.txt
├── render.yaml
├── Dockerfile
├── gunicorn.conf.py
├── start.sh
├── Procfile
├── runtime.txt
└── .dockerignore
```

### 2. Configuração no Cloud Render

#### Opção A: Deploy via render.yaml (Recomendado)

1. Acesse o [Cloud Render Dashboard](https://dashboard.render.com)
2. Clique em "New" → "Blueprint"
3. Conecte seu repositório Git
4. O Cloud Render detectará automaticamente o arquivo `render.yaml`
5. Clique em "Apply" para criar o serviço e banco de dados

#### Opção B: Deploy Manual

1. **Criar Banco de Dados PostgreSQL:**
   - New → PostgreSQL
   - Nome: `saneamento-ceara-db`
   - Plano: Free
   - Clique em "Create Database"

2. **Criar Web Service:**
   - New → Web Service
   - Conecte seu repositório Git
   - Nome: `saneamento-ceara-api`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `./start.sh`

3. **Configurar Variáveis de Ambiente:**
   ```
   DATABASE_URL = [URL do banco criado]
   ENVIRONMENT = production
   LOG_LEVEL = INFO
   PORT = 8000
   ```

### 3. Configurações de Ambiente

#### Variáveis de Ambiente Necessárias

| Variável | Descrição | Valor |
|----------|-----------|-------|
| `DATABASE_URL` | URL de conexão com PostgreSQL | Automático (Render) |
| `ENVIRONMENT` | Ambiente de execução | `production` |
| `LOG_LEVEL` | Nível de logging | `INFO` |
| `PORT` | Porta da aplicação | `8000` |

#### Configurações Opcionais

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `PYTHON_VERSION` | Versão do Python | `3.10.0` |

### 4. Migração do Banco de Dados

O script `start.sh` executa automaticamente as migrações do Alembic. Se precisar executar manualmente:

```bash
# Acesse o shell do serviço no Render
alembic upgrade head
```

### 5. Carregamento de Dados

Após o deploy, você pode carregar os dados usando os scripts disponíveis:

```bash
# Executar scripts de carregamento
python scripts/load_data.py
```

## 🔧 Configurações de Produção

### Gunicorn

A aplicação usa Gunicorn como servidor WSGI com as seguintes configurações:

- **Workers**: `CPU_COUNT * 2 + 1`
- **Worker Class**: `uvicorn.workers.UvicornWorker`
- **Timeout**: 30 segundos
- **Max Requests**: 1000 por worker

### Banco de Dados

- **Pool Size**: 10 conexões
- **Max Overflow**: 20 conexões
- **Pool Recycle**: 300 segundos
- **Pool Pre Ping**: Habilitado

### CORS

Em produção, apenas os seguintes domínios são permitidos:
- `https://saneamento-ceara-api.onrender.com`
- `https://*.onrender.com`

## 📊 Monitoramento

### Logs

Os logs estão disponíveis no dashboard do Render:
- **Access Logs**: Requisições HTTP
- **Error Logs**: Erros da aplicação
- **Build Logs**: Logs do processo de build

### Health Check

Endpoint para verificar a saúde da aplicação:
```
GET /health
```

### Métricas

- **Response Time**: Tempo de resposta das requisições
- **Error Rate**: Taxa de erros
- **Memory Usage**: Uso de memória
- **CPU Usage**: Uso de CPU

## 🔒 Segurança

### Configurações Implementadas

- Usuário não-root no Docker
- CORS configurado para produção
- Timeouts configurados
- Limites de requisição
- Pool de conexões otimizado

### Recomendações Adicionais

1. **Rate Limiting**: Implementar rate limiting para APIs públicas
2. **Authentication**: Adicionar autenticação se necessário
3. **HTTPS**: Render fornece HTTPS automaticamente
4. **Backup**: Configurar backup automático do banco

## 🚨 Troubleshooting

### Problemas Comuns

1. **Build Fails**
   - Verificar `requirements.txt`
   - Verificar versão do Python
   - Verificar dependências do sistema

2. **Database Connection**
   - Verificar `DATABASE_URL`
   - Verificar se o banco está ativo
   - Verificar configurações de pool

3. **Application Crashes**
   - Verificar logs de erro
   - Verificar configurações do Gunicorn
   - Verificar variáveis de ambiente

### Comandos Úteis

```bash
# Verificar status do serviço
curl https://saneamento-ceara-api.onrender.com/health

# Verificar logs
# (via dashboard do Render)

# Executar migrações manualmente
alembic upgrade head

# Verificar conectividade do banco
python -c "from app.database import engine; print(engine.execute('SELECT 1').scalar())"
```

## 📞 Suporte

Para problemas específicos do Cloud Render:
- [Documentação Render](https://render.com/docs)
- [Suporte Render](https://render.com/support)

Para problemas da aplicação:
- Verificar logs no dashboard
- Consultar documentação da API
- Verificar configurações de ambiente 