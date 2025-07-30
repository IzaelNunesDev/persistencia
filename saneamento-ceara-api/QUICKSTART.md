# 🚀 Guia Rápido - Dashboard de Saneamento do Ceará

## ⚡ Como Rodar em 5 Passos

### 1. Clone e entre na pasta
```bash
git clone <url-do-repositorio>
cd saneamento-ceara-api
```

### 2. Suba os containers
```bash
docker-compose up --build -d
```

### 3. Execute as migrações
```bash
docker-compose exec api alembic upgrade head
```

### 4. Carregue os dados
```bash
docker-compose exec api python scripts/load_data.py
```

### 5. Acesse o dashboard
- **Dashboard:** http://localhost:8000/dashboard
- **API Docs:** http://localhost:8000/docs

## 🎯 URLs Principais

- **Dashboard Principal:** http://localhost:8000/dashboard
- **Lista de Municípios:** http://localhost:8000/dashboard/municipios
- **Análises:** http://localhost:8000/dashboard/analises
- **API Documentation:** http://localhost:8000/docs

## 🛠️ Comandos Úteis

```bash
# Verificar se está rodando
docker-compose ps

# Ver logs
docker-compose logs api

# Parar tudo
docker-compose down

# Reconstruir
docker-compose up --build -d
```

## 📊 O que você verá

- **2.257 registros** de dados de saneamento
- **184 municípios** do Ceará
- **Rankings** dos melhores municípios
- **Gráficos interativos** com Chart.js
- **Análises comparativas** entre municípios

## ✅ Status

O projeto está **100% funcional** e pronto para uso!

---

**🎉 Pronto! Seu dashboard de saneamento está rodando!** 