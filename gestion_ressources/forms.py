from django import forms
from .models import Demande

class DemandeForm(forms.ModelForm):
    class Meta:
        model = Demande
        # Champs que l'utilisateur peut remplir lors de la création
        fields = ['type_demande', 'date_debut', 'date_fin', 'motif']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}), # Utiliser le widget date HTML5
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        if date_debut and date_fin:
            if date_fin < date_debut:
                raise forms.ValidationError("La date de fin ne peut pas être antérieure à la date de début.")
        return cleaned_data

# Optionnel: Formulaire pour le commentaire de rejet (pourrait être intégré dans la vue admin)
class RejetCommentaireForm(forms.Form):
     commentaire = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Motif du rejet", required=True)