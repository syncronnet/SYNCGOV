
#from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from SYNCGOV import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name="index"),
    path('login', views.logar, name="login"),
    path('sair', views.sair, name="sair"),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('home', views.home, name="home"),
    path('principal/', views.principal, name="principal"),
    path('principal/populacao.html', views.populacao_view, name='populacao'),
     
    
    #path('adm', views.adm, name="adm"),
    
]
  
   
  