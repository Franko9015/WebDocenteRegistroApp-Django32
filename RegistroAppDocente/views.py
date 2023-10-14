from django.shortcuts import render, redirect
from .models import *
import qrcode
from django.http import HttpResponse
from .forms import ComunicadoForm 
from io import BytesIO
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
def login(request):
    return render(request, "login.html")

def index(request):
    user = request.user  # Obtén el usuario autenticado

    if user.is_authenticated:
        full_name = user.get_full_name()  # Obtén el nombre completo del usuario autenticado
    else:
        full_name = "Profesor X"  # Nombre por defecto si no hay usuario autenticado

    return render(request, "index.html", {'full_name': full_name})

def asistencia(request):
    return render(request, "asistencia.html")

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

def listaasistencia(request):
    return render(request, "listadoasistencia.html")

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

def generar_qr(request):
    # Obtener la fecha actual
    fecha_asistencia = timezone.now().strftime("%Y-%m-%d")

    # Resto del código para generar el código QR (sin cambios)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(fecha_asistencia)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type="image/png")
    return response