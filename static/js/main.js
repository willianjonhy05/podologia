// Aguarda o carregamento completo do DOM antes de executar o código
document.addEventListener('DOMContentLoaded', function () {
    // Recupera o token de autenticação JWT do armazenamento local
    const token = localStorage.getItem('access');

    /**
     * Função assíncrona para carregar os relatórios de progresso do usuário.
     * Faz uma requisição à API para obter dados de progresso e exibe os resultados
     * na página, dentro do elemento com o ID 'relatorios-list'.
     */
    async function loadRelatorios() {
        const response = await fetch('/api/relatorios/', {
            headers: { 'Authorization': `Bearer ${token}` } // Inclui o token de autenticação
        });
        const data = await response.json(); // Extrai os dados JSON da resposta
        const relatoriosList = document.getElementById('relatorios-list');

        // Mapeia os dados recebidos para HTML e os insere no elemento
        relatoriosList.innerHTML = data.map(item =>
            `<div class="list-group-item">
                <h5>Data: ${item.data}</h5>
                <p>Progresso: ${item.progresso}%</p>
                <p>Recomendações: ${item.recomendacoes}</p>
            </div>`
        ).join(''); // join('') remove as vírgulas entre os itens do array
    }

    /**
     * Função assíncrona para carregar os feedbacks fornecidos pelos responsáveis.
     * Faz uma requisição à API para obter os feedbacks e exibe os resultados
     * dentro do elemento com o ID 'feedbacks-list'.
     */
    async function loadFeedbacks() {
        const response = await fetch('/api/feedbacks/', {
            headers: { 'Authorization': `Bearer ${token}` } // Inclui o token de autenticação
        });
        const data = await response.json(); // Extrai os dados JSON da resposta
        const feedbacksList = document.getElementById('feedbacks-list');

        // Mapeia os dados recebidos para HTML e os insere no elemento
        feedbacksList.innerHTML = data.map(item =>
            `<div class="list-group-item">
                <h5>Data: ${item.data}</h5>
                <p>${item.conteudo}</p>
            </div>`
        ).join('');
    }

    /**
     * Função assíncrona para carregar a lista de agendamentos do usuário.
     * Faz uma requisição à API para obter dados de agendamentos e exibe os resultados
     * dentro do elemento com o ID 'agendamentos-list'.
     */
    async function loadAgendamentos() {
        const response = await fetch('/api/agendamentos/', {
            headers: { 'Authorization': `Bearer ${token}` } // Inclui o token de autenticação
        });
        const data = await response.json(); // Extrai os dados JSON da resposta
        const agendamentosList = document.getElementById('agendamentos-list');

        // Mapeia os dados recebidos para HTML e os insere no elemento
        agendamentosList.innerHTML = data.map(item =>
            `<div class="list-group-item">
                <h5>Data do Agendamento: ${item.data_agendamento}</h5>
                <p>Notificação em: ${item.data_notificacao}</p>
            </div>`
        ).join('');
    }

    // Verifica a presença dos elementos no DOM e carrega os dados específicos para cada página
    if (document.getElementById('relatorios-list')) loadRelatorios();
    if (document.getElementById('feedbacks-list')) loadFeedbacks();
    if (document.getElementById('agendamentos-list')) loadAgendamentos();
});
