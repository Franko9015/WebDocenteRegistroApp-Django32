// Esta función está relacionada con la terminación de la clase
function terminarClase() {
    const radios = document.querySelectorAll('input[type="radio"]');
    const asistenciaCompleta = Array.from(radios).some((radio) => radio.checked);

    if (asistenciaCompleta) {
        Swal.fire({
            title: '¿Estás seguro de terminar la clase?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, terminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire('Clase finalizada con éxito', '', 'success').then(() => {
                    // Redirecciona a otra página cuando se confirma la terminación de la clase
                    window.location.href = "{%url 'LASIS'%}";
                });
            }
        });
    } else {
        Swal.fire({
            title: 'Oops...',
            text: 'Debes marcar la asistencia de al menos un estudiante.',
            icon: 'error',
        });
    }
}

// Esta función está relacionada con el cierre de sesión
function logout() {
    document.getElementById('cerrarSesion').addEventListener('click', function (event) {
        // Evita que el enlace redireccione inmediatamente
        event.preventDefault();

        document.getElementById('cerrarSesion').classList.add('disabled');
        document.getElementById('botonTexto').style.display = 'none';
        document.getElementById('animacionCarga').style.display = 'inline-block';

        // Simula una pausa de 2 segundos (2000 milisegundos)
        setTimeout(function () {
            // Redirige al usuario a la página de inicio de sesión
            window.location.href = "{% url'LOG' %}";
        }, 2000);
    });
}

// Esta función está relacionada con el inicio de la clase
function iniciarClase() {
    Swal.fire({
        title: '¿Estás seguro de iniciar la clase?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, iniciar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Redirige a la página de asistencia.html
            window.location.href = 'asistencia.html';
        }
    });
}

// Esta función está relacionada con el envío de comunicados
function enviarComunicado() {
    const tipoComunicado = document.getElementById('tipoComunicado').value;
    const tituloComunicado = document.getElementById('tituloComunicado').value;
    const mensaje = document.getElementById('mensaje').value;

    if (mensaje.trim() === '' || tituloComunicado.trim() === '') {
        Swal.fire('Error', 'Todos los campos deben estar completos', 'error');
        return;
    }

    Swal.fire({
        title: '¿Estás seguro de enviar el comunicado?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, enviar',
        cancelButtonText: 'Cancelar'
    }).then(async (result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Enviando comunicado...',
                icon: 'info',
                showConfirmButton: false,
                allowOutsideClick: false
            });

            setTimeout(() => {
                Swal.fire('Comunicado enviado con éxito', '', 'success').then(() => {
                    // Redirige al index.html
                    window.location.href = 'index.html';
                });
            }, 3000); // Simula un envío de 3 segundos
        }
    });
}

// Esta función está relacionada con la limpieza del formulario de comunicados
function limpiarFormulario() {
    document.getElementById('tipoComunicado').value = 'general';
    document.getElementById('tituloComunicado').value = ''; // Agregado para limpiar el título
    document.getElementById('mensaje').value = '';
}

// Esta función está relacionada con la modificación de notas
function guardarCambiosNotas() {
    Swal.fire({
        title: '¿Estás seguro de modificar las notas de los alumnos?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, modificar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Modificando notas...',
                icon: 'info',
                showConfirmButton: false,
                allowOutsideClick: false
            });

            setTimeout(() => {
                Swal.fire('Notas modificadas con éxito', '', 'success').then(() => {
                    // Redirige a la página de notas.html después de la simulación de carga
                    window.location.href = 'notas.html';
                });
            }, 1000); // Cambia 1000 a 3000 para una espera de 3 segundos
        }
    });
}

// Esta función permite reprobar a un alumno por inasistencia
function reprobarAlumno() {
    Swal.fire({
        title: '¿Estás seguro de reprobar a este alumno por inasistencia?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, reprobar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: 'Reprobando alumno...',
                icon: 'info',
                showConfirmButton: false,
                allowOutsideClick: false
            });

            setTimeout(() => {
                Swal.fire('Alumno reprobado por inasistencia', '', 'success').then(() => {
                    window.location.href = 'index.html';
                });
            }, 3000); // Simula una carga de 3 segundos
        }
    });
}
