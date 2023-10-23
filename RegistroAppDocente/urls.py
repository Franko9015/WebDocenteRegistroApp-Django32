from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings

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
    path('modificarnotas/<int:curso_id>/', modificarnotas, name='MODN'),
    path('situacionalumnos/',situacionalumnos,name  ='SISA'),
    path('notas/',notas,name='NON'),
    path('listaasistencia/',listaasistencia,name='LASIS'),
    path('historialcomunicados/', historialcomunicados, name="HSC"),
    path('historialanotaciones/', historialanotaciones, name="HAN"),
    path('Perfil/',perfilprofesor,name='PF'),
    path('api/periodosemestral/', PeriodoSemestralListCreateAPIView().as_view(), name='producto-list-create'),
    path('api/periodosemestral/<int:pk>/', PeriodoSemestralRetrieveUpdateDestroyAPIView.as_view(), name='producto-update'),
    path('api/cursos/', CursoListCreateAPIView.as_view(), name='contacto-list-create'),
    path('api/cursos/<int:pk>/', CursoRetrieveUpdateDestroyAPIView.as_view(), name='contacto-retrieve-update-destroy'),
    path('api/materias/', MateriaListCreateAPIView.as_view(), name='marcas-list-create'),
    path('api/materias/<int:pk>/', MateriaRetrieveUpdateDestroyAPIView.as_view(), name='marcas-retrieve-update-destroy'),
    path('api/alumnos/', AlumnoListCreateAPIView().as_view(), name='modelo-list-create'),
    path('api/alumnos/<int:pk>/', AlumnoRetrieveUpdateDestroyAPIView.as_view(), name='modelo-retrieve-update-destroy'),
    path('api/profesor/', ProfesorListCreateAPIView().as_view(), name='modelo-list-create'),
    path('api/profesor/<int:pk>/', ProfesorRetrieveUpdateDestroyAPIView.as_view(), name='modelo-retrieve-update-destroy'),
    path('api/notas/', NotasListCreateAPIView().as_view(), name='modelo-list-create'),
    path('api/notas/<int:pk>/', NotasRetrieveUpdateDestroyAPIView.as_view(), name='modelo-retrieve-update-destroy'),
    path('api/comunicados/', ComunicadoListCreateAPIView().as_view(), name='modelo-list-create'),
    path('api/comunicados/<int:pk>/', ComunicadoRetrieveUpdateDestroyAPIView.as_view(), name='modelo-retrieve-update-destroy'),
    path('api/anotaciones/', AnotacionListCreateAPIView().as_view(), name='modelo-list-create'),
    path('api/anotaciones/<int:pk>/', AnotacionRetrieveUpdateDestroyAPIView.as_view(), name='modelo-retrieve-update-destroy'),
    path('crear_clase/', crear_clase, name='crear_clase'),
]

