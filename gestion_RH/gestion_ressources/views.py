from django.shortcuts import render, get_object_or_404
from .models import Demande

def imprimer_demande(request, demande_id):
    """
    Vue pour l'impression d'une demande spécifique
    """
    demande = get_object_or_404(Demande, id=demande_id)
    return render(request, 'gestion_ressources/imprimer_demande.html', {
        'demande': demande
    })