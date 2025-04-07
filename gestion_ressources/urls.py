from django.urls import path
from . import views

app_name = 'gestion_ressources' # Pour les noms d'URL (namespace)

urlpatterns = [
    # Tableau de bord principal (différent pour employé et admin)
    path('', views.tableau_de_board, name='tableau_de_bord'),

    # Création d'une nouvelle demande
    path('demande/nouvelle/', views.creer_demande, name='creer_demande'),

    # Vue détaillée d'une demande (pour l'impression par exemple)
    path('demande/<int:pk>/', views.detail_demande, name='detail_demande'),

    # Actions pour le super utilisateur
    path('demande/<int:pk>/approuver/', views.approuver_demande, name='approuver_demande'),
    path('demande/<int:pk>/rejeter/', views.rejeter_demande, name='rejeter_demande'),

    # Page d'impression
    path('demande/<int:pk>/imprimer/', views.imprimer_demande, name='imprimer_demande'),
]
