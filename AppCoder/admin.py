from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'camada')
    ordering = ('nombre',)
#    list_editable = ('nombre')
    search_fields = ('nombre', 'camada')
    list_filter = ('nombre',)
    list_per_page = 10


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'fecha_nac', 'dni', 'mail')
    ordering = ('apellido',)
    search_fields = ('apellido', 'nombre', 'dni')
    list_filter = ('apellido', 'nombre')
    list_per_page = 10


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'mail', 'profesion')
    ordering = ('apellido',)
    search_fields = ('apellido', 'nombre', 'profesion')
    list_filter = ('profesion',)
    list_per_page = 10


@admin.register(Entregable)
class EntregableAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_entrega', 'entregado')
    ordering = ('fecha_entrega',)
    search_fields = ('nombre',)
    list_filter = ('nombre', 'fecha_entrega', 'entregado')
    list_per_page = 10


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'imagen')
    ordering = ('user',)
    list_filter = ('user',)
    list_per_page = 10

