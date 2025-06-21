/**
 * Scripts para o formulário de Adicionar Usuário Grátis
 * QG - Quartel General
 */

document.addEventListener('DOMContentLoaded', () => {
    // Elementos do DOM
    const form = document.getElementById('addUserForm');
    const messageArea = document.getElementById('messageArea');
    const togglePassword = document.querySelector('.toggle-password');
    const senhaInput = document.getElementById('senha');
    const celularInput = document.getElementById('celular');

    // Função para mostrar mensagens
    function showMessage(message, type) {
        messageArea.textContent = message;
        messageArea.className = `message-area ${type}`;
        
        // Esconde a mensagem após 5 segundos
        setTimeout(() => {
            messageArea.className = 'message-area';
        }, 5000);
    }

    // Função para limpar o formulário
    function clearForm() {
        form.reset();
    }

    // Toggle de visibilidade da senha
    togglePassword.addEventListener('click', () => {
        const type = senhaInput.getAttribute('type') === 'password' ? 'text' : 'password';
        senhaInput.setAttribute('type', type);
        
        // Alterna o ícone
        togglePassword.setAttribute('data-lucide', type === 'password' ? 'eye' : 'eye-off');
        lucide.createIcons(); // Recria os ícones
    });

    // Máscara para o campo de celular
    celularInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
            value = value.replace(/(\d)(\d{4})$/, '$1-$2');
            e.target.value = value;
        }
    });

    // Handler do formulário
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        try {
            // Desabilita o botão durante o envio
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;

            // Coleta os dados do formulário
            const formData = {
                nome: form.nome.value.trim(),
                email: form.email.value.trim(),
                celular: form.celular.value.replace(/\D/g, ''), // Remove formatação
                senha: form.senha.value
            };

            // Envia os dados para a API
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                showMessage(data.message || 'Usuário cadastrado com sucesso!', 'success');
                clearForm();
            } else {
                throw new Error(data.message || 'Erro ao cadastrar usuário');
            }

        } catch (error) {
            console.error('Erro ao cadastrar:', error);
            showMessage(error.message || 'Erro ao cadastrar usuário. Tente novamente.', 'error');
        } finally {
            // Reabilita o botão
            submitButton.disabled = false;
        }
    });
}); 