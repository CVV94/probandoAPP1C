from django.contrib import admin
from .models import Task            #importacion del modelo

class TaskAdmin(admin.ModelAdmin):      #muestra solo los datos de lectura de la fecha de creacion
    readonly_fields=('created',)

admin.site.register(Task,TaskAdmin)   #   Registra el modelo, registra la clase creada de admin