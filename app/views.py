from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum
from decimal import Decimal

from .models import Categoria, Lancamento
from .forms import CadastroUsuarioForm, CategoriaForm, LancamentoForm


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
    lancamentos = Lancamento.objects.filter(
        usuario=request.user
    )

    total_receitas = lancamentos.filter(
        tipo='receita'
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

    total_despesas = lancamentos.filter(
        tipo='despesa'
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

    saldo = total_receitas - total_despesas

    return render(request, 'dashboard.html', {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
    })



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



@login_required(login_url='login')
def lancamentos(request):
    if request.method == 'POST':
        form = LancamentoForm(
            request.POST,
            usuario=request.user
        )

        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.usuario = request.user
            lancamento.save()
            return redirect('lancamentos')
    else:
        form = LancamentoForm(usuario=request.user)

    lista_lancamentos = Lancamento.objects.filter(
        usuario=request.user
    )

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if data_inicio:
        lista_lancamentos = lista_lancamentos.filter(
            data__gte=data_inicio
        )

    if data_fim:
        lista_lancamentos = lista_lancamentos.filter(
            data__lte=data_fim
        )

    total_receitas = lista_lancamentos.filter(
        tipo='receita'
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

    total_despesas = lista_lancamentos.filter(
        tipo='despesa'
    ).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')

    saldo = total_receitas - total_despesas

    lista_lancamentos = lista_lancamentos.order_by('-data', '-id')

    return render(request, 'lancamentos.html', {
        'form': form,
        'lancamentos': lista_lancamentos,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    })



@login_required(login_url='login')
def editar_lancamento(request, id):
    lancamento = get_object_or_404(
        Lancamento,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        form = LancamentoForm(
            request.POST,
            instance=lancamento,
            usuario=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('lancamentos')
    else:
        form = LancamentoForm(
            instance=lancamento,
            usuario=request.user
        )

    return render(request, 'editar_lancamento.html', {
        'form': form,
        'lancamento': lancamento
    })


@login_required(login_url='login')
@require_POST
def excluir_lancamento(request, id):
    lancamento = get_object_or_404(
        Lancamento,
        id=id,
        usuario=request.user
    )

    lancamento.delete()

    return redirect('lancamentos')




