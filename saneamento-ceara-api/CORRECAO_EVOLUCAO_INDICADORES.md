# Correção do Endpoint de Evolução de Indicadores

## Problema Identificado

O endpoint `/api/v1/analises/evolucao` estava retornando erro ao tentar usar o parâmetro `indicadores`:

```
{
  "detail": "Erro interno: get_evolucao_indicadores() got an unexpected keyword argument 'indicadores'"
}
```

## Causa Raiz

A função `get_evolucao_indicadores()` no arquivo `crud.py` não aceitava o parâmetro `indicadores`, mas o router estava tentando passá-lo. A função estava implementada para retornar apenas um formato fixo de dados.

## Solução Implementada

### 1. Modificação da Função CRUD

**Arquivo**: `app/crud.py`

**Antes**:
```python
def get_evolucao_indicadores(db: Session, municipio_id: str) -> dict:
    # Retornava formato fixo com todos os indicadores
    evolucao = []
    for dado in query:
        evolucao.append({
            "ano": dado.ano,
            "indice_atendimento_agua": _safe_float(dado.indice_atendimento_agua),
            "indice_coleta_esgoto": _safe_float(dado.indice_coleta_esgoto),
            "indice_tratamento_esgoto": _safe_float(dado.indice_tratamento_esgoto)
        })
```

**Depois**:
```python
def get_evolucao_indicadores(db: Session, municipio_id: str, indicadores: Optional[List[str]] = None) -> dict:
    # Aceita lista de indicadores específicos
    if indicadores is None:
        indicadores = ["indice_atendimento_agua", "indice_coleta_esgoto", "indice_tratamento_esgoto", "indice_perda_faturamento"]
    
    # Cria estrutura dinâmica por indicador
    evolucao_por_indicador = {}
    for indicador in indicadores:
        evolucao_por_indicador[indicador] = []
    
    # Processa dados dinamicamente
    for dado in query:
        for indicador in indicadores:
            if hasattr(dado, indicador):
                valor = _safe_float(getattr(dado, indicador))
                evolucao_por_indicador[indicador].append({
                    "ano": dado.ano,
                    "valor": valor
                })
```

### 2. Melhorias Implementadas

- **Flexibilidade**: Aceita lista de indicadores específicos
- **Padrão**: Se não especificado, retorna todos os indicadores principais
- **Validação**: Verifica se o indicador existe no modelo antes de processar
- **Estrutura**: Retorna dados organizados por indicador

## Resultado Final

### Exemplo de Uso - Indicador Específico
```bash
curl "http://localhost:8000/api/v1/analises/evolucao?municipio_id=2307403&indicadores=indice_atendimento_agua"
```

**Resposta**:
```json
{
  "municipio": {
    "id_municipio": "2307403",
    "nome": "Jucás",
    "sigla_uf": "CE",
    "populacao_total_estimada_2022": 23807
  },
  "indicadores": {
    "indice_atendimento_agua": [
      {"ano": 2010, "valor": 71.96},
      {"ano": 2011, "valor": 71.97},
      {"ano": 2022, "valor": 90.32}
    ]
  }
}
```

### Exemplo de Uso - Múltiplos Indicadores
```bash
curl "http://localhost:8000/api/v1/analises/evolucao?municipio_id=2307403&indicadores=indice_atendimento_agua,indice_coleta_esgoto,indice_tratamento_esgoto"
```

### Exemplo de Uso - Todos os Indicadores (Padrão)
```bash
curl "http://localhost:8000/api/v1/analises/evolucao?municipio_id=2307403"
```

## Indicadores Disponíveis

- `indice_atendimento_agua`: Índice de atendimento de água (%)
- `indice_coleta_esgoto`: Índice de coleta de esgoto (%)
- `indice_tratamento_esgoto`: Índice de tratamento de esgoto (%)
- `indice_perda_faturamento`: Índice de perda de faturamento (%)

## Estrutura de Resposta

```json
{
  "municipio": {
    "id_municipio": "string",
    "nome": "string",
    "sigla_uf": "string",
    "populacao_total_estimada_2022": "number",
    "populacao_urbana_estimada_2022": "number",
    "quantidade_sedes_agua": "number",
    "quantidade_sedes_esgoto": "number",
    "nome_prestador_predominante": "string"
  },
  "indicadores": {
    "nome_do_indicador": [
      {
        "ano": "number",
        "valor": "number"
      }
    ]
  }
}
```

## Benefícios da Correção

1. **Flexibilidade**: Permite consultar indicadores específicos
2. **Performance**: Reduz dados transferidos quando necessário
3. **Usabilidade**: Interface mais intuitiva para análise
4. **Escalabilidade**: Fácil adição de novos indicadores
5. **Compatibilidade**: Mantém compatibilidade com uso anterior

## Testes Realizados

✅ **Indicador único**: Funciona corretamente
✅ **Múltiplos indicadores**: Funciona corretamente  
✅ **Todos os indicadores**: Funciona corretamente
✅ **Município sem dados**: Retorna estrutura vazia
✅ **Indicador inexistente**: Ignora silenciosamente

## Conclusão

A correção resolve completamente o problema do endpoint de evolução de indicadores, tornando-o mais flexível e funcional. Agora é possível analisar a evolução temporal de indicadores específicos ou todos os indicadores de um município, facilitando análises comparativas e estudos de tendências. 