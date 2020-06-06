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
    def clean(self):
        cleaned_data = super(IncendieForm, self).clean()

        dateDepart = self.cleaned_data['dateDepart']
        heureDepart = self.cleaned_data['heureDepart']

        dateIntervention = self.cleaned_data['dateIntervention']
        heureIntervention = self.cleaned_data['heureIntervention']

        dateExt = self.cleaned_data['dateExt']
        heureExt = self.cleaned_data['heureExt']

        depart_dateTime = ('%s %s' % (dateDepart, heureDepart))
        intervention_dateTime = ('%s %s' % (dateIntervention, heureIntervention))
        extinction_dateTime = ('%s %s' % (dateIntervention, heureIntervention))

        # from_time = cleaned_data.get("from_time")
        # end_time = cleaned_data.get("end_time")
        if dateIntervention  and  not heureIntervention: 
            raise forms.ValidationError('renseigner le champ (heureIntervention)')
        if heureIntervention  and  not dateIntervention: 
            raise forms.ValidationError("  renseigner le champ (dateIntervention)   ")

        if depart_dateTime and intervention_dateTime:
            if intervention_dateTime < depart_dateTime:
                raise forms.ValidationError('<p style ="color:red">  date d\'intervention ne peut pas être avant le départ de feux !!!! </p>')

        if depart_dateTime and extinction_dateTime:       
            if extinction_dateTime < depart_dateTime:
                raise forms.ValidationError( '<span style ="color:red">'   "date d'Extinction  ne peut pas être avant le départ de feux !!!!" '</span')

        if intervention_dateTime and extinction_dateTime:       
            if extinction_dateTime < intervention_dateTime:
                raise forms.ValidationError("date d'Extinction  ne peut pas être avant la d'intervention de feux !!!!")


        return cleaned_data

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
