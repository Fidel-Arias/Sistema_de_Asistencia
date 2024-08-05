document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('cam-video');
    const canvas = document.getElementById('cam-canvas');
    const context = canvas.getContext('2d');
    const btnStart = document.getElementById('btn-cam');
    const btnStop = document.getElementById('btn-stop-cam');
    const audio = document.getElementById('audioScaner');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const bloqueSelect = document.querySelector('[name=bloque]');
    
    let stream;
    let animationFrameId;

    btnStart.addEventListener('click', async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            video.srcObject = stream;
            video.play();
            video.classList.add('hidden');  // Mostrar el video
            canvas.classList.remove('hidden');  // Ocultar el canvas
            scanQRCode();
        }
    });

    btnStop.addEventListener('click', () => {
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            video.srcObject = null;
            video.classList.add('hidden');  // Ocultar el video
            canvas.classList.add('hidden');  // Ocultar el canvas
        }

        // Cancelar la animación
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    });

    function scanQRCode() {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            canvas.hidden = false;
            canvas.height = video.videoHeight;
            canvas.width = video.videoWidth;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height, {
                inversionAttempts: "dontInvert",
            });

            if (code) {
                audio.play();
                //Envio al metodo
                if (bloqueSelect.value) {
                    fetch('/colaborador/interfaz_colaborador/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                        },
                        body: JSON.stringify({
                            qr_code: code.data,
                            bloque: bloqueSelect.value
                        })
                    })
                    .then(response => response.json());
                } else {
                    alert('Debe seleccionar un bloque');
                }
                
                btnStop.click(); // Stop the camera after detecting a QR code
            }
        }

        animationFrameId = requestAnimationFrame(scanQRCode);
    }


});