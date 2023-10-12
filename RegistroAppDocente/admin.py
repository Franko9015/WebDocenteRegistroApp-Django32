from django.contrib import admin
from .models import Curso, Materia, Alumno, Profesor, Notas, Comunicado, Anotacion

# Registra los modelos aquí
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Notas)
admin.site.register(Comunicado)
admin.site.register(Anotacion)
