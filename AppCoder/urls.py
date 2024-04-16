from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.inicio, name="home"),
    path("dashborad", views.dashboard, name="dashboard"),
    path("buscarc", views.buscarc),
    # urls de LOGIN
    path("login", views.login_request, name="login"),
    path("register", views.register, name="registro"),
    path("editarPerfil", views.editarPerfil, name="EditarPerfil"),
    #path("cambiarContrasenia", views.CambiarContrasenia.as_view(), name="CambiarContrasenia"),
    path("logout", LogoutView.as_view(template_name="logout.html"), name="LogOut"),
    # urls de CURSOS
    path("ver_cursos", views.ver_cursos, name="cursos"),
    path("alta_curso", views.curso_formulario, name="alta"),
    path("buscar_curso", views.buscar_curso, name="bus_curso"),
    path("buscar", views.buscar),
    path("eliminar_curso/<int:id>", views.eliminar_curso, name="eliminar_curso"),
    path("confirma_eliminar_curso/<int:id>", views.confirma_eliminar_curso, name="c_eliminar_curso"),
    path("editar_curso/<int:id>", views.editar_curso, name="editar_curso"),
    # urls de ALUMNOS
    path("ver_alumnos", views.ver_alumnos, name="alumnos"),
    path("alta_alumno", views.alumno_formulario, name="alta_alumno"),
    path("buscar_alumno", views.buscar_alumno, name="bus_alumno"),
    path("buscara", views.buscara),
    path("eliminar_alumno/<int:id>", views.eliminar_alumno, name="eliminar_alumno"),
    path("editar_alumno/<int:id>", views.editar_alumno, name="editar_alumno"),
    # urls de PROFESORES
    path("ver_profesores", views.ver_profesores, name="profesores"),
    path("alta_profesor", views.profesor_formulario, name="alta_profesor"),
    path("buscar_profesor", views.buscar_profesor, name="bus_profesor"),
    path("buscarp", views.buscarp),
    path("eliminar_profesor/<int:id>", views.eliminar_profesor, name="eliminar_profesor"),
    path("editar_profesor/<int:id>", views.editar_profesor, name="editar_profesor"),
    # urls de ENTREGABLES
    path("ver_entregables", views.ver_entregables, name="entregables"),
    path("alta_entregable", views.entregable_formulario, name="alta_entregable"),
    path("buscar_entregable", views.buscar_entregable, name="bus_entregable"),
    path("buscare", views.buscare),
    path("eliminar_entregable/<int:id>", views.eliminar_entregable, name="eliminar_entregable"),
    path("editar_entregable/<int:id>", views.editar_entregable, name="editar_entregable")    
]
