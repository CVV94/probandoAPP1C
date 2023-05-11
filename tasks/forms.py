#from django.forms import ModelForm        #creacion de importacion de formularios
from django import forms
from .models import Task                    #importamos nuestro modelo de tarea sqlite3

class TaskForm(forms.ModelForm):                      #creacion de formulario personalizado
    class Meta:                                 #Clase Meta es para especificar los detalles del modelo a utilizar
        model=Task                              #modelo Task a utilizar
        fields= ['title','description','important'] #fields son las descripciones del modelo

        widgets={
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Write a title'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input  my-3 m-auto'}),
            
        }