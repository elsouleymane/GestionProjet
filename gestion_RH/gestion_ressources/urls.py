from django.urls import path
from . import views

urlpatterns = [
    path('demande/<int:demande_id>/imprimer/', views.imprimer_demande, name='imprimer_demande'),
]