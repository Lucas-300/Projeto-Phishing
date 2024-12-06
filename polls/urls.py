from django.urls import path
from .views import index_func, funcionalidades  # Importando a função funcionalidades
from . import views
from polls.views import index_func




urlpatterns = [
     path('', index_func, name='index'),
    #path('', views.index_func, name='index'),  # Página inicial
    path('funcionalidades/', views.funcionalidades, name='funcionalidades'),  # Página de funcionalidades
]
