from django.shortcuts import render, redirect, get_object_or_404
from AppCoder.models import Curso, Alumno, Profesor, Entregable, Avatar
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from AppCoder.forms import Curso_formulario, Alumno_formulario, Profesor_formulario, Entregable_formulario, UserEditForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import AvatarForm
from django.shortcuts import render, redirect
from django.conf import settings


# Create your views here.
# -------------------------------------------------------------------------------------------------
# VIEWS DE LOGIN
# -------------------------------------------------------------------------------------------------


def login_request(request):
    cursos = Curso.objects.all()
    c_cursos = cursos.count()        
    alumnos = Alumno.objects.all()
    c_alumnos = alumnos.count()        
    profesores = Profesor.objects.all()
    c_profesores = profesores.count()        
    entregables = Entregable.objects.all()
    c_entregables = entregables.count()        

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario, password=contra, staff=True)

            if user is not None:
                # Verificamos si el usuario es staff
                #if user.is_staff:
                    # Si ya es staff, procedemos a iniciar sesión
                login(request, user)
                avatares = Avatar.objects.filter(user=request.user.id)
                return render( request, "index.html", {"url": avatares[0].imagen.url,
                            "mensaje": f"Bienvenido/a {usuario}", "usuario": usuario, "c_cursos": c_cursos,
                            "c_alumnos": c_alumnos, "c_profesores": c_profesores, "c_entregables": c_entregables})
                #else:
                    # Si no es staff, podemos asignarle el estado de staff aquí
                #    user.is_staff = True
                #    user.save()
                    # Y luego iniciamos sesión
                #    login(request, user)
                #    avatares = Avatar.objects.filter(user=request.user.id)
                #    return render(request, "index.html", {"url": avatares[0].imagen.url,
                #            "mensaje": f"Bienvenido/a {usuario}", "usuario": usuario, "c_cursos": c_cursos,
                #            "c_alumnos": c_alumnos, "c_profesores": c_profesores, "c_entregables": c_entregables})
            else:
                return HttpResponse(f"Usuario no encontrado")
        else:
            form = AuthenticationForm()
            return render(request, "login.html", {"form": form})
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        # Guardo usuario y password
        form = UserCreationForm(request.POST)
        # Guardo imagen por default que esta oculto en el registro.html
        avatar_form = AvatarForm(request.POST, request.FILES)
        if form.is_valid() and avatar_form.is_valid():
            user = form.save()
            # Crear una instancia de Avatar asociada con el usuario
            avatar = Avatar(user=user, imagen=avatar_form.cleaned_data['imagen'])
            avatar.save()
            # Asigno roll de staff
            user.is_staff = True
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        avatar_form = AvatarForm()
    return render(request, "registro.html", {"form": form, "avatar_form": avatar_form})


@login_required
def agregar_avatar(request):
    cursos = Curso.objects.all()
    c_cursos = cursos.count()
    alumnos = Alumno.objects.all()
    c_alumnos = alumnos.count()
    profesores = Profesor.objects.all()
    c_profesores = profesores.count()
    entregables = Entregable.objects.all()
    c_entregables = entregables.count()
    # Obtiene el avatar del usuario
    archivo_seleccionado = request.FILES.get('imagen')
    usuario = request.user.id
    if request.method == "POST":
        # Obtén el archivo subido desde request.FILES
        if archivo_seleccionado:
            # Puedes obtener el nombre del archivo con archivo_subido.name
            avatar = Avatar.objects.get(user=usuario)
            avatar.imagen = archivo_seleccionado
            avatar.save()
            # form = UserEditForm(request.POST, instance=request.user)
            dashboard_seleccionado = True
            avatares = Avatar.objects.filter(user=usuario)
            return render(request, "index.html", {"url": avatares[0].imagen.url,
                        "mensaje": f"Bienvenido/a {usuario}", "usuario": usuario,
                        "c_cursos": c_cursos, "c_alumnos": c_alumnos, "c_profesores": c_profesores,
                        "c_entregables": c_entregables, "dashboard_seleccionado": dashboard_seleccionado})
            #return render(request, "editar_perfil.html", {"url": avatares[0].imagen.url, "mi_formulario": form,
                                                        #"usuario": usuario, "perfil_seleccionado": perfil_seleccionado})
    else:
        form = AvatarForm()
    perfil_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, 'frm_avatar.html', {'form': form, "url": avatares[0].imagen.url,
                                                    "perfil_seleccionado": perfil_seleccionado})


#@login_request  # <-- DECORADORES
def editarPerfil(request):
    global formulario
    cursos = Curso.objects.all()
    c_cursos = cursos.count()
    alumnos = Alumno.objects.all()
    c_alumnos = alumnos.count()
    profesores = Profesor.objects.all()
    c_profesores = profesores.count()
    entregables = Entregable.objects.all()
    c_entregables = entregables.count()
    usuario = request.user
    mi_formulario = UserEditForm(request.POST, instance=request.user)
    # Obtener los nombres de los campos del formulario
    #nombres_de_campos = mi_formulario.fields.keys()
    #print(nombres_de_campos)
    # Imprimir los nombres de los campos (puedes hacer algo con ellos según tus necesidades)
    #print(nombres_de_campos)
    if request.method == 'POST':
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            usuario.email = informacion["email"]
            password = informacion['password1']
            usuario.set_password(password)
            usuario.save()
            user = authenticate(username=usuario, password=password, staff=True)
            login(request, user)
            dashboard_seleccionado = True
            avatares = Avatar.objects.filter(user=usuario)
            return render(request, "index.html", {"url": avatares[0].imagen.url,
                        "mensaje": f"Bienvenido/a {usuario}", "usuario": usuario,
                        "c_cursos": c_cursos, "c_alumnos": c_alumnos, "c_profesores": c_profesores,
                        "c_entregables": c_entregables, "dashboard_seleccionado": dashboard_seleccionado})
    else:
        formulario = UserEditForm(initial={"email": usuario.email})
    perfil_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "editar_perfil.html", {"url": avatares[0].imagen.url, "mi_formulario": formulario,
                                                "usuario": request.user.id, "perfil_seleccionado": perfil_seleccionado})

'''
class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    template_name = 'cambiar_contrasenia.html'
    success_url = reverse_lazy('EditarPerfil')
'''


def inicio(request):
    cursos = Curso.objects.all()
    c_cursos = cursos.count()        
    alumnos = Alumno.objects.all()
    c_alumnos = alumnos.count()        
    profesores = Profesor.objects.all()
    c_profesores = profesores.count()        
    entregables = Entregable.objects.all()
    c_entregables = entregables.count()        
    user = request.user.id
    if user is not None:
        buscar_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request , "buscar_camada.html", {"url": avatares[0].imagen.url,
                                                    "buscar_seleccionado": buscar_seleccionado})
    return render( request , "index.html" , {"c_cursos": c_cursos, "c_alumnos": c_alumnos, "c_profesores": c_profesores,
                                            "c_entregables": c_entregables})


def buscarc(request):
    if request.GET["camada"]:
        camada = request.GET["camada"]
        cursos = Curso.objects.filter(camada__icontains=camada)
        user = request.user.id
        if user is not None:
            buscar_seleccionado = True
            avatares = Avatar.objects.filter(user=request.user.id)
            return render(request , "rb_camada.html", {"url": avatares[0].imagen.url, "cursos": cursos,
                                                    "buscar_seleccionado": buscar_seleccionado})
        return render( request , "rb_camada.html", {"cursos": cursos})
    else:
        return HttpResponse("Ingrese el nombre de la camada")


def dashboard(request):
    cursos = Curso.objects.all()
    c_cursos = cursos.count()        
    alumnos = Alumno.objects.all()
    c_alumnos = alumnos.count()        
    profesores = Profesor.objects.all()
    c_profesores = profesores.count()        
    entregables = Entregable.objects.all()
    c_entregables = entregables.count()        
    user = request.user.id
    if user is not None:
        dashboard_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request , "index.html", {"url": avatares[0].imagen.url, "c_cursos": c_cursos,
                                "c_alumnos": c_alumnos, "c_profesores": c_profesores, "c_entregables": c_entregables,
                                                    "dashboard_seleccionado": dashboard_seleccionado})
    return render(request, "index.html", {"c_cursos": c_cursos, "c_alumnos": c_alumnos, "c_profesores": c_profesores,
                                        "c_entregables": c_entregables})
    

# -------------------------------------------------------------------------------------------------
# VIEWS DE CURSO
# -------------------------------------------------------------------------------------------------
#@login_required
def ver_cursos(request):
    cursos = Curso.objects.all()
    user = request.user.id
    if user is not None:
        curso_seleccionado = True   
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "cursos.html", {"url": avatares[0].imagen.url, "cursos": cursos,
                                                "curso_seleccionado": curso_seleccionado})
    return render(request, "cursos.html", {"cursos": cursos})


def curso_formulario(request):
    if request.method == "POST":
        mi_formulario = Curso_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso = Curso(nombre=datos["nombre"], camada=datos["camada"])
            curso.save()
            avatares = Avatar.objects.filter(user=request.user.id)
            return render(request, "frm_curso.html", {"url": avatares[0].imagen.url})
    curso_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "frm_curso.html", {"url": avatares[0].imagen.url, "curso_seleccionado": curso_seleccionado})


def confirma_eliminar_curso(request, id):
    curso = Curso.objects.get(id=id)
    return render(request, "eliminar_curso.html", {"cursos": curso})


def eliminar_curso(request, id):
    curso = Curso.objects.get(id=id)
    curso.delete()
    curso = Curso.objects.all()
    curso_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)    
    return render(request, "cursos.html", {"url": avatares[0].imagen.url, "cursos": curso,
                                        "curso_seleccionado": curso_seleccionado})


def editar_curso(request, id):
    curso_seleccionado = True   
    avatares = Avatar.objects.filter(user=request.user.id)
    curso = Curso.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Curso_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos["nombre"]
            curso.camada = datos["camada"]
            curso.save()
            cursos = Curso.objects.all()
            return render(request, "cursos.html", {"url": avatares[0].imagen.url, "cursos": cursos,
                                                "curso_seleccionado": curso_seleccionado})
    else:
        mi_formulario = Curso_formulario(initial={"nombre": curso.nombre, "camada": curso.camada})
    return render(request, "editar_curso.html", {"url": avatares[0].imagen.url, "mi_formulario": mi_formulario,
                                                "curso": curso, "curso_seleccionado": curso_seleccionado})


def buscar_curso(request):
    user = request.user.id
    if user is not None:
        curso_seleccionado = True   
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "buscar_curso.html", {"url": avatares[0].imagen.url,
                                                    "curso_seleccionado": curso_seleccionado})
    return render(request, "buscar_curso.html")


def buscar(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        cursos = Curso.objects.filter(nombre__icontains= nombre)
        user = request.user.id
        if user is not None:
            curso_seleccionado = True   
            avatares = Avatar.objects.filter(user=request.user.id)
            return render(request, "rb_curso.html", {"url": avatares[0].imagen.url, "cursos": cursos,
                                                    "curso_seleccionado": curso_seleccionado})
        return render( request, "rb_curso.html", {"cursos": cursos})
    else:
        return HttpResponse("Ingrese el nombre del curso")


# -------------------------------------------------------------------------------------------------
# VIEWS DE ALUMNO
# -------------------------------------------------------------------------------------------------
#@login_required
def ver_alumnos(request):
    alumnos = Alumno.objects.all()
    user = request.user.id
    if user is not None:       
        alumno_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "alumnos.html", {"url": avatares[0].imagen.url, "alumnos": alumnos,
                                                "alumno_seleccionado": alumno_seleccionado})
    return render(request, "alumnos.html", {"alumnos": alumnos})


def alumno_formulario(request):
    alumno_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == "POST":
        mi_formulario = Alumno_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            alumno = Alumno(apellido=datos["apellido"], nombre=datos["nombre"], fecha_nac=datos["fecha_nac"],
                            dni=datos["dni"], mail=datos["mail"])
            alumno.save()
            return render(request, "frm_alumno.html", {"url": avatares[0].imagen.url,
                                                    "alumno_seleccionado": alumno_seleccionado})
    return render(request, "frm_alumno.html", {"url": avatares[0].imagen.url,
                                            "alumno_seleccionado": alumno_seleccionado})


def eliminar_alumno(request, id):
    alumno = Alumno.objects.get(id=id)
    alumno.delete()
    alumno = Alumno.objects.all()
    alumno_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "alumnos.html", {"url": avatares[0].imagen.url, "alumno_seleccionado": alumno_seleccionado,
                                            "alumnos":alumno})


def editar_alumno(request, id):
    alumno_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    alumno = Alumno.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Alumno_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            alumno.apellido = datos["apellido"]
            alumno.nombre = datos["nombre"]
            alumno.fecha_nac = datos["fecha_nac"]
            alumno.dni = datos["dni"]
            alumno.mail = datos["mail"]
            alumno.save()
            alumnos = Alumno.objects.all()
            return render(request, "alumnos.html", {"url": avatares[0].imagen.url, "alumnos": alumnos,
                                                    "alumno_seleccionado": alumno_seleccionado})
    else:
        mi_formulario = Alumno_formulario(initial={"apellido": alumno.apellido, "nombre": alumno.nombre,
                                                "fecha_nac": alumno.fecha_nac, "dni": alumno.dni, "mail": alumno.mail})
    return render(request, "editar_alumno.html", {"url": avatares[0].imagen.url, "mi_formulario": mi_formulario,
                                                "alumno": alumno, "alumno_seleccionado": alumno_seleccionado})


def buscar_alumno(request):
    user=request.user.id
    if user is not None:
        alumno_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request , "buscar_alumno.html", {"url": avatares[0].imagen.url,
                                                    "alumno_seleccionado": alumno_seleccionado})
    return render(request , "buscar_alumno.html")


def buscara(request):
    if request.GET["apellido"]:
        apellido = request.GET["apellido"]
        alumnos = Alumno.objects.filter(apellido__icontains= apellido)
        user=request.user.id
        if user is not None:
            alumno_seleccionado = True
            avatares = Avatar.objects.filter(user=request.user.id)
            return render(request , "rb_alumno.html", {"url": avatares[0].imagen.url, "alumnos": alumnos,
                                                    "alumno_seleccionado": alumno_seleccionado})
        return render(request, "rb_alumno.html", {"alumnos": alumnos})
    else:
        return HttpResponse("Ingrese el nombre del alumno")


# -------------------------------------------------------------------------------------------------
# VIEWS DE PROFESOR
# -------------------------------------------------------------------------------------------------
#@login_required
def ver_profesores(request):
    profesores = Profesor.objects.all()
    user = request.user.id
    if user is not None:
        profesor_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "profesores.html", {"url": avatares[0].imagen.url, "profesores": profesores,
                                                "profesor_seleccionado": profesor_seleccionado})
    return render(request, "profesores.html", {"profesores": profesores})


def profesor_formulario(request):
    profesor_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == "POST":
        mi_formulario = Profesor_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            profesor = Profesor(apellido=datos["apellido"], nombre=datos["nombre"], mail=datos["mail"],
                                profesion=datos["profesion"])
            profesor.save()
            return render(request, "frm_profesor.html", {"url": avatares[0].imagen.url, "profesor": profesor,
                                                    "profesor_seleccionado": profesor_seleccionado})
    return render(request, "frm_profesor.html", {"url": avatares[0].imagen.url,
                                                "profesor_seleccionado": profesor_seleccionado})


def eliminar_profesor(request, id):
    profesor = Profesor.objects.get(id=id)
    profesor.delete()
    profesor = Profesor.objects.all()
    return render(request, "profesores.html", {"profesores": profesor})


def editar_profesor(request, id):
    profesor_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    profesor = Profesor.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Profesor_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            profesor.apellido = datos["apellido"]
            profesor.nombre = datos["nombre"]
            profesor.mail = datos["mail"]
            profesor.profesion = datos["profesion"]
            profesor.save()
            profesores = Profesor.objects.all()
            return render(request, "profesores.html", {"url": avatares[0].imagen.url, "profesores": profesores,
                                                    "profesor_seleccionado": profesor_seleccionado})
    else:
        mi_formulario = Profesor_formulario(initial={"apellido": profesor.apellido, "nombre": profesor.nombre,
                                                    "mail": profesor.mail, "profesion": profesor.profesion})
    return render(request, "editar_profesor.html", {"url": avatares[0].imagen.url, "mi_formulario": mi_formulario,
                                                "profesor": profesor, "profesor_seleccionado": profesor_seleccionado})


def buscar_profesor(request):
    user = request.user.id
    if user is not None:
        profesor_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "buscar_profesor.html", {"url": avatares[0].imagen.url,
                                                        "profesor_seleccionado": profesor_seleccionado})
    return render(request, "buscar_profesor.html")


def buscarp(request):
    if request.GET["apellido"]:
        apellido = request.GET["apellido"]
        profesores = Profesor.objects.filter(apellido__icontains= apellido)
        user = request.user.id
        if user is not None:
            profesor_seleccionado = True
            avatares = Avatar.objects.filter(user=request.user.id)
            return render(request, "rb_profesor.html", {"url": avatares[0].imagen.url, "profesores": profesores,
                                                        "profesor_seleccionado": profesor_seleccionado})
        return render( request, "rb_profesor.html", {"profesores": profesores})
    else:
        return HttpResponse("Ingrese el nombre del alumno")


# -------------------------------------------------------------------------------------------------
# VIEWS DE ENTREGABLE
# -------------------------------------------------------------------------------------------------
#@login_required
def ver_entregables(request):
    entregables = Entregable.objects.all()
    user = request.user.id
    if user is not None:
        entregable_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request , "entregables.html", {"url": avatares[0].imagen.url, "entregables": entregables,
                                                    "entregable_seleccionado": entregable_seleccionado})
    return render(request, "entregables.html", {"entregables": entregables})


def entregable_formulario(request):
    entregable_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == "POST":
        mi_formulario = Entregable_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            entregable = Entregable(nombre=datos["nombre"], fecha_entrega=datos["fecha_entrega"],
                                    entregado=datos["entregado"])
            entregable.save()
            return render(request, "frm_entregable.html", {"url": avatares[0].imagen.url, "entregable": entregable,
                                                    "entregable_seleccionado": entregable_seleccionado})
    return render(request, "frm_entregable.html", {"url": avatares[0].imagen.url,
                                            "entregable_seleccionado": entregable_seleccionado})


def eliminar_entregable(request, id):
    entregable = Entregable.objects.get(id=id)
    entregable.delete()
    entregable = Entregable.objects.all()
    return render(request, "entregables.html", {"entregables": entregable})


def editar_entregable(request, id):
    entregable_seleccionado = True
    avatares = Avatar.objects.filter(user=request.user.id)
    entregable = Entregable.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Entregable_formulario(request.POST)
        if mi_formulario.is_valid():
            print('valid true')
            datos = mi_formulario.cleaned_data
            entregable.nombre = datos["nombre"]
            entregable.fecha_entrega = datos["fecha_entrega"]
            entregable.entregado = datos["entregado"]
            print(entregable.entregado)
            entregable.save()
            entregables = Entregable.objects.all()
            return render(request, "entregables.html", {"url": avatares[0].imagen.url, "entregables": entregables,
                                                        "entregable_seleccionado": entregable_seleccionado})
        else:
            print(mi_formulario.errors)
    else:
        mi_formulario = Entregable_formulario(initial={"nombre": entregable.nombre,
                                    "fecha_entrega": entregable.fecha_entrega, "entregado": entregable.entregado})
    return render(request, "editar_entregable.html", {"url": avatares[0].imagen.url, "mi_formulario": mi_formulario,
                                        "entregable": entregable, "entregable_seleccionado": entregable_seleccionado})


def buscar_entregable(request):
    user = request.user.id
    if user is not None:
        entregable_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "buscar_entregable.html", {"url": avatares[0].imagen.url,
                                                        "entregable_seleccionado": entregable_seleccionado})
    return render(request, "buscar_entregable.html")


def buscare(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        entregables = Entregable.objects.filter(nombre__icontains= nombre)
        entregable_seleccionado = True
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, "rb_entregable.html", {"url": avatares[0].imagen.url, "entregables": entregables,
                                                    "entregable_seleccionado": entregable_seleccionado})
    else:
        return HttpResponse("Ingrese el nombre del entregable")
