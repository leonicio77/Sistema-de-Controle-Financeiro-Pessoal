
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')

        return email
    

from .models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        labels = {
            'nome': 'Nome da categoria'
        }


from .models import Lancamento


class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = ['descricao', 'valor', 'data', 'tipo', 'categoria']

        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'valor': forms.NumberInput(
                attrs={'step': '0.01', 'min': '0.01'}
            ),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['data'].input_formats = ['%Y-%m-%d']

        if usuario is not None:
            self.fields['categoria'].queryset = Categoria.objects.filter(
                usuario=usuario
            )
        else:
            self.fields['categoria'].queryset = Categoria.objects.none()


