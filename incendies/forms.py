from django import forms 
from .models import *
from django.forms import ModelForm
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
    )

class DateInput(forms.DateTimeInput):
    input_type = 'datetime'

class IncendieForm(forms.ModelForm):
    class Meta:
        model = Incendie
        fields = ['wilaya','commune','forets','lieudit','Lat','Long','dateDepart','heureDepart','dateIntervention','heureIntervention','dateExt','heureExt','Commentaires']
        # widgets = {
        #     'wilaya': forms.Select(attrs={'class': 'myfieldclass'}),
        #     'commune': forms.Select(attrs={'class': 'myfieldclass'}),
        #     'forets': forms.TextInput(attrs={'class': 'myfieldclass'}),
        #     'lieudit': forms.TextInput(attrs={'class': 'myfieldclass'}),
        #     'Lat': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
        #     'Long': forms.TextInput(attrs={'class': 'myfieldclassLieuDit'}),
        #     'Départ de feux': DateInput(),
        #     'Date d\'Intervention': DateInput(),
        #     'dateExt':DateInput(),
        #     'Commentaires': forms.Textarea(attrs={'class': 'myfieldclassArea'}),
        #  }


     

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
 
 
        self.fields['commune'].queryset = Commune.objects.none()
 
                

  


        if 'wilaya' in self.data:
            try:
                wilaya_id = int(self.data.get('wilaya'))
                self.fields['commune'].queryset = Commune.objects.filter(wilaya_id=wilaya_id) 
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['commune'].queryset = self.instance.wilaya.commune_set 

class InterventionForm(ModelForm):
    class Meta:
        model= Intervention
        fields= ['organisme','moyenshumain','nombrehumain']
class MoyenForm(ModelForm):
    class Meta:
        model= Moyen
        fields= ['organisme','moyensmateriel','nombremateriel']

class TypeFormationincendieForm(ModelForm):
    class Meta:
        model= TypeFormationincendie
        fields= ['typeformation','espece','sup']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['espece'].queryset = Espece.objects.none()## toujours commence par le détail qu'on souhaite afficher ici c'est les espece

        if 'typeformation' in self.data:
            try:
                typeformation_id = int(self.data.get('typeformation'))
                self.fields['espece'].queryset = Espece.objects.filter(typeformation_id=typeformation_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['espece'].queryset = self.instance.typeformation.espece_set.order_by('name')

class DegatForm(ModelForm):
    class Meta:
        model= Degat
        fields= ['typedegat','nombre','cout']
