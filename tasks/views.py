# render nativo y redirect es para redireccionar
from django.shortcuts import render, redirect ,get_object_or_404                      	# creacion de un login  , autentificacion despues del registro
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  							# guarda datos   			
from django.contrib.auth import login, logout, authenticate				# crea un autoguardado de los registros(registro,salir,autentificar logeo)
from django.http import HttpResponse  									# imprime mensajes
from .forms import TaskForm
from .models import Task
from django.utils import timezone                                       #importacion de date completados
from django.contrib.auth.decorators import login_required   #importacion para autenticar que uno esta logiado para desplazarse entre las url (ir a settings tambien)
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

@login_required
def tasks(request):
    tasks=Task.objects.filter(user=request.user , datecompleted__isnull=True)  #guarda en una variable all(todas las tareas que estan en la base de datos) #filter solo muestra las tareas pertenecientes al usuario actual
    return render(request, 'tasks.html',{'tasks': tasks})                      # date completed_isnull = True solo muestra tareas que no han sido completadas

@login_required
def tasks_completed(request):
    tasks=Task.objects.filter(user=request.user , datecompleted__isnull=False).order_by('-datecompleted') #guarda en una variable all(todas las tareas que estan en la base de datos) #filter solo muestra las tareas pertenecientes al usuario actual
    return render(request, 'tasks.html',{'tasks': tasks})                      # date completed_isnull = False solo muestra tareas que han sido completadas

@login_required
def create_task(request):
    if request.method == 'GET':                         # si el metodo es GET muestrame la plantilla en blanco
        return render(request, 'create_task.html',{
        'form': TaskForm
        })
    else:
        try:
            form=TaskForm(request.POST)
            new_task=form.save(commit=False)# guarda en una instancia la base de datos evitando que se guarde
            new_task.user=request.user    #guarda en una variable al usuario autenticado
            new_task.save()                 #guarda la tarea en la base de datos
            return redirect('tasks')      #redirecciona a la lista de tareas
        except ValueError:
            return render(request,'create_task.html', {         #devuelme en la misma plantilla de tareas errores si ubieron
                'form': TaskForm,
                'error':'Please provide valida data'

            })

@login_required        
def task_detail(request ,task_id):      #detalle
    if request.method == 'GET':
        task =get_object_or_404(Task, pk=task_id)         #get_object_or_404(es una importacion para cuando no aparesca la url salga un error de pagina no encontrada
        form=TaskForm(instance=task)                      #visualiza el formulario en la misma instancia para su actualizacion
        return render(request,'task_detail.html',{'task':task ,'form':form})  #Task= base de datos , pk = al numero de tareas ,http://127.0.0.1:8000/tasks/3/
    else:
        try:
            task= get_object_or_404(Task, pk=task_id ,user=request.user) 
            form= TaskForm(request.POST, instance=task)        #actualizar valor
            form.save()
            return redirect('tasks')
        except:
            return render(request,'task_detail.html',{'task':task ,'form':form,
            'error':'Error en la actualizacion de tareas'}) 

@login_required
def signout(request):											#Cerrar sesion
    logout(request)  # logout es una importacion que se sale de una sesion
    return redirect('home')  # es una redireccion

@login_required
def complete_task(request, task_id):
    task= get_object_or_404(Task, pk=task_id , user=request.user)
    if request.method=='POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')
@login_required    
def delete_task(request, task_id):
    task= get_object_or_404(Task, pk=task_id , user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')
    


    
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

