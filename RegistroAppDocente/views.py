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
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import date 
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, authenticate
from .serializers import *
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from decimal import Decimal
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, F, Sum, ExpressionWrapper, FloatField
from django.db.models import OuterRef, Subquery
from django.db.models import Count, Sum, F, FloatField, ExpressionWrapper, Subquery, OuterRef

from django import forms
from django.forms import formset_factory


# Create your views here.
def login(request):
    error_message = None  # Inicializar la variable error_message
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userp = authenticate(request, username=username, password=password)

        if userp is not None:
            auth_login(request, userp)
            return redirect('dashboard/')  # Asegúrate de que 'index.html' sea la URL correcta a la que deseas redirigir

        else:
            # Mostrar un mensaje de error en caso de credenciales incorrectas
            error_message = "Credenciales incorrectas. Por favor, inténtelo de nuevo."

    return render(request, "login.html", {"error_message": error_message})


def index(request):
    user = request.user  # Obtén el usuario autenticado

    if user.is_authenticated:
        full_name = user.get_full_name()  # Obtén el nombre completo del usuario autenticado
    else:
        full_name = "Profesor X"  # Nombre por defecto si no hay usuario autenticado

    return render(request, "index.html", {'full_name': full_name})

def generate_qr_code(qr_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
    
def asistencia(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    students = Alumno.objects.filter(curso=clase.curso)

    if request.method == 'POST':
        for student in students:
            asistencia = request.POST.get(f'asistencia_{student.id}')
            if asistencia == 'presente':
                student.asistencias += 1
                student.save()
        return redirect('listaasistencia')
    
    return render(request, "asistencia.html", {"students": students, "clase": clase})



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
        cantidad_alumnos=Subquery(
            Alumno.objects.filter(curso=OuterRef('pk')).values('curso').annotate(
                num_alumnos=Count('curso')
            ).values('num_alumnos')[:1]
        ),
        total_clases=Count('clase'),
        total_asistencias=Subquery(
            Alumno.objects.filter(curso=OuterRef('pk')).values('curso').annotate(
                num_asistencias=Sum('asistencias')
            ).values('num_asistencias')[:1]
        ),
        porcentaje_asistencia=ExpressionWrapper(
            (F('total_asistencias') / (F('total_clases') * 1.0 * F('cantidad_alumnos'))) * 100,
            output_field=FloatField()
        )
    )
    return render(request, "listadoasistencia.html", {'cursos': cursos})





def listacursos(request):
    cursos = Curso.objects.annotate(cantidad_alumnos=models.Count('alumno'))  # Calcula la cantidad de alumnos por curso
    return render(request, "listadodecursos.html", {'cursos': cursos})

def modificarnotas(request, curso_id):
    # Obtén el curso específico basado en el ID proporcionado
    curso = Curso.objects.get(id=curso_id)

    # Obtén una lista de alumnos en este curso
    alumnos = Alumno.objects.filter(curso=curso).prefetch_related('notas_set')

    if request.method == 'POST':
        # Maneja el formulario de modificación de notas y guarda los cambios en la base de datos
        for alumno in alumnos:
            # Obtiene los valores de las notas del formulario
            parcial1 = request.POST.get(f'parcial1_{alumno.id}')
            parcial2 = request.POST.get(f'parcial2_{alumno.id}')
            parcial3 = request.POST.get(f'parcial3_{alumno.id}')
            parcial4 = request.POST.get(f'parcial4_{alumno.id}')
            examen_final = request.POST.get(f'examen_final_{alumno.id}')

            # Realiza la validación de los valores antes de guardarlos
            try:
                # Convierte los valores a Decimal si existen, de lo contrario, establece en None
                parcial1 = Decimal(parcial1) if parcial1 else None
                parcial2 = Decimal(parcial2) if parcial2 else None
                parcial3 = Decimal(parcial3) if parcial3 else None
                parcial4 = Decimal(parcial4) if parcial4 else None
                examen_final = Decimal(examen_final) if examen_final else None
            except (ValueError, TypeError):
                # Establece un mensaje de error si los valores no son válidos
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
    cursos = Curso.objects.all().annotate(
        cantidad_alumnos=Subquery(
            Alumno.objects.filter(curso=OuterRef('pk')).values('curso').annotate(
                num_alumnos=Count('curso')
            ).values('num_alumnos')[:1]
        )
    )
    return render(request, "notas.html", {'cursos': cursos})


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
    dashboard_url = reverse('IND')
    return render(request, "comunicado.html", {'dashboard_url': dashboard_url})

def reprobar_alumno(request, alumno_id):
    try:
        # Obtener al alumno de la base de datos
        alumno = Alumno.objects.get(pk=alumno_id)
        
        # Realizar las acciones necesarias para marcar al alumno como reprobado (por ejemplo, actualizar un campo en el modelo Alumno)
        alumno.Reprobado = True
        alumno.save()
        
        return JsonResponse({'success': True})
    except Alumno.DoesNotExist:
        return JsonResponse({'success': False})
    
    
def situacionalumnos(request):
    alumnos = Alumno.objects.filter(Reprobado=False).annotate(
        total_clases=Subquery(
            Clase.objects.filter(curso=OuterRef('curso')).values('curso').annotate(
                num_clases=Count('curso')
            ).values('num_clases')[:1]
        ),
        porcentaje_asistencia=ExpressionWrapper(
            (F('asistencias') / (F('total_clases') * 1.0)) * 100,
            output_field=FloatField()
        )
    )

    # Filtra a los alumnos con un porcentaje de asistencia inferior al 70%
    alumnos_reprobados = alumnos.filter(porcentaje_asistencia__lt=70)

    return render(request, "situacionalumnos.html", {"alumnos_reprobados": alumnos_reprobados})




@login_required
def perfilprofesor(request):
    # Recuperar el profesor relacionado con el usuario actual
    profesor = Profesor.objects.get(userp=request.user)
    data = {
        'profesor': profesor 
    }
    return render(request, "PerfilProfesor.html",data)

def historialanotaciones(request):
    # Recupera todas las anotaciones con información de alumno, curso y otros campos relacionados
    anotaciones = Anotacion.objects.select_related('alumno__curso').all()

    return render(request, "historialanotaciones.html", {'anotaciones': anotaciones})

def historialcomunicados(request):
    comunicados = Comunicado.objects.all()
    # Recupera todos los comunicados
    return render(request, "historialdecomunicados.html", {'comunicados': comunicados})

@csrf_protect
def crear_clase(request):
    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        
        # Asegúrate de obtener el curso correspondiente o mostrar un error si no existe
        curso = get_object_or_404(Curso, pk=curso_id)
        
        # Obtén la fecha actual
        fecha_actual = date.today()
        
        # Aquí puedes crear el registro de clase con la información necesaria
        nueva_clase = Clase(
            fecha=fecha_actual,
            curso=curso,
            clase_iniciada=True
        )
        nueva_clase.save()

        # Obtén la URL de asistencia con la ID de la clase
        asistencia_url = reverse('ASIS', args=[nueva_clase.id])

        # Envía una respuesta JSON que incluye la URL de redirección
        return JsonResponse({'message': 'Clase creada exitosamente', 'redirect': asistencia_url})
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

@csrf_protect
def terminar_clase(request):
    if request.method == 'POST':
        clase_id = request.POST.get('clase_id')
        try:
            # Asegúrate de obtener la clase correspondiente
            clase = Clase.objects.get(pk=clase_id)
            
            # Marca la clase como finalizada y no iniciada
            clase.clase_iniciada = False
            clase.clase_finalizada = True
            clase.save()
            
            # Construye la URL de redirección
            listaasistenciaURL = reverse('LASIS')  # Asegúrate de que 'LASIS' sea el nombre correcto de tu URL
            return JsonResponse({'message': 'Clase finalizada con éxito', 'redirect': listaasistenciaURL})
        except Clase.DoesNotExist:
            return JsonResponse({'error': 'Clase no encontrada'}, status=404)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)
from django.http import JsonResponse

def incrementar_asistencia(request):
    alumno_id = request.GET.get('alumno_id')
    try:
        alumno = Alumno.objects.get(pk=alumno_id)
        alumno.asistencias += 1
        alumno.save()
        return JsonResponse({'success': True})
    except Alumno.DoesNotExist:
        return JsonResponse({'success': False})


#####################################-----------METODOS API-------------#########################################################################

class PeriodoSemestralListCreateAPIView(generics.ListCreateAPIView):
    queryset = PeriodoSemestral.objects.all()
    serializer_class = PeriodoSemestralSerializer

class PeriodoSemestralRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PeriodoSemestral.objects.all()
    serializer_class = PeriodoSemestralSerializer

class CursoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class CursoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class MateriaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class MateriaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class AlumnoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class AlumnoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class ProfesorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class ProfesorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class NotasListCreateAPIView(generics.ListCreateAPIView):
    queryset = Notas.objects.all()
    serializer_class = NotasSerializer

class NotasRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notas.objects.all()
    serializer_class = NotasSerializer

class ComunicadoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comunicado.objects.all()
    serializer_class = ComunicadoSerializer

class ComunicadoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comunicado.objects.all()
    serializer_class = ComunicadoSerializer

class AnotacionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Anotacion.objects.all()
    serializer_class = AnotacionSerializer

class AnotacionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anotacion.objects.all()
    serializer_class = AnotacionSerializer
