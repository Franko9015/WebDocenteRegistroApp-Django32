from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request,"login.html")
def index(request):
    return render(request,"index.html")
def asistencia(request):
    return render(request,"asistencia.html")
def listaalumnos(request):
    return render(request,"listadealumnos.html")
def listaasistencia(request):
    return render(request,"listadoasistencia.html")