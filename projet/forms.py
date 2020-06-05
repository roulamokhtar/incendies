from django import forms
from .models import Projet, ObjectifSpecifique,Resultat , Action,Indicateurdeclinaison,Reboisement,Reboisementphysique,Reboisementfinancier
from django.forms import ModelForm
class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ('titre','objectifglobal','justification','commune','lieu_dit','superficie_zone','menage','population','duree','annee')
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'objectifglobal': forms.Select(attrs={'class': 'myfieldclass'}),
            'justification': forms.Textarea(attrs={'class': 'myfieldclassArea'}),
            'lieu_dit': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'superficie_zone': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'menage': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'population': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'duree': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'annee': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
        }

class IndicateurdeclinaisonForm(forms.ModelForm):
    class Meta:
        model = Indicateurdeclinaison
        fields = ('name' ,'resultat_id','ciblle_2035','unite','quinquennat1','quinquennat2','quinquennat3','quinquennat4'  )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'resultat_id': forms.Select(attrs={'class': 'myfieldclass'}),
            'ciblle_2035': forms.TextInput(attrs={'class': 'myfieldclassArea'}),
            'unite': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'quinquennat1': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'quinquennat2': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'quinquennat3': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'quinquennat4': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
         }
    
class ActionForm(ModelForm):
    class Meta:
        model = Action
     # geom = models.GeometryCollectionField(srid=4326)
    # projet = models.ForeignKey(Projets, on_delete =models.CASCADE)
    
        fields = ('name','volume','montant','source_financement','duree'     )

class ObjectifSpecifiqueForm(ModelForm):
    class Meta:
        model=ObjectifSpecifique
        fields =['name',]

class ReboisementForm(forms.ModelForm):
    class Meta:
        model = Reboisement
        fields = ('name','layer','kml_folder','commune','cantons','volume_pre','montant_ma','besoins_pl','duree'  )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'myfieldclass'}),
            'layer': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'kml_folder': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'commune': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'cantons': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'volume_pre': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'montant_ma': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),

            'besoins_pl': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
            'duree': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
         }
class ReboisementphysiqueForm(forms.ModelForm):
    class Meta:
        model = Reboisementphysique
        fields = ['n','realisation_physique','date']
class ReboisementfinanceForm(forms.ModelForm):
    class Meta:
        model = Reboisementfinancier
        fields = ['n','paiement','datefinance']