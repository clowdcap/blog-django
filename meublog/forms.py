from django import forms
from django.core.mail import EmailMessage

from meublog.models import Comentario



class EmailPost(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    destino = forms.EmailField()
    comentario = forms.CharField(required=False,
                                 widget=forms.Textarea)
    
    def enviar_email(self, meupost):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        destino = self.cleaned_data['destino']
        comentario = self.cleaned_data['comentario']
        
        conteudo = f'Recomendo ler o post: {meupost.titulo}\n'\
                f"Comentarios: {comentario}"
        mail = EmailMessage(
            subject=f"Recomendo esse post",
            body = conteudo,
            from_email='contato@meublog.com.br',
            to=[destino, ],
            headers={'Reply-to': email},
        )
        mail.send()


class ComentarioModelForm(forms.ModelForm):
    
    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'corpo']
        
    def salvar_comentario(self, post):
        novo_comentario = self.save(commit=False)
        novo_comentario.post = post
        novo_comentario.nome = self.cleaned_data['nome']
        novo_comentario.email = self.cleaned_data['email']
        novo_comentario.corpo = self.cleaned_data['corpo']
        return novo_comentario.save()


