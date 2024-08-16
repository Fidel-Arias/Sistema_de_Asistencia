document.addEventListener('DOMContentLoaded', () => {
    const nombresAdmin = document.getElementById('nombreInput'),
        apellidosAdmin = document.getElementById('apellidoInput'),
        correoAdmin = document.getElementById('correoInput'),
        contrasenaAdmin = document.getElementById('contrasenaInput'),
        nombreCongreso = document.getElementById('nombreCongreso'),
        asistencia = document.getElementById('asistencias'),
        fechaInicioCongreso = document.getElementById('inicioCongreso'),
        fechaFinCongreso = document.getElementById('finCongreso'),
        csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
        messageSuccessOrFailed = document.querySelector('.message.alert-failed'),
        messageAlert = document.querySelector('.alert-error'),
        messageAlertCongreso = document.querySelector('.alert-error-congreso'),
        formularioAdmin = document.getElementById('formulario-admin'),
        formularioCongreso = document.getElementById('formulario'),
        containerRegister = document.querySelector('.container'),
        containerRegisterCongreso = document.querySelector('.container-congreso'),
        buttonSiguiente = document.querySelector('.submit-btn'),
        buttonAnterior = document.querySelector('.back-btn');

    // Botón siguiente para mover al segundo formulario
    buttonSiguiente.addEventListener('click', function () {
        if (nombresAdmin.value && apellidosAdmin.value && correoAdmin.value && contrasenaAdmin.value) {
            if (!validarDominiosDeCorreo(correoAdmin.value)) {
                mostrarAlerta(messageAlert, 'Ingresa un correo válido');
            } else {
                // Si todo está bien, pasa al siguiente formulario (no toca las animaciones aquí)
                containerRegister.classList.add('hide-izquierda');
                containerRegisterCongreso.classList.remove('hide-derecha');
            }
        } else {
            mostrarAlerta(messageAlert, 'Ingrese todos los campos');
        }
    });

    // Botón anterior para regresar al primer formulario
    buttonAnterior.addEventListener('click', function () {
        containerRegisterCongreso.classList.add('hide-derecha');
        containerRegister.classList.remove('hide-izquierda');
    });

    // Manejo de la acción del formulario de congreso
    formularioCongreso.addEventListener('submit', function (event) {
        event.preventDefault();
        if (nombreCongreso.value && asistencia.value && fechaInicioCongreso.value && fechaFinCongreso.value) {
            // Crear el objeto datosFormulario con los datos del formulario
            const datosFormulario = {
                nombresAdmin: nombresAdmin.value,
                apellidosAdmin: apellidosAdmin.value,
                correoAdmin: correoAdmin.value,
                contrasenaAdmin: contrasenaAdmin.value,
                nombreCongreso: nombreCongreso.value,
                asistencia: asistencia.value,
                fechaInicioCongreso: fechaInicioCongreso.value,
                fechaFinCongreso: fechaFinCongreso.value
            };

            containerRegisterCongreso.classList.remove('hide-derecha');
            containerRegister.classList.add('hide-izquierda');

            // Deshabilitar el botón de registro para evitar múltiples envíos
            event.target.querySelector('button[type="submit"]').disabled = true;

            // Enviar los datos del formulario
            enviarDatosFormulario(messageSuccessOrFailed, csrftoken, datosFormulario, formularioAdmin, formularioCongreso);
        } else {
            mostrarAlerta(messageAlertCongreso, 'Ingrese todos los campos');
        }
    });
});

function mostrarAlerta(messageAlert, message) {
    messageAlert.textContent = message;
    messageAlert.classList.add('mostrar');
    setTimeout(() => {
        messageAlert.classList.remove('mostrar');
    }, 3000);
}

function validarDominiosDeCorreo(correoAdmin) {
    const prefixEmail = ['@ucsm.edu.pe'];
    return prefixEmail.some(dominio => correoAdmin.includes(dominio));
}

// Función para enviar los datos del formulario al backend
function enviarDatosFormulario(messageSuccessOrFailed, csrftoken, datosFormulario, formularioAdmin, formularioCongreso) {
    document.querySelector('.container-congreso').classList.remove('hide-derecha');
    document.querySelector('.container').classList.add('hide-izquierda');
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            formulario: datosFormulario
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Si Django retorna un success, ejecutar la animación
            messageSuccessOrFailed.textContent = 'Se ha enviado un correo al área administrativa';
            messageSuccessOrFailed.classList.remove('alert-failed');
            messageSuccessOrFailed.classList.add('alert-success');
            messageSuccessOrFailed.classList.remove('top');
            messageSuccessOrFailed.classList.add('bottom');
            setTimeout(() => {
                messageSuccessOrFailed.classList.remove('bottom');
                messageSuccessOrFailed.classList.add('top');
            }, 2000);

            // Aquí es donde puedes agregar la animación de vuelta al primer formulario
            containerRegisterCongreso.classList.add('hide-derecha');
            containerRegister.classList.remove('hide-izquierda');

            // Limpiar los formularios después de enviar los datos
            formularioCongreso.reset();
            formularioAdmin.reset();
        }
    })
    .catch(error => {
        messageSuccessOrFailed.textContent = 'Error al recibir los datos del formulario';
        messageSuccessOrFailed.classList.remove('alert-success');
        messageSuccessOrFailed.classList.add('alert-failed');
        messageSuccessOrFailed.classList.remove('top');
        messageSuccessOrFailed.classList.add('bottom');
        setTimeout(() => {
            messageSuccessOrFailed.classList.remove('bottom');
            messageSuccessOrFailed.classList.add('top');
        }, 2000);

        // También puedes manejar aquí la animación de error
        containerRegisterCongreso.classList.add('hide-derecha');
        containerRegister.classList.remove('hide-izquierda');

        formularioCongreso.reset();
        formularioAdmin.reset();
    })
    .finally(() => {
        // Habilitar el botón nuevamente
        document.querySelector('button[type="submit"]').disabled = false;
    });
    
}
