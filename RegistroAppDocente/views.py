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
def listacursos(request):
    return render(request,"listadodecursos.html")
def modificarnotas(request):
    return render(request,"modificarnotas.html")
def notas(request):
    return render(request,"notas.html")
def situacionalumnos(request):
    return render(request,"situacionalumnos.html")
def anotaciones(request):
    return render(request,"anotaciones.html")
def comunicado(request):
    return render(request,"comunicado.html")
