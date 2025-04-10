from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Demande
from .forms import DemandeForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm  # Ajoutez cet import
from django.contrib.auth.models import User  # Ajoutez cet import pour la vue liste_employes


def accueil(request):
    """
    Vue d'accueil qui redirige vers le tableau de bord approprié si l'utilisateur est connecté
    ou affiche une page de bienvenue s'il n'est pas connecté
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Rediriger vers le tableau de bord admin
            return redirect('gestion_ressources:tableau_de_bord')
        else:
            # Rediriger vers le tableau de bord employé
            return redirect('gestion_ressources:tableau_de_bord')
    else:
        # Afficher la page de bienvenue
        return render(request, 'gestion_ressources/bienvenue.html')
    
# --- Fonctions utilitaires ---
def is_superuser(user):
    return user.is_superuser

# --- Vues ---

@login_required
def tableau_de_bord(request):
    if request.user.is_superuser:
        # Vue Admin : Voir toutes les demandes en attente et les demandes traitées récemment
        demandes_en_attente = Demande.objects.filter(statut='EN_ATTENTE').order_by('date_soumission')
        demandes_traitees = Demande.objects.exclude(statut='EN_ATTENTE').order_by('-date_traitement')[:10] # 10 dernières traitées
        context = {
            'demandes_en_attente': demandes_en_attente,
            'demandes_traitees': demandes_traitees,
        }
        return render(request, 'gestion_ressources/dashboard_admin.html', context)
    else:
        # Vue Employé : Voir ses propres demandes
        demandes_utilisateur = Demande.objects.filter(demandeur=request.user).order_by('-date_soumission')
        context = {
            'demandes': demandes_utilisateur,
        }
        return render(request, 'gestion_ressources/dashboard_employee.html', context)

@login_required
def creer_demande(request):
    if request.method == 'POST':
        form = DemandeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.demandeur = request.user
            demande.statut = 'EN_ATTENTE' # Statut initial
            demande.save()
            messages.success(request, 'Votre demande a été soumise avec succès.')
            return redirect('gestion_ressources:tableau_de_bord')
        else:
             messages.error(request, 'Erreur dans le formulaire. Veuillez corriger les erreurs.')
    else:
        form = DemandeForm()

    context = {'form': form}
    return render(request, 'gestion_ressources/demande_form.html', context)

@login_required
def detail_demande(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    # Sécurité : L'employé ne peut voir que ses demandes, l'admin peut tout voir
    if not request.user.is_superuser and demande.demandeur != request.user:
        messages.error(request, "Vous n'avez pas la permission de voir cette demande.")
        return redirect('gestion_ressources:tableau_de_bord')

    context = {'demande': demande}
    return render(request, 'gestion_ressources/detail_demande.html', context)

# --- Vues réservées au Super Utilisateur ---

@login_required
@user_passes_test(is_superuser, login_url='/comptes/login/') # Redirige si pas superuser
def approuver_demande(request, pk):
    if request.method == 'POST': # Utiliser POST pour les actions qui modifient l'état
        demande = get_object_or_404(Demande, pk=pk, statut='EN_ATTENTE')
        # Ajouter un champ pour le commentaire dans le template si besoin
        commentaire = request.POST.get('commentaire', '') # Récupérer commentaire du POST si formulaire ajouté

        demande.statut = 'APPROUVEE'
        demande.traitee_par = request.user
        demande.date_traitement = timezone.now()
        demande.commentaire_approbateur = commentaire
        demande.save()
        messages.success(request, f"La demande {demande.id} a été approuvée.")
        # TODO: Envoyer une notification à l'employé (optionnel)
    else:
        messages.warning(request, "Utilisez le bouton prévu pour cette action.")

    return redirect('gestion_ressources:tableau_de_bord')


@login_required
@user_passes_test(is_superuser, login_url='/comptes/login/')
def rejeter_demande(request, pk):
    if request.method == 'POST':
        demande = get_object_or_404(Demande, pk=pk, statut='EN_ATTENTE')
        # Il est fortement recommandé d'ajouter un champ 'commentaire' obligatoire pour le rejet
        commentaire = request.POST.get('commentaire', '') # Récupérer du POST
        if not commentaire:
             messages.error(request, "Un commentaire est requis pour rejeter une demande.")
             # Rediriger vers une page de confirmation de rejet avec formulaire ? Ou retour tableau de bord.
             return redirect('gestion_ressources:tableau_de_bord') # Simplifié ici

        demande.statut = 'REJETEE'
        demande.traitee_par = request.user
        demande.date_traitement = timezone.now()
        demande.commentaire_approbateur = commentaire
        demande.save()
        messages.success(request, f"La demande {demande.id} a été rejetée.")
        # TODO: Envoyer une notification à l'employé (optionnel)
    else:
        messages.warning(request, "Utilisez le bouton prévu pour cette action.")

    return redirect('gestion_ressources:tableau_de_bord')

# --- Vue pour l'impression ---

@login_required
def imprimer_demande(request, pk):
    demande = get_object_or_404(Demande, pk=pk)
    # Vérifier si la demande est traitée et si l'utilisateur a le droit de la voir/imprimer
    if demande.statut == 'EN_ATTENTE':
         messages.error(request, "Cette demande n'a pas encore été traitée.")
         return redirect('gestion_ressources:detail_demande', pk=pk)

    if not request.user.is_superuser and demande.demandeur != request.user:
        messages.error(request, "Vous n'avez pas la permission d'imprimer cette demande.")
        return redirect('gestion_ressources:tableau_de_bord')

    context = {'demande': demande}
    # Utilise un template spécifique pour l'impression, sans menus, etc.
    return render(request, 'gestion_ressources/demande_print.html', context)

def logout_view(request):
    """
    Vue simplifiée de déconnexion qui fonctionne avec GET
    """
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    from django.contrib import messages
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('accueil')

@login_required
@user_passes_test(is_superuser)
def creer_employe(request):
    """
    Vue permettant aux administrateurs de créer des comptes employés
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Compte employé {user.username} créé avec succès.')
            return redirect('gestion_ressources:liste_employes')
    else:
        form = UserCreationForm()
    
    return render(request, 'gestion_ressources/creer_employe.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def liste_employes(request):
    """
    Vue pour afficher la liste des employés (admin uniquement)
    """
    employes = User.objects.filter(is_superuser=False)
    return render(request, 'gestion_ressources/liste_employes.html', {'employes': employes})