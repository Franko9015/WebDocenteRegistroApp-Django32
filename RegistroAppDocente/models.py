from django.db import models
from django.contrib.auth.models import User

class PeriodoSemestral(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'periodo_semestral'

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nombrecurso = models.CharField(max_length=100)
    aniocurso = models.IntegerField(blank=True, null=True)
    cantidadalumnos = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Curso'

    def __str__(self):
        return self.nombrecurso

class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'materia'

    def __str__(self):
        return self.nombre

class Clase(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    periodo_semestral = models.ForeignKey(PeriodoSemestral, on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, null=True, blank=True)
    clase_iniciada = models.BooleanField(default=False)

    class Meta:
        db_table = 'clase'

def __str__(self):
    curso_nombre = self.curso.nombrecurso if self.curso else "Sin curso"
    materia_nombre = self.materia.nombre if self.materia else "Sin materia"
    return f'Clase del {self.fecha} - {curso_nombre} - {materia_nombre}'
       





class Alumno(models.Model):
    id = models.AutoField(primary_key=True)
    usera = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto_alumno = models.ImageField(upload_to='foto', null=True, blank=True, default='foto/fotodefault.png')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default=None, null=True)
    asistencias = models.PositiveIntegerField(default=0)
    Reprobado = models.BooleanField(default=False)

    class Meta:
        db_table = 'alumno'

    def __str__(self):
        return str(self.usera)

    def calcular_porcentaje_asistencia(self):
        # Obtén todas las clases del curso del alumno
        clases_del_curso = Clase.objects.filter(curso=self.curso)
        
        # Filtra las clases en función de la fecha de nacimiento del alumno
        clases_programadas = clases_del_curso.filter(
            periodo_semestral__fecha_inicio__lte=self.fecha_nacimiento,
            periodo_semestral__fecha_fin__gte=self.fecha_nacimiento
        )
        
        total_clases_programadas = clases_programadas.count()
        if total_clases_programadas > 0:
            return (self.asistencias / total_clases_programadas) * 100
        return 0


class Profesor(models.Model):
    id = models.AutoField(primary_key=True)
    userp = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    foto_perfil = models.ImageField(upload_to='foto', null=True, blank=True, default='foto/fotodefault.png')
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
        return str(self.userp)

class Notas(models.Model):
    id = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    parcial1 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    parcial2 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    parcial3 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    parcial4 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    examen_final = models.DecimalField(max_digits=3, decimal_places=1, null=True)

    class Meta:
        db_table = 'notas'

    def __str__(self):
        return f'Notas de {self.alumno.usera.first_name} {self.alumno.usera.last_name}'

class Comunicado(models.Model):
    URGENTE = 'U'
    GENERAL = 'G'
    
    TIPO_COMUNICADO_CHOICES = [
        (URGENTE, 'Urgente'),
        (GENERAL, 'General'),
    ]
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    tipo_comunicado = models.CharField(
        max_length=1,
        choices=TIPO_COMUNICADO_CHOICES,
        default=GENERAL
    )

    def __str__(self):
        return self.titulo

class Anotacion(models.Model):
    id = models.AutoField(primary_key=True)
    TIPO_ANOTACION = (
        ('bitacora', 'Bitácora'),
        ('anotacion negativa', 'Anotación Negativa'),
    )

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    tipo_anotacion = models.CharField(max_length=20, choices=TIPO_ANOTACION)
    fecha = models.DateField(auto_now=True)
    comentario = models.TextField()

    class Meta:
        db_table = 'anotacion'

    def __str__(self):
        return f'Notas de {self.alumno.usera.first_name} {self.alumno.usera.last_name}'

