from django.contrib import admin
from django.urls import path
from .views import *

#Ejemplo
#path('',index,name='IND'),
#path('galeria/',galeria,name='GALE'),
#path('quienes/',quienes,name='QUIEN'),
#path('formulario/',formulario,name='FORMU'),

urlpatterns = [
    path('',login,name='login'),
    path('dashboard/',index,name='index'),
    path('asistencia/',asistencia,name='asistencia'),
    path('listaalumnos/',listaalumnos,name='alumnosl'),
]