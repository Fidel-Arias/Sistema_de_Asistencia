// Ocultar el mensaje después de 3 segundos
setTimeout(function() {
    var message = document.getElementById('message');
    var mainContent = document.getElementById('main');
    if (message) {
        message.style.display = 'none';
        mainContent.style.gap = '2em';
    }
}, 3000); // 3000 milisegundos = 3 segundos