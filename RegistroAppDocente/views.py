from django.shortcuts import render, redirect
from .models import *
import qrcode
from django.http import HttpResponse
from .forms import ComunicadoForm 
from io import BytesIO
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

def listaalumnos(request):
    return render(request, "listadealumnos.html")

def listaasistencia(request):
    return render(request, "listadoasistencia.html")

def listacursos(request):
    return render(request, "listadodecursos.html")

def modificarnotas(request):
    return render(request, "modificarnotas.html")

def notas(request):
    return render(request, "notas.html")

def situacionalumnos(request):
    return render(request, "situacionalumnos.html")

def anotaciones(request):
    return render(request, "anotaciones.html")

def comunicado(request):
    if request.method == 'POST':
        form = ComunicadoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el comunicado en la base de datos

    # Si no es una solicitud POST o el formulario no es válido, simplemente muestra el formulario nuevamente
    else:
        form = ComunicadoForm()

    return render(request, "comunicado.html", {'form': form})

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