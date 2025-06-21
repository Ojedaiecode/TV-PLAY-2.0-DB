/**
 * Controle do Painel Administrativo
 * QG - Quartel General
 */

document.addEventListener('DOMContentLoaded', () => {
    // Elementos principais
    const mainContent = document.querySelector('.main-content');
    const menuItems = document.querySelectorAll('.sidebar-menu li');
    const headerTitle = document.querySelector('.header-left h1');

    // Mapeamento de rotas para arquivos HTML
    const routes = {
        'Add-user-gratis': '/templates/add-user-gratis.html',
        // Outras rotas serão adicionadas aqui
    };

    // Função para carregar conteúdo dinamicamente
    async function loadContent(route) {
        try {
            const response = await fetch(route);
            const html = await response.text();
            
            // Atualiza o conteúdo principal
            mainContent.innerHTML = html;
            
            // Atualiza o título do header
            const title = route.split('/').pop().split('.')[0];
            headerTitle.textContent = title.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        } catch (error) {
            console.error('Erro ao carregar conteúdo:', error);
        }
    }

    // Adiciona listeners aos itens do menu
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove classe active de todos os itens
            menuItems.forEach(i => i.classList.remove('active'));
            
            // Adiciona classe active ao item clicado
            item.classList.add('active');

            // Obtém o texto do item (nome da rota)
            const routeName = item.querySelector('span').textContent;
            
            // Se existe uma rota mapeada, carrega o conteúdo
            if (routes[routeName]) {
                loadContent(routes[routeName]);
            }
        });
    });
}); 