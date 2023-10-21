from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import qrcode
import json
from django.http import HttpResponse
from .forms import ComunicadoForm 
from .forms import AsistenciaForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, F, Sum, ExpressionWrapper, FloatField

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


def listaasistencia(request):
    cursos = Curso.objects.all().annotate(
        cantidad_alumnos=Count('alumno'),
        total_clases=Count('clase'),
        total_asistencias=Sum(F('alumno__asistencias')),
        porcentaje_asistencia=ExpressionWrapper(
            (F('total_asistencias') / (F('cantidad_alumnos') * F('total_clases'))) * 100,
            output_field=FloatField()
        )
    )
    return render(request, "listadoasistencia.html", {'cursos': cursos})



def listacursos(request):
    cursos = Curso.objects.annotate(cantidad_alumnos=models.Count('alumno'))  # Calcula la cantidad de alumnos por curso
    return render(request, "listadodecursos.html", {'cursos': cursos})

def modificarnotas(request, curso_id):
    # Obtén el curso específico basado en el ID proporcionado
    curso = Curso.objects.get(pk=curso_id)

    # Obtén una lista de alumnos en este curso
    alumnos = Alumno.objects.filter(curso=curso)

    if request.method == 'POST':
        # Maneja el formulario de modificación de notas y guarda los cambios en la base de datos
        for alumno in alumnos:
            parcial1 = request.POST.get(f'parcial1_{alumno.id}')
            parcial2 = request.POST.get(f'parcial2_{alumno.id}')
            parcial3 = request.POST.get(f'parcial3_{alumno.id}')
            parcial4 = request.POST.get(f'parcial4_{alumno.id}')
            examen_final = request.POST.get(f'examen_final_{alumno.id}')

            # Realiza la validación de los valores antes de guardarlos
            try:
                parcial1 = Decimal(parcial1) if parcial1 else None
                parcial2 = Decimal(parcial2) if parcial2 else None
                parcial3 = Decimal(parcial3) if parcial3 else None
                parcial4 = Decimal(parcial4) if parcial4 else None
                examen_final = Decimal(examen_final) if examen_final else None
            except (ValueError, TypeError):
                # Establece un mensaje de error
                error_message = "Hubo un error al procesar los valores de las notas. Asegúrate de ingresar números válidos."
                messages.error(request, error_message)
            else:
                # Guarda o actualiza las notas en la base de datos si la validación fue exitosa
                notas, created = Notas.objects.get_or_create(alumno=alumno)
                notas.parcial1 = parcial1
                notas.parcial2 = parcial2
                notas.parcial3 = parcial3
                notas.parcial4 = parcial4
                notas.examen_final = examen_final
                notas.save()

        # Después de procesar los cambios, muestra un mensaje de éxito
        success_message = "Notas modificadas con éxito."
        messages.success(request, success_message)

        # Redirecciona al índice o dashboard
        return redirect('IND')  # Asegúrate de que 'index' sea el nombre correcto de la URL

    return render(request, "modificarnotas.html", {'curso': curso, 'alumnos': alumnos})

def notas(request):
    cursos = Curso.objects.all()  # Obtén una lista de todos los cursos

    return render(request, "notas.html", {'cursos': cursos})

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

@csrf_exempt  # Agrega esta decoración
def crear_clase(request):
    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        
        # Asegúrate de obtener el curso correspondiente o mostrar un error si no existe
        curso = get_object_or_404(Curso, pk=curso_id)
        
        # Aquí puedes crear el registro de clase con la información necesaria
        # como la fecha, materia, etc. Esto es solo un ejemplo básico:
        nueva_clase = Clase(
            fecha=datetime.date.today(),  # Puedes personalizar la fecha
            curso=curso,                # Asigna el curso correspondiente
            materia=None,               # Añade la materia si es necesario
            clase_iniciada=True         # Marca la clase como iniciada
        )
        nueva_clase.save()
        
        # Envía una respuesta JSON para indicar que se creó la clase con éxito y la URL de redirección
        return JsonResponse({'message': 'Clase creada exitosamente', 'redirect': asistenciaURL})
    else:
        # En caso de una solicitud incorrecta, devuelva un error apropiado
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)