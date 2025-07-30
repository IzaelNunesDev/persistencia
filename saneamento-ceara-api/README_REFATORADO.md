# API de Análise de Saneamento do Ceará - Versão Refatorada

## Visão Geral

Esta é uma API RESTful completa para análise de dados de saneamento básico no Ceará, baseada no Sistema Nacional de Informações sobre Saneamento (SNIS). A API foi refatorada para ser puramente RESTful, separando completamente a camada de apresentação web da API.

## Principais Mudanças na Refatoração

### ✅ Fase 1: Separação da Camada Web
- **Removido**: Dashboard HTML, templates e arquivos estáticos
- **Removido**: Router do dashboard (`app/routers/dashboard.py`)
- **Transformado**: API puramente RESTful sem dependências web

### ✅ Fase 2: Melhoria dos Schemas Pydantic
- **Adicionado**: Validações rigorosas com `Field` constraints
- **Criado**: Schemas de listagem (`*List`) e detalhes (`*Detail`)
- **Adicionado**: Schemas de atualização (`*Update`) para operações PATCH/PUT
- **Implementado**: Validadores customizados (ex: sigla UF apenas CE)

### ✅ Fase 3: Filtros Avançados
- **Municípios**: Filtros por população (min/max), ordenação customizada
- **Indicadores**: Filtros por ano (range), prestador, município
- **Prestadores**: Filtros por nome, sigla, natureza jurídica
- **Recursos Hídricos**: Filtros por volume, indicador
- **Financeiro**: Filtros por receita, indicador

### ✅ Fase 4: Endpoints para as 5 Entidades
Cada entidade agora possui endpoints CRUD completos:

1. **Municípios** (`/api/v1/municipios`)
2. **Prestadores de Serviço** (`/api/v1/prestadores`)
3. **Indicadores de Desempenho** (`/api/v1/indicadores`)
4. **Recursos Hídricos** (`/api/v1/recursos-hidricos`)
5. **Financeiro** (`/api/v1/financeiro`)

## Estrutura da API

### Endpoints Principais

#### 1. Municípios (`/api/v1/municipios`)
```
GET    /api/v1/municipios/                    # Listar municípios com filtros
GET    /api/v1/municipios/{id_municipio}      # Obter município específico
POST   /api/v1/municipios/                    # Criar novo município
PUT    /api/v1/municipios/{id_municipio}      # Atualizar município
DELETE /api/v1/municipios/{id_municipio}      # Remover município
GET    /api/v1/municipios/{id}/indicadores    # Indicadores do município
```

**Filtros disponíveis:**
- `nome`: Busca por nome do município
- `populacao_min`: População mínima
- `populacao_max`: População máxima
- `order_by`: Campo para ordenação
- `order_direction`: Direção da ordenação

#### 2. Prestadores de Serviço (`/api/v1/prestadores`)
```
GET    /api/v1/prestadores/                   # Listar prestadores com filtros
GET    /api/v1/prestadores/{id}               # Obter prestador específico
GET    /api/v1/prestadores/sigla/{sigla}      # Obter por sigla
POST   /api/v1/prestadores/                   # Criar novo prestador
PUT    /api/v1/prestadores/{id}               # Atualizar prestador
DELETE /api/v1/prestadores/{id}               # Remover prestador
GET    /api/v1/prestadores/{id}/indicadores   # Indicadores do prestador
```

**Filtros disponíveis:**
- `nome`: Busca por nome do prestador
- `sigla`: Busca por sigla
- `natureza_juridica`: Filtro por natureza jurídica
- `order_by`: Campo para ordenação
- `order_direction`: Direção da ordenação

#### 3. Indicadores de Desempenho (`/api/v1/indicadores`)
```
GET    /api/v1/indicadores/                   # Listar indicadores com filtros
GET    /api/v1/indicadores/{id}               # Obter indicador completo
POST   /api/v1/indicadores/                   # Criar novo indicador
PUT    /api/v1/indicadores/{id}               # Atualizar indicador
DELETE /api/v1/indicadores/{id}               # Remover indicador
GET    /api/v1/indicadores/{id}/recursos-hidricos  # Recursos hídricos do indicador
GET    /api/v1/indicadores/{id}/financeiro    # Dados financeiros do indicador
```

**Filtros disponíveis:**
- `ano_inicio`: Ano inicial do período
- `ano_fim`: Ano final do período
- `municipio_id`: ID do município
- `prestador_id`: ID do prestador
- `order_by`: Campo para ordenação
- `order_direction`: Direção da ordenação

#### 4. Recursos Hídricos (`/api/v1/recursos-hidricos`)
```
GET    /api/v1/recursos-hidricos/             # Listar recursos hídricos
GET    /api/v1/recursos-hidricos/{id}         # Obter registro específico
GET    /api/v1/recursos-hidricos/indicador/{indicador_id}  # Por indicador
POST   /api/v1/recursos-hidricos/             # Criar novo registro
PUT    /api/v1/recursos-hidricos/{id}         # Atualizar registro
DELETE /api/v1/recursos-hidricos/{id}         # Remover registro
GET    /api/v1/recursos-hidricos/estatisticas/volume-agua  # Estatísticas
```

**Filtros disponíveis:**
- `indicador_id`: ID do indicador
- `volume_min`: Volume mínimo de água produzida
- `volume_max`: Volume máximo de água produzida
- `order_by`: Campo para ordenação
- `order_direction`: Direção da ordenação

#### 5. Financeiro (`/api/v1/financeiro`)
```
GET    /api/v1/financeiro/                    # Listar dados financeiros
GET    /api/v1/financeiro/{id}                # Obter registro específico
GET    /api/v1/financeiro/indicador/{indicador_id}  # Por indicador
POST   /api/v1/financeiro/                    # Criar novo registro
PUT    /api/v1/financeiro/{id}                # Atualizar registro
DELETE /api/v1/financeiro/{id}                # Remover registro
GET    /api/v1/financeiro/estatisticas/receitas-despesas  # Estatísticas
GET    /api/v1/financeiro/sustentabilidade/{ano}  # Análise de sustentabilidade
```

**Filtros disponíveis:**
- `indicador_id`: ID do indicador
- `receita_min`: Receita mínima
- `receita_max`: Receita máxima
- `order_by`: Campo para ordenação
- `order_direction`: Direção da ordenação

### Endpoints de Análise (Mantidos)
```
GET    /api/v1/analises/ranking/{indicador}   # Ranking de municípios
GET    /api/v1/analises/evolucao/{municipio_id}  # Evolução temporal
GET    /api/v1/analises/comparativo/{ano}     # Comparativo entre municípios
GET    /api/v1/analises/sustentabilidade/{ano}  # Análise de sustentabilidade
GET    /api/v1/analises/recursos-hidricos/{ano}  # Análise de recursos hídricos
```

## Validações Implementadas

### Schemas com Validações Rigorosas
- **Municípios**: ID IBGE (7 dígitos), sigla UF apenas CE
- **Prestadores**: Sigla única, nome obrigatório
- **Indicadores**: Ano entre 1900-2100, índices entre 0-100%
- **Recursos Hídricos**: Volumes não negativos
- **Financeiro**: Valores não negativos

### Validações de Negócio
- Verificação de existência antes de criar registros duplicados
- Verificação de integridade referencial
- Validação de relacionamentos entre entidades

## Exemplos de Uso

### 1. Listar Municípios com Filtros
```bash
GET /api/v1/municipios/?populacao_min=50000&order_by=populacao_total_estimada_2022&order_direction=desc&limit=10
```

### 2. Buscar Indicadores por Período
```bash
GET /api/v1/indicadores/?ano_inicio=2020&ano_fim=2022&municipio_id=2304400
```

### 3. Análise de Sustentabilidade Financeira
```bash
GET /api/v1/financeiro/sustentabilidade/2022
```

### 4. Estatísticas de Recursos Hídricos
```bash
GET /api/v1/recursos-hidricos/estatisticas/volume-agua?ano=2022
```

## Instalação e Execução

### Pré-requisitos
- Python 3.8+
- PostgreSQL (recomendado) ou SQLite
- Dependências listadas em `requirements.txt`

### Configuração
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure as variáveis de ambiente (veja `env.example`)
4. Execute as migrações: `alembic upgrade head`
5. Inicie a API: `uvicorn app.main:app --reload`

### Documentação Interativa
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Melhorias Implementadas

### Performance
- Queries otimizadas com índices apropriados
- Eager loading para relacionamentos
- Paginação em todos os endpoints de listagem

### Segurança
- Validação rigorosa de entrada
- Sanitização de parâmetros de consulta
- Tratamento adequado de erros

### Usabilidade
- Documentação automática via OpenAPI
- Exemplos de uso na documentação
- Códigos de status HTTP apropriados
- Mensagens de erro descritivas

## Próximos Passos

1. **Testes**: Implementar testes unitários e de integração
2. **Cache**: Adicionar cache Redis para consultas frequentes
3. **Autenticação**: Implementar autenticação JWT
4. **Rate Limiting**: Adicionar limitação de taxa de requisições
5. **Monitoramento**: Implementar logs estruturados e métricas

## Contribuição

Para contribuir com o projeto:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Adicione testes
5. Submeta um pull request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 