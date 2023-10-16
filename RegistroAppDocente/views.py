from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import qrcode
from django.http import HttpResponse
from .forms import ComunicadoForm 
from .forms import AsistenciaForm
from io import BytesIO
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirigir al panel de control o a la página deseada después del inicio de sesión
            return redirect('nombre_de_la_vista')
        else:
            # Mostrar un mensaje de error en caso de credenciales incorrectas
            error_message = "Credenciales incorrectas. Por favor, inténtelo de nuevo."

    return render(request, "login.html")

def index(request):
    user = request.user  # Obtén el usuario autenticado

    if user.is_authenticated:
        full_name = user.get_full_name()  # Obtén el nombre completo del usuario autenticado
    else:
        full_name = "Profesor X"  # Nombre por defecto si no hay usuario autenticado

    return render(request, "index.html", {'full_name': full_name})

def generate_qr_code(student_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(student_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
def asistencia(request, clase_id):
    # Obtener la clase por su ID o mostrar un error 404 si no existe
    clase = get_object_or_404(Clase, pk=clase_id)
    
    # Obtener la lista de estudiantes para la clase actual
    students = Alumno.objects.filter(curso=clase.curso)

    # Generar y almacenar los códigos QR para cada estudiante
    qr_codes = {}
    for student in students:
        qr_code = generate_qr_code(student.usera.username)  # Utiliza el campo 'username' del usuario asociado
        qr_codes[student.id] = qr_code

    if request.method == 'POST':
        # Procesar el formulario de asistencia
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            for student in students:
                # Obtener el campo de asistencia del formulario para el estudiante actual
                presente_field = f"presente_{student.id}"
                ausente_field = f"ausente_{student.id}"

                # Verificar si el estudiante ha sido marcado como presente o ausente
                if form.cleaned_data[presente_field]:
                    student.asistencias += 1
                elif form.cleaned_data[ausente_field]:
                    # Si se marca como ausente, no hacer nada, ya que el valor predeterminado es 0 asistencias
                    pass
                else:
                    # Manejar errores si es necesario
                    pass

                # Guardar el estudiante actualizado en la base de datos
                student.save()

            # Redirigir o mostrar un mensaje de éxito
            return redirect('listaasistencia')
    
    else:
        # Crear un formulario de asistencia vacío
        form = AsistenciaForm()

    # Renderizar la plantilla con los formularios de asistencia y los códigos QR
    return render(request, "asistencia.html", {"students": students, "clase": clase, "form": form, "qr_codes": qr_codes})


def listaalumnos(request, curso_id):
    alumnos = Alumno.objects.filter(curso_id=curso_id)
    for alumno in alumnos:
        if alumno.fecha_nacimiento:
            today = datetime.today()
            age = today.year - alumno.fecha_nacimiento.year - ((today.month, today.day) < (alumno.fecha_nacimiento.month, alumno.fecha_nacimiento.day))
            alumno.edad = age
        else:
            alumno.edad = None  # Otra opción si no hay fecha de nacimiento registrada
    return render(request, "listadealumnos.html", {"alumnos": alumnos})


def listaasistencia(request, curso_id):
    # Obtén una lista de clases para el curso específico
    clases = Clase.objects.filter(curso__id=curso_id)

    # Calcula el total de asistencias de todos los alumnos en el curso específico
    total_asistencias = Alumno.objects.filter(curso__id=curso_id).aggregate(total_asistencias=models.Sum('asistencias'))['total_asistencias']
    
    # Calcula el total de alumnos en el curso específico
    total_alumnos = Alumno.objects.filter(curso__id=curso_id).count()

    # Inicializa el porcentaje en cero por defecto
    porcentaje_asistencia_general = 0

    # Verifica que haya al menos un alumno antes de calcular el porcentaje
    if total_alumnos > 0:
        # Calcula el porcentaje solo si hay clases, de lo contrario, permanece en 0
        if len(clases) > 0:
            porcentaje_asistencia_general = (total_asistencias / (total_alumnos * len(clases))) * 100

    return render(request, "listadoasistencia.html", {'porcentaje_asistencia_general': porcentaje_asistencia_general})




def listacursos(request):
    cursos = Curso.objects.annotate(cantidad_alumnos=models.Count('alumno'))  # Calcula la cantidad de alumnos por curso
    return render(request, "listadodecursos.html", {'cursos': cursos})

def modificarnotas(request):
    return render(request, "modificarnotas.html")

def notas(request):
    return render(request, "notas.html")

def situacionalumnos(request):
    return render(request, "situacionalumnos.html")

def anotaciones(request, alumno_id):
    # Encuentra el alumno en función del ID
    try:
        alumno = Alumno.objects.get(id=alumno_id)
    except Alumno.DoesNotExist:
        return render(request, "anotaciones.html", {'error': 'No se encontró al alumno'})

    if request.method == 'POST':
        tipo_anotacion = request.POST.get('tipoAnotacion')
        comentario = request.POST.get('comentario')

        # Crea una nueva anotación y guárdala en la base de datos
        anotacion = Anotacion(alumno=alumno, tipo_anotacion=tipo_anotacion, comentario=comentario)
        anotacion.save()

        return JsonResponse({'success': True})

    return render(request, "anotaciones.html", {'alumno': alumno})

def comunicado(request):
    if request.method == 'POST':
        tipoComunicado = request.POST.get('tipoComunicado')
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')

        # Crea un nuevo comunicado y guárdalo en la base de datos
        comunicado = Comunicado(
            tipo_comunicado=tipoComunicado,
            titulo=titulo,
            contenido=contenido
        )
        comunicado.save()

        return JsonResponse({'success': True})

    return render(request, "comunicado.html", {})

def perfilprofesor(request):
    return render(request, "PerfilProfesor.html")

def historialanotaciones(request):
    # Recupera todas las anotaciones con información de alumno, curso y otros campos relacionados
    anotaciones = Anotacion.objects.select_related('alumno__curso').all()

    return render(request, "historialanotaciones.html", {'anotaciones': anotaciones})

def historialcomunicados(request):
    comunicados = Comunicado.objects.all()
    # Recupera todos los comunicados
    return render(request, "historialdecomunicados.html", {'comunicados': comunicados})
