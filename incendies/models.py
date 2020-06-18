from datetime import datetime
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Subquery,OuterRef,Sum,Count,Max,Value as V ,FloatField, F


# Create your models here.
class Wilaya(models.Model):
    name = models.CharField(max_length= 200)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Lat =  models.DecimalField(max_digits=8, decimal_places=6,null=True,default=0)
    Long= models.DecimalField(max_digits=8, decimal_places=6,null=True,default=0)
    def __str__(self):
        return self.name    
class Commune(models.Model):
	name= models.CharField(max_length= 200)
	wilaya = models.ForeignKey(Wilaya,on_delete=models.SET_NULL, null=True)
	CodePostal = models.IntegerField()
	def __str__(self):
	  return self.name
class Circonscription(models.Model):
	name= models.CharField(max_length= 200)
	commune = models.ForeignKey(Commune,on_delete=models.SET_NULL, null=True)
  
class Typeformation (models.Model):
    name= models.CharField('type formation forestière',max_length= 200,null=True)
    # def get_percentage(self):
    #     total_sup = TypeFormationincendie.objects.filter(typeformation=self.id).annotate(superficie = Sum('sup'))
    #     cnt = TypeFormationincendie.objects.filter(typeformation=self).annotate(superficie = Sum('sup'))
    #     perc = cnt * 100 / total_sup
    #     return perc
    def __str__(self):
        return self.name
    
class Espece (models.Model):
    name= models.CharField('espece',max_length= 200,null=True)
    typeformation = models.ForeignKey(Typeformation, on_delete= models.CASCADE)

    def __str__(self):
        return self.name  
class Organisme(models.Model):
    name = models.CharField('organisme intervention',max_length= 200,blank=True)
    def __str__(self):
        return self.name     
class Moyenshumain (models.Model):
    name = models.CharField('ressources humains',max_length= 100,null=True)
    def __str__(self):
        return self.name
class Moyensmateriel (models.Model):
    name = models.CharField( max_length= 100,null=True)
    moyenshumain = models.ForeignKey(Moyenshumain, on_delete= models.CASCADE)
    def __str__(self):
        return self.name
class Typedegat (models.Model):
    name = models.CharField('type dégat',max_length= 100,null=True)
    def __str__(self):
        return self.name
class Incendie(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete= models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete= models.CASCADE)
    forets = models.CharField(max_length= 200,blank=True)
    lieudit = models.CharField(max_length= 200,blank=True)
    Lat =  models.DecimalField(max_digits=8, decimal_places=6,null=True,default=0)
    Long= models.DecimalField(max_digits=8, decimal_places=6,null=True,default=0)
    dateDepart = models.DateField('date départ')
    heureDepart=models.TimeField('heure départ')
    dateIntervention = models.DateField('date d\'intervention',blank=True,null = True)
    heureIntervention = models.TimeField('heure d\'intervention',blank=True,null = True)
    dateExt = models.DateField('date d\'extinction',blank=True,null = True)
    heureExt= models.TimeField('heure d\'intervention',blank=True,null = True)
    Commentaires = models.TextField(blank=True)
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    def  get_absolute_url(self):
    	return reverse('detail', kwargs={'incendie_id':self.id})
    def __str__(self):
    	return self.lieudit
    def get_json(self):
    	return {
            'id': self.id,
            'commune': self.commune.name,
            'wilaya': self.wilaya.name,
            'forets': self.forets,
            'lieudit': self.lieudit,
            'Lat': self.Lat,
            'Long': self.Long,
            'dateDepart': self.dateDepart.strftime("%Y-%m-%d"),
            'heureDepart': self.heureDepart.strftime("%H:%M"),
            'dateIntervention' : self.dateIntervention,
            'heureIntervention': self.heureIntervention,
            'dateExt':self.dateExt,
            'heureExt': self.heureExt, 
            'lieudit': self.lieudit,
            'interventions': [{'id': b.id,'organisme':b.organisme.name,'nombre':b.nombrehumain,'moyen':b.moyenshumain.name} for b in self.intervention_set.all()] ,
            'moyens': [{'id': c.id,'organisme':c.organisme.name,'nombre materiel':c.nombremateriel,'moyen matérel':c.moyensmateriel.name} for c in self.moyen_set.all()] ,
            'Type de formation': [{'id': d.id,'Superficie':d.sup,'Espèce':d.typeformation.name} for d in self.typeformationincendie_set.all()]  }

    def is_encours(self):
    	return self.dateExt == None
    

class Intervention ( models.Model): 
    incendie = models.ForeignKey(Incendie, on_delete= models.CASCADE)
    organisme = models.ForeignKey(Organisme,on_delete= models.CASCADE)
    moyenshumain = models.ForeignKey( Moyenshumain, on_delete= models.CASCADE)
    nombrehumain = models.IntegerField('nombre',null=True,default=0)
    def __str__(self):
        return str(self.organisme)
    def  get_absolute_url(self):
        return reverse('detail', kwargs={'incendie_id':self.incendie_id})

class Moyen ( models.Model):
    incendie = models.ForeignKey(Incendie, on_delete= models.CASCADE)
    organisme = models.ForeignKey(Organisme,on_delete= models.CASCADE)
    # moyenshumain = models.ForeignKey(Moyenshumain,on_delete=models.SET_NULL, null=True)
    # nombrehumain = models.IntegerField(null=True,default=0)
    moyensmateriel = models.ForeignKey( Moyensmateriel, on_delete= models.CASCADE) 
    nombremateriel = models.IntegerField('nombre',null=True,default=0)
    def __str__(self):
        return str(self.organisme)
    def  get_absolute_url(self):
        return reverse('detail', kwargs={'incendie_id':self.incendie_id})


class TypeFormationincendie ( models.Model):
    incendie = models.ForeignKey(Incendie, on_delete= models.CASCADE)
    typeformation = models.ForeignKey(Typeformation, on_delete= models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete= models.CASCADE)
    sup = models.DecimalField('superficie',max_digits=4, decimal_places=2,null=True,default=0)
    def  get_absolute_url(self):
        return reverse('detail', kwargs={'incendie_id':self.incendie_id})


class Degat ( models.Model):
    incendie = models.ForeignKey(Incendie, on_delete= models.CASCADE)
    typedegat = models.ForeignKey(Typedegat, on_delete= models.CASCADE)
    nombre = models.IntegerField('nombre',null=True,default=0)
    cout = models.DecimalField('coût monétaire',max_digits=10, decimal_places=2,null=True,default=0)
    def __str__(self):
        return str(self.typedegat)
    def  get_absolute_url(self):
        return reverse('detail', kwargs={'incendie_id':self.incendie_id})
class Limite_commune(models.Model):
    gid = models.IntegerField()
    objectid_1 = models.IntegerField()
    objectid = models.IntegerField()
    objectid_2 = models.IntegerField()
    nature = models.CharField(max_length=20)
    commune = models.CharField(max_length=30)
    autre_nom = models.CharField(max_length=30)
    nom_wilaya = models.CharField(max_length=30)
    wilaya = models.FloatField()
    origine = models.CharField(max_length=30)
    code = models.IntegerField()
    shape_leng = models.FloatField()
    shape_le_1 = models.FloatField()
    shape_le_2 = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    def __str__(self):
        return self.commune










