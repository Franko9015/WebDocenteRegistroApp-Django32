function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Buscar la cookie que comienza con el nombre proporcionado
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Esta función se llama cuando se termina una clase
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
                    window.location.href = listaasistenciaURL;
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
    Swal.fire({
        title: '¿Estás seguro de cerrar la sesión?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('cerrarSesion').classList.add('disabled');
            document.getElementById('botonTexto').style.display = 'none';
            document.getElementById('animacionCarga').style.display = 'inline-block';

            // Simula una pausa de 2 segundos (2000 milisegundos)
            setTimeout(function () {
                // Redirige al usuario a la página de inicio de sesión
                window.location.href = loginURL; // Reemplaza loginURL con la URL de inicio de sesión
            }, 2000);
        }
    });
}

// Esta función está relacionada con el inicio de la clase
function iniciarClase(button) {
    var cursoID = $(button).data("curso-id");
    var crearClaseURL = $(button).data("crearclase-url");

    Swal.fire({
        title: '¿Estás seguro de iniciar la clase?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, iniciar',
        cancelButtonText: 'Cancelar',
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar un mensaje de carga mientras se inicia la clase
            Swal.fire({
                title: 'Iniciando la clase...',
                icon: 'info',
                showConfirmButton: false,
                allowOutsideClick: false,
            });

            // Obtén el token CSRF
            var csrftoken = getCookie('csrftoken');

            // Datos para crear la clase
            const data = {
                curso_id: cursoID,
                csrfmiddlewaretoken: csrftoken,
            };

            // Realiza una solicitud POST para crear la clase
            $.ajax({
                type: 'POST',
                url: crearClaseURL,
                data: data,
                success: function (response) {
                    if (response.redirect && response.redirect !== '') {
                        // Redirige a la página de asistencia con la ID de la clase creada
                        window.location.href = response.redirect;
                    }
                },
                error: function (error) {
                    Swal.fire('Error', 'No se pudo iniciar la clase', 'error');
                },
            });
        }
    });
}





// Esta función está relacionada con el envío de comunicados
function enviarComunicado() {
    // Obtén los valores de los campos
    const tipoComunicado = document.getElementById('tipoComunicado').value;
    const tituloComunicado = document.getElementById('tituloComunicado').value;
    const mensaje = document.getElementById('mensaje').value;

    if (mensaje.trim() === '' || tituloComunicado.trim() === '') {
        Swal.fire('Error', 'Todos los campos deben estar completos', 'error');
        return;
    }

    // Mostrar una alerta de confirmación
    Swal.fire({
        title: '¿Estás seguro de enviar el comunicado?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, enviar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar un mensaje de carga mientras se envía
            Swal.fire({
                title: 'Enviando comunicado...',
                icon: 'info',
                showConfirmButton: false,
                allowOutsideClick: false
            });

            // Datos del comunicado
            const data = {
                tipoComunicado: tipoComunicado,
                titulo: tituloComunicado,
                contenido: mensaje,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            };

            // Realiza la solicitud POST solo si el usuario confirma
            $.ajax({
                type: 'POST',
                url: comunicadoURL,
                data: data,
                success: function () {
                    Swal.fire('Comunicado enviado con éxito', '', 'success').then(() => {
                        // Redirige al dashboard después de enviar
                        window.location.href = dashboardURL;
                    });
                },
                error: function () {
                    Swal.fire('Error', 'No se pudo enviar el comunicado', 'error');
                }
            });
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
                    // Redirige a la página de notas
                    window.location.href = notasURL;
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
                    // Redirige a la página de inicio
                    window.location.href = dashboardURL;
                });
            }, 3000); // Simula una carga de 3 segundos
        }
    });
}

function confirmarAnotacion() {
    const anotacionesURL = document.querySelector('[data-anotaciones-url]').getAttribute('data-anotaciones-url');
    const listacursosURL = document.querySelector('[data-listacursos-url]').getAttribute('data-listacursos-url');

    // Obtén los valores de los campos
    const tipoAnotacion = document.getElementById('tipoAnotacion').value;
    const comentario = document.getElementById('comentario').value;

    // Verifica si algún campo está vacío
    if (tipoAnotacion === '' || comentario === '') {
        Swal.fire('Error', 'Todos los campos deben estar llenos', 'error');
    } else {
        // Realiza una solicitud POST para guardar la anotación
        $.ajax({
            type: 'POST',
            url: anotacionesURL,
            data: $('#Formulario').serialize(),
            success: function () {
                Swal.fire('Anotación generada con éxito', '', 'success').then(() => {
                    // Redirecciona a la página de cursos después de guardar
                    window.location.href = listacursosURL;
                });
            },
            error: function () {
                Swal.fire('Error', 'No se pudo guardar la anotación', 'error');
            }
        });
    }
}


function generarCodigosQR(studentIds) {
    var qrCodesContainer = document.getElementById('qr-codes');
    qrCodesContainer.innerHTML = ''; // Limpia cualquier código QR existente

    if (studentIds.length === 0) {
        return; // No hay estudiantes para generar códigos QR
    }

    studentIds.forEach(function(studentId) {
        // Crea un nuevo objeto QRious para cada estudiante
        var qr = new QRious({
            value: studentId,
            size: 150 // Ajusta el tamaño del código QR según tus necesidades
        });

        // Crea un elemento de imagen para el código QR y agrégalo al contenedor
        var qrImage = document.createElement('img');
        qrImage.src = qr.toDataURL('image/png');
        qrCodesContainer.appendChild(qrImage);
    });
    
}




// Asigna las URL a variables JavaScript
var loginURL = "{% url 'LOG' %}";
var dashboardURL = "{% url 'IND' %}";
var asistenciaURL = "{% url 'ASIS' %}";
var listaalumnosURL = "{% url 'LALU' curso.id %}"; 
var listaasistenciaURL = "{% url 'LASIS' %}";
var listacursosURL = "{% url 'LCUR' %}";
var modificarnotasURL = "{% url 'MODN' curso.id %}";
var notasURL = "{% url 'NON' %}";
var situacionalumnosURL = "{% url 'SISA' %}";
var anotacionesURL = "/anotaciones/" + alumno.id + "/";
var comunicadoURL = "{% url 'comunicado' %}";
var historialcomunicadosURL = "{% url 'HSC' %}";
var historialanotacionesURL = "{% url 'HAN' %}";
var perfilURL = "{% url 'PF' %}";
var crearClaseURL = "{% url 'crear_clase' %}";
