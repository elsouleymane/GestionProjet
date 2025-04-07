# gestion_ressources/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Demande(models.Model):
    TYPE_DEMANDE_CHOICES = [
        ('CONGE', 'Congé'),
        ('ABSENCE', 'Absence'),
        ('MISSION', 'Mission'),
    ]

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVEE', 'Approuvée'),
        ('REJETEE', 'Rejetée'),
    ]

    # Qui fait la demande
    demandeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes')
    # Type de demande
    type_demande = models.CharField(max_length=10, choices=TYPE_DEMANDE_CHOICES)
    # Dates
    date_debut = models.DateField()
    date_fin = models.DateField()
    # Détails
    motif = models.TextField(blank=True, null=True) # Raison de la demande
    # Suivi
    date_soumission = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='EN_ATTENTE')
    # Traitement par le super utilisateur/manager
    traitee_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_traitees')
    date_traitement = models.DateTimeField(null=True, blank=True)
    commentaire_approbateur = models.TextField(blank=True, null=True) # Commentaires lors de l'approbation/rejet

    def __str__(self):
        return f"{self.get_type_demande_display()} de {self.demandeur.username} du {self.date_debut} au {self.date_fin} ({self.get_statut_display()})"

    class Meta:
        ordering = ['-date_soumission'] # Ordonner par date de soumission décroissante
