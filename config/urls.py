
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('cadastro/', views.cadastro, name='cadastro'),

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('categorias/', views.categorias, name='categorias'),

    path(
        'categorias/excluir/<int:id>/',
        views.excluir_categoria,
        name='excluir_categoria'
    ),

    path('lancamentos/', views.lancamentos, name='lancamentos'),

    path(
        'lancamentos/editar/<int:id>/',
        views.editar_lancamento,
        name='editar_lancamento'
    ),

    path(
        'lancamentos/excluir/<int:id>/',
        views.excluir_lancamento,
        name='excluir_lancamento'
    ),

    # RF16 - Contas a pagar e receber
    path('contas/', views.contas, name='contas'),

    path(
        'contas/concluir/<int:id>/',
        views.concluir_conta,
        name='concluir_conta'
    ),

    path(
        'contas/excluir/<int:id>/',
        views.excluir_conta,
        name='excluir_conta'
    ),
]
