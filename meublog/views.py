'''from django.forms.fields import EmailField
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView 
'''
from django.contrib import messages
from django.urls import reverse_lazy 
from .forms import ComentarioModelForm, EmailPost
from .models import Post, Comentario
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.shortcuts import redirect


# Create your views here.

class ListarPostsView(ListView):
    queryset = Post.publicados.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = "meublog/post/listarposts.html"


class DetalharPostView(DetailView):
    template_name = "meublog/post/detalharpost.html"
    model = Post
    
    def _get_coments(self, id_post):
        try:
            return Comentario.objects.filter(post_id=id_post)
        except Comentario.DoesNotExist:
            raise Exception
        
    def _get_context_data(self, **kwargs):
        contexto = super(DetalharPostView, self).get_context_data(**kwargs)
        contexto['comentario'] = self._get_coments(self.object.id)
        return contexto
    
    
class FormContatoView(FormView):
    template_name = "meublog/post/sharepost.html"
    form_class = EmailPost
    sucess_url = reverse_lazy('meublog:listar_posts')
    
    def get_post(self, id_post):
        try:
            return Post.publicados.get(pk=id_post)
        except Post.DoesNotExist:
            messages.error(self.request, 'O post nao existe!')
            reverse_lazy('meublog:listar_posts')

    def get_context_data(self, **kwargs):
        contexto = super(FormContatoView, self).get_context_data(**kwargs)
        contexto['post'] = self.get_post(self.kwargs['pk'])
        return contexto
        
    def form_valid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        form.enviar_email(meupost)
        messages.success(self.request,f'Post {meupost.titulo} enviado com sucesso.')
        return super(FormContatoView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        messages.error(self.request, f'Post {meupost.titulo} '
                                       f'não enviado.')
        return super(FormContatoView, self).form_invalid(form, *args, **kwargs)


class ComentarioView(CreateView):
    template_name = 'meublog/post/comentarios.html'
    form_class = ComentarioModelForm
    
    def _get_post(self, id_post):
        try:
            post = Post.publicados.get(pk=id_post)
            return post
        except Post.DoesNotExist:
            raise Exception
        
    def get_context_data(self, **kwargs):
        contexto = super(ComentarioView, self).get_context_data(**kwargs)
        contexto['post'] = self._get_post(self.kwargs['pk'])
        return contexto
    
    
    def form_valid(self, form, **kwargs):
        post = self._get_post(self.kwargs['pk'])
        form.salvar_comentario(post)
        return redirect('meublog:detalhar', post.slug)
