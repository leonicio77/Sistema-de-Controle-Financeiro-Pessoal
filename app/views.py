
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CadastroUsuarioForm


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

