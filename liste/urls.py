from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('habitat/', views.habitat, name='habitat'),
    path('animaux/', views.animaux, name='animaux'),
    path('service/', views.service, name='service'),
    path('rapport/', views.rapport, name='rapport'),  # protégé par @login_required
    path('admin/', admin.site.urls),
    path('avis/', views.avis, name='avis_page'),
    path('contact/', views.contact, name='contact'),
    path('avis_visibles/', views.avis_visible, name='avis_visibles'),
    path('submit_avis/', views.submit_avis, name='submit_avis'),
    path('animal/<int:animal_id>/click/', views.increment_click, name='increment_click'),
    path('login1/', auth_views.LoginView.as_view(template_name='liste/login1.html'), name='login1'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    

    path('validation_avis/<int:avis_id>/', views.valider_avis, name='valider_avis'),#  nom de la vue de la page de validation d'avis
]
