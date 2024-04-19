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
    
#admin.site.register(Curso)
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Entregable)
admin.site.register(Avatar)
