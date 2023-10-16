from django.contrib import admin
from django.urls import path
from .views import *

#Ejemplo
#path('',index,name='IND'),
#path('galeria/',galeria,name='GALE'),
#path('quienes/',quienes,name='QUIEN'),
#path('formulario/',formulario,name='FORMU'),

urlpatterns = [
    path('',login,name='LOG'),
    path('dashboard/',index,name='IND'),
    path('asistencia/<int:clase_id>/', asistencia, name='ASIS'),
    path('listaalumnos/<int:curso_id>/', listaalumnos, name='LALU'),
    path('anotaciones/<int:alumno_id>/', anotaciones, name='anotaciones'),
    path('comunicados/', comunicado, name='comunicado'),
    path('listacursos/',listacursos,name='LCUR'),
    path('modificarnotas/',modificarnotas,name='MODN'),
    path('situacionalumnos/',situacionalumnos,name  ='SISA'),
    path('notas/',notas,name='NON'),
    path('listaasistencia/',listaasistencia,name='LASIS'),
    path('historialcomunicados/', historialcomunicados, name="HSC"),
    path('historialanotaciones/', historialanotaciones, name="HAN"),
    path('Perfil/',perfilprofesor,name='PF'),
]

