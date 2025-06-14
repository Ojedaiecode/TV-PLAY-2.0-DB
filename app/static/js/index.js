// Arquivo preparado para futuras implementações 

// 🧠 Função: Alternar exibição da senha (Mostrar/Esconder)
// Este script controla o clique no ícone de olho para exibir ou ocultar a senha
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.querySelector('.toggle-password');
    const senhaInput = document.getElementById('senhaInput');
    const eyeOpen = document.querySelector('.eye-open');
    const eyeClosed = document.querySelector('.eye-closed');

    togglePassword.addEventListener('click', function() {
        // Alterna o tipo do input entre password e text
        const type = senhaInput.getAttribute('type') === 'password' ? 'text' : 'password';
        senhaInput.setAttribute('type', type);

        // Alterna a visibilidade dos ícones
        eyeOpen.classList.toggle('hidden');
        eyeClosed.classList.toggle('hidden');
    });
}); 