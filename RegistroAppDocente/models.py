from django.db import models

# Create your models here.

class Materia(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'materia'

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombres = models.CharField(max_length=100)
    apellidoP = models.CharField(max_length=100)
    apellidoM = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    asistencias = models.PositiveIntegerField(default=0)
    clases_programadas = models.PositiveIntegerField(default=0)
    Reprobado = models.BooleanField(default=False)

    class Meta:
        db_table = 'alumno'

    def __str__(self):
        return f'{self.nombres} {self.apellidoP} {self.apellidoM}'

    def calcular_porcentaje_asistencia(self):
        if self.clases_programadas > 0:
            return (self.asistencias / self.clases_programadas) * 100
        return 0


class Profesor(models.Model):
    nombres = models.CharField(max_length=100)
    apellidoP = models.CharField(max_length=100)
    apellidoM = models.CharField(max_length=100)
    foto_perfil = models.ImageField(upload_to='perfil_profesor', null=True, blank=True)
    cursos = models.ManyToManyField(Curso)
    titulo = models.CharField(max_length=100)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    cantidad_alumnos = models.IntegerField()
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    redes_sociales = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'profesor'

    def __str__(self):
        return f'{self.nombres} {self.apellidoP} {self.apellidoM}'

class Notas(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    parcial1 = models.DecimalField(max_digits=3, decimal_places=1)
    parcial2 = models.DecimalField(max_digits=3, decimal_places=1)
    parcial3 = models.DecimalField(max_digits=3, decimal_places=1)
    parcial4 = models.DecimalField(max_digits=3, decimal_places=1)
    examen_final = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        db_table = 'notas'

    def __str__(self):
        return f'Notas de {self.alumno.nombres} {self.alumno.apellidoP} {self.alumno.apellidoM}'

class Comunicado(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    es_urgente = models.BooleanField(default=False)  # Campo booleano para indicar si es urgente

    def __str__(self):
        return self.titulo