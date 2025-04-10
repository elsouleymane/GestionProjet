from django.urls import path
from . import views

app_name = 'gestion_ressources'

urlpatterns = [
    path('', views.tableau_de_bord, name='tableau_de_bord'),
    path('demande/creer/', views.creer_demande, name='creer_demande'),
    path('demande/<int:pk>/', views.detail_demande, name='detail_demande'),
    path('demande/<int:pk>/approuver/', views.approuver_demande, name='approuver_demande'),
    path('demande/<int:pk>/rejeter/', views.rejeter_demande, name='rejeter_demande'),
    # Nouvelles URLs pour la gestion des employés
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/creer/', views.creer_employe, name='creer_employe'),
]