function validarFormulario() {
  var usuario = document.getElementById("username").value;
  var contrasena = document.getElementById("password").value;

  if (usuario.trim() === "" && contrasena.trim() === "") {
      // Caso 1: Ambos campos están vacíos
      Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Debes llenar los campos de usuario y contraseña',
      });
  } else if (usuario.trim() === "") {
      // Caso 2: El campo de usuario está vacío
      Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Debes llenar el campo de usuario',
      });
  } else if (contrasena.trim() === "") {
      // Caso 3: El campo de contraseña está vacío
      Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Debes llenar el campo de contraseña',
      });
  } else {
      // Mostrar la animación de inicio de sesión
      const loginAnimation = document.querySelector('.login-animation');
      loginAnimation.style.display = 'flex';

      // Simula un inicio de sesión después de 3 segundos (reemplaza esto con tu lógica real)
      setTimeout(function () {
          // Ocultar la animación y redireccionar al usuario
          loginAnimation.style.display = 'none';
          window.location.href = "dashboard/"; // Redirecciona al index.html
      }, 3000); // 3000 milisegundos (3 segundos)
  }
}



        // Asigna las URL a variables JavaScript
        var loginURL = "{% url 'LOG' %}";
        var dashboardURL = "{% url 'IND' %}";
        var asistenciaURL = "{% url 'ASIS' %}";
        var listaalumnosURL = "{% url 'LALU' %}";
        var listaasistenciaURL = "{% url 'LASIS' %}";
        var listacursosURL = "{% url 'LCUR' %}";
        var modificarnotasURL = "{% url 'MODN' %}";
        var notasURL = "{% url 'NON' %}";
        var situacionalumnosURL = "{% url 'SISA' %}";
        var anotacionesURL = "{% url 'ANOT' %}";
        var comunicadoURL = "{% url 'comunicado' %}";
        var historialcomunicadosURL = "{% url 'HSC' %}";  // Agregado para el historial de comunicados
        var historialanotacionesURL = "{% url 'HAN' %}";  // URL sin argumento de 'username'
        var perfilURL = "{% url 'PF' %}";  // Agregado para el perfil con el nombre de usuario