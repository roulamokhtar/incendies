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

class Canton(models.Model):
    name = models.CharField('Canton',max_length=25, null= True)
    layer = models.CharField('Foret Domaniale',max_length=25)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name
class Limite_commune(models.Model):
    gid = models.IntegerField()
    objectid_1 = models.IntegerField()
    objectid = models.IntegerField()
    objectid_2 = models.IntegerField()
    nature = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
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
        return self.name
class Parcellaire_perimetre(models.Model):
    objectid = models.IntegerField(null=True)
    name = models.CharField(max_length=27,null=True)
    layer = models.CharField(max_length=45,null=True)
    kml_folder = models.CharField(max_length=28,null=True)
    id_par = models.IntegerField(null=True)
    ha = models.IntegerField(null=True)
    a = models.IntegerField(null=True)
    ca = models.IntegerField(null=True)
    sup_ha = models.IntegerField(null=True)
    obs = models.CharField(max_length=100,null=True)
    shape_leng = models.FloatField(null=True)
    shape_area = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=4326)
    def __str__(self):
        return self.name
    
class Localites(models.Model):
    objectid = models.IntegerField()
    code_du_pp = models.CharField(max_length=254)
    annee = models.FloatField()
    daira = models.CharField(max_length=254)
    commune = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    type_de_pr = models.CharField(max_length=254)
    nom_du_bas = models.CharField(max_length=254)
    ville = models.FloatField()
    ville_nom_field = models.CharField(max_length=254)
    ville_id = models.FloatField()
    ville_depa = models.FloatField()
    ville_long = models.FloatField()
    ville_lati = models.FloatField()
    descriptio = models.CharField(max_length=254)
    geom = models.MultiPointField(srid=4326)
    def __str__(self):
        return self.name
class Perimetre(models.Model):
    objectid = models.IntegerField()
    id_per = models.IntegerField()
    nom = models.CharField(max_length=50)
    date_arre = models.DateField()
    ha = models.IntegerField(null=True)
    a = models.IntegerField(null=True)
    ca = models.IntegerField(null=True)
    sup_ha = models.IntegerField(null=True)
    obs = models.CharField(max_length=100,null=True)
    shape_leng = models.FloatField(null=True)
    shape_area = models.FloatField(null=True)
    sup = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=4326)
    def __str__(self):
        return self.nom

class Foret_recreative(models.Model):
    name = models.CharField(max_length=200)
    layer = models.CharField(max_length=200)
    kml_folder = models.CharField(max_length=200)
    geom = models.MultiPolygonField(srid=4326)
    def __str__(self):
        return self.name
class Reboisement(models.Model):
    name = models.CharField(max_length=31)
    layer = models.CharField(max_length=30)
    kml_folder = models.CharField(max_length=25)
    id_reboi = models.IntegerField()
    id_reboise = models.IntegerField()
    notificati = models.CharField(max_length=254)
    appel_offr = models.DateField(max_length=100,null=True)
    date_attri = models.CharField(max_length=254,null=True)
    entreprise = models.CharField(max_length=254,null=True)
    duree = models.IntegerField(null=True)
    nature_act = models.CharField(max_length=254,null=True)
    objectif = models.CharField(max_length=254,null=True)
    occupation = models.CharField(max_length=254,null=True)
    antecedant = models.CharField(max_length=254,null=True)
    lot = models.IntegerField(null=True)
    n_marche = models.CharField(max_length=254,null=True)
    date_march = models.DateField(null=True)
    montant_ma = models.DecimalField(max_digits=10, decimal_places=2,null=True,default=0)
    n_ods_depa = models.CharField(max_length=254,null=True)
    date_ods_d = models.DateField(null=True)
    n_ods_arre = models.IntegerField(null=True)
    date_ods_a = models.DateField(null=True)
    n_osd_repr = models.IntegerField(null=True)
    date_osd_r = models.DateField(null=True)
    nbr_jour_a = models.IntegerField(null=True)
    delais_con = models.IntegerField(null=True)
    date_expir = models.DateField(null=True)
    lancement = models.CharField(max_length=254,null=True)
    nbr_ouvrie = models.IntegerField(null=True)
    daira = models.CharField(max_length=254,null=True)
    district = models.CharField(max_length=254,null=True)
    triage = models.CharField(max_length=254,null=True)
    circonscri = models.CharField(max_length=254,null=True)
    commune = models.CharField(max_length=254,null=True)
    forets = models.CharField(max_length=254,null=True)
    cantons = models.CharField(max_length=254,null=True)
    volume_pre = models.IntegerField(null=True)
    espece = models.CharField(max_length=254,null=True)
    densite = models.IntegerField(null=True)
    besoins_pl = models.CharField(max_length=254,null=True)
    obs = models.CharField(max_length=254,null=True)
    longeure_c = models.CharField(max_length=254,null=True)
    pique = models.CharField(max_length=254,null=True)
    date_lance = models.CharField(max_length=254,null=True)
    nbr_ouvr_1 = models.IntegerField(null=True)
    ouverture_field = models.CharField(max_length=254,null=True)
    plantation = models.CharField(max_length=254,null=True)
    cloture_ml = models.IntegerField(null=True)
    nbr_plants = models.CharField(max_length=254,null=True)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=4326)

    def  get_absolute_url(self):
        return f"/projet/reboisements/{self.id}/"
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Reboisements"













