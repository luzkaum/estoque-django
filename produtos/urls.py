from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),
    path('novo/', views.criar_produto, name='criar_produto'),
    path('<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    path('<int:pk>/apagar/', views.deletar_produto, name='deletar_produto'),
    path('login/', auth_views.LoginView.as_view(template_name='produtos/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('relatorio/', views.relatorio, name='relatorio'),
]