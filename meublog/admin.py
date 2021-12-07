from django.contrib import admin
from .models import Post,Comentario

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'autor', 'data_publicacao', 'status')
    list_filter = ('status', 'data_criacao', 'data_publicacao', 'autor')
    search_fields = ('titulo', 'corpo')
    preopopulated_fields = {'slug':('titulo',)}
    #raw_id_fields = ('autor')
    date_hierarchy = 'data_publicacao'
    ordering = ('status', '-data_publicacao')
    
    
@admin.register(Comentario) 
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('post', 'nome', 'email', 'ativo',)
    list_filter = ('data_criacao', 'ativo',)
    ordering = ('post', 'ativo', 'data_criacao',)
    
    