from django.contrib import admin
from .models import Task            #importacion del modelo
# Register your models here.

admin.site.register(Task)   #   Registra el modelo