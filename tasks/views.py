# render nativo y redirect es para redireccionar
from django.shortcuts import render, redirect                         	# creacion de un login  , autentificacion despues del registro
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  							# guarda datos   			
from django.contrib.auth import login, logout, authenticate				# crea un autoguardado de los registros(registro,salir,autentificar logeo)
from django.http import HttpResponse  									# imprime mensajes


def home(request):								#index
    return render(request, 'home.html')


def signup(request):							#Registrarse

    if request.method == 'GET':              # Get es para enviar formulario y Post Recibe formulario
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registro
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)  # guarda el user  antes de redireccionar
                return redirect('tasks')  # guarda el registro

            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existente',
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password no coincide'
        })


def tasks(request):												#Tareas
    return render(request, 'tasks.html')


def signout(request):											#Cerrar sesion
    logout(request)  # logout es una importacion que se sale de una sesion
    return redirect('home')  # es una redireccion

    
def signin(request):											#iniciar sesion
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error':'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks') # es una redireccion


