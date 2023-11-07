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


function marcarPresente(radio) {
    var alumnoId = radio.dataset.alumnoId;
    var url = "/incrementar_asistencia/" + alumnoId + "/";

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            'alumno_id': alumnoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Asistencia incrementada con éxito");
        } else {
            console.log("Error al incrementar la asistencia");
        }
    });
}

function terminarClase(button) {
    const terminarClaseURL = $(button).data("terminarclase-url");
    const claseID = $(button).data("clase-id");
    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    const listaasistenciaURL = $(button).data("listaasistencia-url");

    // Obtén la asistencia seleccionada
    const radios = document.querySelectorAll('input[type="radio"]');
    const asistenciaData = [];

    radios.forEach((radio) => {
        if (radio.checked) {
            const studentID = radio.getAttribute("data-student-id");
            const asistencia = radio.value;
            asistenciaData.push({ studentID, asistencia });
        }
    });

    if (asistenciaData.length > 0) {
        Swal.fire({
            title: '¿Estás seguro de terminar la clase?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, terminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: terminarClaseURL,
                    data: {
                        clase_id: claseID,
                        csrfmiddlewaretoken: csrfToken,
                        asistencia_data: JSON.stringify(asistenciaData)
                    },
                    success: function (response) {
                        Swal.fire('Clase finalizada con éxito', '', 'success').then(() => {
                            // Redirige a la página de asistencia después de confirmar la terminación de la clase
                            window.location.href = listaasistenciaURL;
                        });
                    },
                    error: function () {
                        Swal.fire('Error', 'No se pudo terminar la clase', 'error');
                    }
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
                window.location.href = "/"; // Reemplaza loginURL con la URL de inicio de sesión
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





function enviarComunicado(button) {
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
                url: button.getAttribute('data-comunicados-url'),
                data: data,
                success: function () {
                    Swal.fire('Comunicado enviado con éxito', '', 'success').then(() => {
                        // Redirige al dashboard después de enviar
                        window.location.href = button.getAttribute('data-dashboard-url');
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
                    window.location.href = "/notas/";
                });
            }, 1000); // Cambia 1000 a 3000 para una espera de 3 segundos
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
                    window.location.href = "/listacursos/";
                });
            },
            error: function () {
                Swal.fire('Error', 'No se pudo guardar la anotación', 'error');
            }
        });
    }
}


function reprobarAlumno(button) {
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

            // Recupera el ID del alumno automáticamente desde el botón
            var alumnoId = button.getAttribute('data-alumno-id');

            // Recupera el token CSRF del formulario que rodea el botón
            var csrfToken = document.querySelector('form#reprobar-form-' + alumnoId + ' [name="csrfmiddlewaretoken"]').value;

            // Realiza una solicitud AJAX para marcar al alumno como reprobado
            $.ajax({
                type: 'POST',
                url: `/reprobar_alumno/${alumnoId}/`,
                data: { csrfmiddlewaretoken: csrfToken },
                success: function (response) {
                    Swal.fire('Alumno reprobado por inasistencia', '', 'success').then(() => {
                        // Redirige al dashboard después de reprobar al alumno
                        window.location.href = "/dashboard/";
                    });
                },
                error: function () {
                    Swal.fire('Error', 'No se pudo reprobar al alumno', 'error');
                }
            });
        }
    });
}


    

document.addEventListener('DOMContentLoaded', function () {
    var qrCodesContainer = document.getElementById('qr-codes');
    var codigoQR = document.getElementById('codigoQR');
    var qrDataArray = [];
    var generandoQR = false;

    function generarCodigoQR() {
        if (generandoQR) {
            return; // Evitar generar múltiples códigos al mismo tiempo
        }

        generandoQR = true;
        qrCodesContainer.innerHTML = ''; // Limpia cualquier código QR existente

        qrDataArray = [
            // Define tus datos para generar los códigos QR aquí
            "idcurso:1, asistencia:presente, fecha:FECHA_ACTUAL"
            // Otros datos aquí
        ];

        // Reemplaza 'FECHA_ACTUAL' con la fecha y hora actual en todos los elementos del array
        qrDataArray = qrDataArray.map(function (qrData) {
            return qrData.replace('FECHA_ACTUAL', obtenerFechaActual());
        });

        generarSiguienteQR();
    }

    function generarSiguienteQR() {
        if (qrDataArray.length === 0) {
            generandoQR = false;
            return; // No quedan datos para generar códigos QR
        }

        var qrData = qrDataArray.shift();

        // Crea un nuevo objeto QRious con el contenido actualizado
        var qr = new QRious({
            value: qrData,
            size: 700 // Ajusta el tamaño del código QR según tus necesidades
        });

        // Crea un elemento de imagen para el código QR y agrégalo al contenedor
        var qrImage = document.createElement('img');
        qrImage.src = qr.toDataURL('image/png');
        qrCodesContainer.appendChild(qrImage);

        // Muestra la sección de códigos QR
        codigoQR.classList.add('show');

        generandoQR = false;
    }

    // Agrega un evento de clic al botón para llamar a la función generarCodigoQR
    var generarQRButton = document.getElementById('generar-qr-button');
    generarQRButton.addEventListener('click', generarCodigoQR);

    // Función para obtener la fecha y hora actual en el formato deseado
    function obtenerFechaActual() {
        var fecha = new Date();
        var dia = fecha.getDate();
        var mes = fecha.getMonth() + 1;
        var año = fecha.getFullYear();
        var hora = fecha.getHours();
        var minutos = fecha.getMinutes();
        var segundos = fecha.getSeconds();

        var fechaFormateada = dia + '/' + mes + '/' + año + ' ' + hora + ':' + minutos + ':' + segundos;

        return fechaFormateada;
    }
});








// Asigna las URL a variables JavaScript
var loginURL = "/{% url 'LOG' %}";
var dashboardURL = "/{% url 'IND' %}";
var asistenciaURL = "/{% url 'ASIS' %}";
var listaalumnosURL = "/{% url 'LALU' curso.id %}"; 
var listaasistenciaURL = "/{% url 'LASIS' %}";
var listacursosURL = "/{% url 'LCUR' %}";
var modificarnotasURL = "/{% url 'MODN' curso.id %}";
var notasURL = "/{% url 'NON' %}";
var situacionalumnosURL = "/{% url 'SISA' %}";
var anotacionesURL = "/anotaciones/" + alumno.id + "/";
var comunicadoURL = "/{% url 'comunicado' %}";
var historialcomunicadosURL = "/{% url 'HSC' %}";
var historialanotacionesURL = "/{% url 'HAN' %}";
var perfilURL = "/{% url 'PF' %}";
var crearClaseURL = "/{% url 'crear_clase' %}";
var reprobarAlumnoURL = (alumnoId) => `/reprobar_alumno/${alumnoId}/`;