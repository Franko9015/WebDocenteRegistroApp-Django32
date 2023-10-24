from rest_framework import serializers
from .models import *


class PeriodoSemestralSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoSemestral
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class NotasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notas
        fields = '__all__'

class ComunicadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunicado
        fields = '__all__'

class AnotacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anotacion
        fields = '__all__'