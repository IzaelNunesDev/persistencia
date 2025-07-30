// JavaScript principal para o Dashboard de Saneamento do Ceará

// Configurações globais
const API_BASE_URL = '/api/v1';

// Utilitários
const utils = {
    // Formatar números
    formatNumber: (num) => {
        if (num === null || num === undefined) return 'N/A';
        return new Intl.NumberFormat('pt-BR').format(num);
    },
    
    // Formatar percentuais
    formatPercent: (num) => {
        if (num === null || num === undefined) return 'N/A';
        return `${num.toFixed(1)}%`;
    },
    
    // Formatar valores monetários
    formatCurrency: (num) => {
        if (num === null || num === undefined) return 'N/A';
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(num);
    },
    
    // Mostrar loading
    showLoading: (elementId) => {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '<div class="loading">Carregando...</div>';
        }
    },
    
    // Mostrar erro
    showError: (elementId, message) => {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `<div class="error">Erro: ${message}</div>`;
        }
    },
    
    // Fazer requisição à API
    async fetchAPI: async (endpoint, options = {}) => {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição à API:', error);
            throw error;
        }
    }
};

// Gerenciador de gráficos
const ChartManager = {
    // Criar gráfico de linha
    createLineChart: (canvasId, data, options = {}) => {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return null;
        
        return new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: options.title || ''
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: options.maxY || 100
                    }
                },
                ...options
            }
        });
    },
    
    // Criar gráfico de barras
    createBarChart: (canvasId, data, options = {}) => {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return null;
        
        return new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: options.title || ''
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                ...options
            }
        });
    },
    
    // Criar gráfico de pizza
    createPieChart: (canvasId, data, options = {}) => {
        const ctx = document.getElementById(canvasId)?.getContext('2d');
        if (!ctx) return null;
        
        return new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: options.title || ''
                    }
                },
                ...options
            }
        });
    }
};

// Gerenciador de dados
const DataManager = {
    // Carregar indicadores principais
    async loadIndicadoresPrincipais() {
        try {
            const data = await utils.fetchAPI('/analises/indicadores-principais');
            return data;
        } catch (error) {
            console.error('Erro ao carregar indicadores principais:', error);
            throw error;
        }
    },
    
    // Carregar evolução temporal
    async loadEvolucaoTemporal() {
        try {
            const data = await utils.fetchAPI('/analises/evolucao-temporal');
            return data;
        } catch (error) {
            console.error('Erro ao carregar evolução temporal:', error);
            throw error;
        }
    },
    
    // Carregar ranking
    async loadRanking(indicador, limit = 10, municipioId = null) {
        try {
            let endpoint = `/analises/ranking?indicador=${indicador}&limit=${limit}`;
            if (municipioId) {
                endpoint += `&municipio_id=${municipioId}`;
            }
            const data = await utils.fetchAPI(endpoint);
            return data;
        } catch (error) {
            console.error('Erro ao carregar ranking:', error);
            throw error;
        }
    },
    
    // Carregar dados de município
    async loadMunicipioData(municipioId) {
        try {
            const data = await utils.fetchAPI(`/municipios/${municipioId}`);
            return data;
        } catch (error) {
            console.error('Erro ao carregar dados do município:', error);
            throw error;
        }
    },
    
    // Carregar evolução de município
    async loadMunicipioEvolucao(municipioId) {
        try {
            const data = await utils.fetchAPI(`/municipios/${municipioId}/evolucao`);
            return data;
        } catch (error) {
            console.error('Erro ao carregar evolução do município:', error);
            throw error;
        }
    }
};

// Gerenciador de interface
const UIManager = {
    // Atualizar indicadores principais
    updateIndicadoresPrincipais(data) {
        const container = document.getElementById('indicadores-principais');
        if (!container) return;
        
        container.innerHTML = `
            <div class="grid">
                <div class="indicador-card">
                    <div class="indicador-label">Atendimento Água</div>
                    <div class="indicador-valor agua">${utils.formatPercent(data.media_atendimento_agua || 0)}</div>
                </div>
                <div class="indicador-card">
                    <div class="indicador-label">Coleta Esgoto</div>
                    <div class="indicador-valor esgoto">${utils.formatPercent(data.media_coleta_esgoto || 0)}</div>
                </div>
                <div class="indicador-card">
                    <div class="indicador-label">Tratamento Esgoto</div>
                    <div class="indicador-valor esgoto">${utils.formatPercent(data.media_tratamento_esgoto || 0)}</div>
                </div>
                <div class="indicador-card">
                    <div class="indicador-label">Perda Faturamento</div>
                    <div class="indicador-valor">${utils.formatPercent(data.media_perda_faturamento || 0)}</div>
                </div>
            </div>
        `;
    },
    
    // Atualizar ranking
    updateRanking(containerId, rankingData) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = rankingData.ranking.map((item, index) => `
            <div class="ranking-item">
                <strong>${index + 1}.</strong> ${item.municipio.nome} - ${utils.formatPercent(item.valor)}
            </div>
        `).join('');
    },
    
    // Criar gráfico de evolução
    createEvolucaoChart(canvasId, data) {
        const chartData = {
            labels: data.anos,
            datasets: [
                {
                    label: 'Atendimento Água (%)',
                    data: data.atendimento_agua,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1
                },
                {
                    label: 'Coleta Esgoto (%)',
                    data: data.coleta_esgoto,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.1
                },
                {
                    label: 'Tratamento Esgoto (%)',
                    data: data.tratamento_esgoto,
                    borderColor: 'rgb(255, 205, 86)',
                    backgroundColor: 'rgba(255, 205, 86, 0.1)',
                    tension: 0.1
                }
            ]
        };
        
        return ChartManager.createLineChart(canvasId, chartData, {
            title: 'Evolução dos Indicadores',
            maxY: 100
        });
    }
};

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard de Saneamento do Ceará inicializado');
    
    // Adicionar animações de fade-in
    document.querySelectorAll('article').forEach(article => {
        article.classList.add('fade-in');
    });
    
    // Configurar tooltips e outras funcionalidades
    setupEventListeners();
});

// Configurar event listeners
function setupEventListeners() {
    // Busca de municípios
    const searchInput = document.getElementById('municipio-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleMunicipioSearch, 300));
    }
    
    // Filtros de ano
    const anoFilter = document.getElementById('ano-filter');
    if (anoFilter) {
        anoFilter.addEventListener('change', handleAnoFilterChange);
    }
}

// Função de debounce para otimizar buscas
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Handlers de eventos
async function handleMunicipioSearch(event) {
    const searchTerm = event.target.value;
    if (searchTerm.length < 3) return;
    
    try {
        const municipios = await utils.fetchAPI(`/municipios/search?q=${encodeURIComponent(searchTerm)}`);
        updateMunicipioSearchResults(municipios);
    } catch (error) {
        console.error('Erro na busca de municípios:', error);
    }
}

function handleAnoFilterChange(event) {
    const ano = event.target.value;
    // Recarregar dados com o ano selecionado
    if (window.currentPage === 'dashboard') {
        carregarDadosDashboard(ano);
    }
}

// Função para atualizar resultados da busca
function updateMunicipioSearchResults(municipios) {
    const resultsContainer = document.getElementById('municipio-search-results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = municipios.map(municipio => `
        <div class="search-result-item" onclick="selectMunicipio('${municipio.id_municipio}')">
            <strong>${municipio.nome}</strong>
            <small>${municipio.id_municipio}</small>
        </div>
    `).join('');
}

// Função para selecionar município
function selectMunicipio(municipioId) {
    window.location.href = `/dashboard/municipios/${municipioId}`;
}

// Exportar funções para uso global
window.utils = utils;
window.ChartManager = ChartManager;
window.DataManager = DataManager;
window.UIManager = UIManager; 