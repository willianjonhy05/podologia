document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const response = await fetch('/api/token/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                alert('Login realizado com sucesso!');
                window.location.href = '/dashboard/';
            } else {
                alert('Erro no login! Verifique suas credenciais.');
            }
        });
    }

    // Função para carregar relatórios (Exemplo)
    async function loadRelatorios() {
        const token = localStorage.getItem('access');
        const response = await fetch('/api/relatorios/', {
            headers: { 'Authorization': 'Bearer ' + token }
        });

        if (response.ok) {
            const data = await response.json();
            const relatoriosList = document.getElementById('relatorios-list');
            relatoriosList.innerHTML = data.map(relatorio => `<p>${relatorio.data}: ${relatorio.progresso}% - ${relatorio.recomendacoes}</p>`).join('');
        } else {
            console.error('Erro ao carregar relatórios.');
        }
    }

    // Chama a função loadRelatorios ao carregar a página de relatórios
    if (document.getElementById('relatorios-list')) {
        loadRelatorios();
    }
});
