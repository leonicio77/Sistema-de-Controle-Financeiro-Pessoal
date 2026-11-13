
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
]
