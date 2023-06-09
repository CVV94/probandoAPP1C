from django.db import models
from django.contrib.auth.models import User             #importacion de una tabla modelo de django

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description= models.TextField(blank=True)           #texto mas largo
    created=models.DateTimeField(auto_now_add=True)     #se rellena automaticamente las fechas
    datecompleted= models.DateTimeField(null=True, blank=True)      #hay que determinar la fecha completada de la tarea, blanck significa que es opcional
    important=models.BooleanField(default=False)        #por defecto la tarea no es importante
    user= models.ForeignKey(User, on_delete=models.CASCADE)                       #hace llamdo a otra tabla User, se tiene que importar # eliminacion en cascada

    def __str__(self) -> str:                           #para mostrar el titulo de la tarea
        return self.title +' (Responsable de cumplimiento: '+ self.user.username +' )'

    #crear superusuario
    #py manage.py createsuperuser

    #guardar migracion
    #py manage.py makemigrations
    #py manage.py migrate