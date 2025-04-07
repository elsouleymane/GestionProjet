from django.contrib import admin
from .models import Demande

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('demandeur', 'type_demande', 'date_debut', 'date_fin', 'statut', 'date_soumission', 'traitee_par')
    list_filter = ('statut', 'type_demande', 'demandeur')
    search_fields = ('demandeur__username', 'motif')
    # Rendre certains champs en lecture seule dans l'admin une fois la demande créée
    readonly_fields = ('demandeur', 'date_soumission')

    # Optionnel : Actions personnalisées dans l'admin (ex: approuver/rejeter en masse)
    # def approve_requests(modeladmin, request, queryset):
    #     queryset.update(statut='APPROUVEE', traitee_par=request.user, date_traitement=timezone.now())
    # approve_requests.short_description = "Approuver les demandes sélectionnées"

    # def reject_requests(modeladmin, request, queryset):
    #     queryset.update(statut='REJETEE', traitee_par=request.user, date_traitement=timezone.now())
    # reject_requests.short_description = "Rejeter les demandes sélectionnées"

    # actions = [approve_requests, reject_requests]


# Register your models here.
