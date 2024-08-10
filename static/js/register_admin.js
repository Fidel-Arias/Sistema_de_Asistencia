const buttonSiguiente = document.querySelector('.submit-btn'),
              buttonAnterior = document.querySelector('.back-btn'),
              formularioAdmin = document.getElementById('formulario-admin')
              formularioCongreso = document.getElementById('formulario'),
              containerRegister = document.querySelector('.container'),
              containerRegisterCongreso = document.querySelector('.container-congreso'),
              messageAlert = document.querySelector('.alert-error'),
              messageAlertCongreso = document.querySelector('.alert-error-congreso'),
              messageSuccessOrFailed = document.querySelector('.message'),
              title = document.querySelector('.title');

document.addEventListener('DOMContentLoaded', () => {
    const nombresAdmin = document.getElementById('nombreInput'),
            apellidosAdmin = document.getElementById('apellidoInput'),
            correoAdmin = document.getElementById('correoInput'),
            contrasenaAdmin = document.getElementById('contrasenaInput'),
            nombreCongreso = document.getElementById('nombreCongreso'),
            asistencia = document.getElementById('asistencias'),
            fechaInicioCongreso = document.getElementById('inicioCongreso'),
            csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value,
            fechaFinCongreso = document.getElementById('finCongreso');

    buttonSiguiente.addEventListener('click', function() {
        
        if (nombresAdmin.value && apellidosAdmin.value && correoAdmin.value && contrasenaAdmin.value) {
            if (!validarDominiosDeCorreo(correoAdmin.value)) {
                mostrarAlerta(messageAlert, 'Ingresa un correo válido');
            } else {
                containerRegister.classList.add('hide-izquierda');
                containerRegisterCongreso.classList.remove('hide-derecha');
            }
        } else {
            mostrarAlerta(messageAlert, 'Ingrese todos los campos');
        }
    });

    buttonAnterior.addEventListener('click', function() {
        containerRegisterCongreso.classList.add('hide-derecha');
        containerRegister.classList.remove('hide-izquierda');
    });

    formulario.addEventListener('submit', function(event){
        event.preventDefault();
        if (nombreCongreso.value && asistencia.value && fechaInicioCongreso.value && fechaFinCongreso.value) {
            datosFormulario = {
                nombresAdmin: nombresAdmin.value,
                apellidosAdmin: apellidosAdmin.value,
                correoAdmin: correoAdmin.value,
                contrasenaAdmin: contrasenaAdmin.value,
                nombreCongreso: nombreCongreso.value,
                asistencia: asistencia.value,
                fechaInicioCongreso: fechaInicioCongreso.value,
                fechaFinCongreso: fechaFinCongreso.value
            }

            enviarDatosFormulario(messageSuccessOrFailed, csrftoken, datosFormulario);
            containerRegisterCongreso.classList.add('hide-derecha');
            containerRegister.classList.remove('hide-izquierda');
            
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
    const prefixEmail = ['@ucsm.edu.pe', '@gmail.com', '@hotmail.com'];
    
    //Verificar si el correo incluye alguno de los dominios validos
    return prefixEmail.some(dominio => correoAdmin.includes(dominio));
}

function enviarDatosFormulario(messageSuccessOrFailed, csrftoken, datosFormulario) {
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
            messageSuccessOrFailed.textContent = 'Se ha enviado un correo al área administrativa';
            messageSuccessOrFailed.classList.remove('alert-failed');
            messageSuccessOrFailed.classList.add('alert-success');
            messageSuccessOrFailed.classList.remove('top');
            messageSuccessOrFailed.classList.add('bottom');
            setTimeout(() => {
                messageSuccessOrFailed.classList.remove('bottom');
                messageSuccessOrFailed.classList.add('top');
            }, 2000);
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
        formularioCongreso.reset();
        formularioAdmin.reset();
     })
}