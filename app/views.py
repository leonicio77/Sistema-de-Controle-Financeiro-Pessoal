from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import CadastroUsuarioForm, CategoriaForm
from .models import Categoria


def cadastro(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'cadastro.html', {'form': form})


from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def categorias(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)

        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()

            return redirect('categorias')
    else:
        form = CategoriaForm()

    lista_categorias = Categoria.objects.filter(
        usuario=request.user
    ).order_by('nome')

    return render(request, 'categorias.html', {
        'form': form,
        'categorias': lista_categorias
    })


@login_required(login_url='login')
@require_POST
def excluir_categoria(request, id):
    categoria = get_object_or_404(
        Categoria,
        id=id,
        usuario=request.user
    )

    if not categoria.lancamento_set.exists():
        categoria.delete()

    return redirect('categorias')


