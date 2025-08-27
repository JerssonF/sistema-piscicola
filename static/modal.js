// Funciones para manejo de modales

function showSuccessModal() {
    document.getElementById('modal-overlay').style.display = 'block';
    document.getElementById('success-modal').style.display = 'block';
}

function showErrorModal() {
    document.getElementById('modal-overlay').style.display = 'block';
    document.getElementById('error-modal').style.display = 'block';
}

function closeModal() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
    document.getElementById('modal-overlay').style.display = 'none';
}

function toggleMenu() {
    const menu = document.getElementById('menu');
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

// Cerrar modal al hacer clic en el overlay
document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) {
        overlay.addEventListener('click', closeModal);
    }
    
    // Cerrar modal con tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
});
