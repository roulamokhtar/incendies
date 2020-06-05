from datetime import datetime
from django.contrib.gis.db import models
from django.contrib.auth.models import User

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




class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name


class OrientationGlobale(models.Model):
    name= models.CharField(max_length=200)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Orientations Globales"

class OrientationStrategiques(models.Model):
    name= models.CharField(max_length=200)
    orientationglobal=models.ForeignKey(OrientationGlobale,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Orientations Stratégiques"

class ObjectifGlobal(models.Model):
    name= models.CharField(max_length=200)
    orientationstrategique = models.ForeignKey(OrientationStrategiques,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    # class Meta:
    #     verbose_name_plural = "Objectifs Globales"
class ObjectifSpecifique(models.Model):
    name= models.CharField(max_length=200)
    objectifglobal=models.ForeignKey(ObjectifGlobal,on_delete=models.CASCADE)
 
    def __str__(self):
        return self.name
    def  get_absolute_url(self):
        return f"/objectifspecifique/{self.id}/"
    # class Meta:
    #     verbose_name_plural = "Objectifs spécifique"
class Resultat(models.Model):
    name= models.CharField(max_length=200)
    objectifspecifique=models.ForeignKey(ObjectifSpecifique,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Résultats"

class Projet(models.Model):
    objectifglobal = models.ForeignKey(ObjectifGlobal,on_delete=models.SET_NULL, null=True)
    titre=models.CharField(max_length=255)
    justification=models.TextField(null=True)
    commune = models.ForeignKey(Limite_commune,on_delete=models.SET_NULL, null=True)
    lieu_dit = models.CharField(max_length=200)
    superficie_zone= models.IntegerField(null=True)
    menage = models.IntegerField(null=True)
    population = models.IntegerField(null=True)
    duree= models.IntegerField(null=True)
    annee= models.IntegerField(null=True)
    deleted_at= models.DateTimeField(default=datetime.now, blank=True)
    objectifspecifique=models.ManyToManyField(ObjectifSpecifique)
    resultat= models.ManyToManyField(Resultat)
    user = models.ForeignKey(User, on_delete =models.CASCADE)

 
    
    def  get_absolute_url(self):
        return f"/projet/{self.id}/"
    def __str__(self):
        return self.titre
    class Meta:
        verbose_name_plural = "Projets"

class Projetspecifique(models.Model):
    projet = models.ForeignKey(Projet,on_delete=models.SET_NULL, null=True)
    objectifspecifique = models.ForeignKey(ObjectifSpecifique,on_delete=models.SET_NULL, null=True)
        
    def  get_absolute_url(self):
        return f"/Projetos/{self.id}/"
    def __str__(self):
        return self.objectifspecifique
    class Meta:
        verbose_name_plural = "projet objectif specifique"

class Projetresultat(models.Model):
    projetspecifique = models.ForeignKey(Projetspecifique,on_delete=models.SET_NULL, null=True)
    resultat = models.ForeignKey(Resultat,on_delete=models.SET_NULL, null=True)
        
    def  get_absolute_url(self):
        return f"/Projetresultat/{self.id}/"
    def __str__(self):
        return self.resultat
    class Meta:
        verbose_name_plural = "projet résultats"





class IndicateurResultat(models.Model):
    name= models.CharField(max_length=200)
    resultat=models.ForeignKey(Resultat,on_delete=models.CASCADE)

class IndicateurObjectifSpecifique(models.Model):
    name= models.CharField(max_length=200)
    resultat=models.ForeignKey(ObjectifSpecifique,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Indicateurs de objectifs spécifique"

class IndicateurObjectifsGlobal(models.Model):
    name= models.CharField(max_length=200)
    resultat=models.ForeignKey(ObjectifGlobal,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Indicateurs de objectifs globaux"

class Indicateurdeclinaison(models.Model):
    resultat_indic = models.CharField(max_length=200)
    resultat_id = models.ForeignKey(Resultat,on_delete=models.CASCADE)
    name =  models.CharField(max_length=200)
    ciblle_2035 = models.CharField(max_length=200)
    unite= models.CharField(max_length=200)
    quinquennat1= models.CharField(max_length=200)
    quinquennat2= models.CharField(max_length=200)
    quinquennat3= models.CharField(max_length=200)
    quinquennat4= models.CharField(max_length=200)
 

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "declinaison indicateurs quinquenat"


class nomenclature(models.Model):
    nomenclature = models.CharField(max_length=144)
     
 
    def __str__(self):
        return self.nomenclature     
class Action(models.Model):
    name = models.ForeignKey(nomenclature, on_delete =models.CASCADE)
    volume= models.DecimalField(max_digits=10, decimal_places=2)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    source_financement = models.CharField(max_length=100)
    duree= models.IntegerField()
    ods=models.DateTimeField(default=datetime.now, blank=True)
    projet = models.ForeignKey(Projet, on_delete =models.CASCADE)
    resultat= models.ManyToManyField(Resultat)
 
    def __str__(self):
        return f"{self.name} on {self.source_financement}"
 
class ActionSig(models.Model):
    name = models.ForeignKey(nomenclature, on_delete =models.CASCADE)
    volume= models.DecimalField(max_digits=5, decimal_places=2)
    montant = models.DecimalField(max_digits=5, decimal_places=2)
    source_financement = models.CharField(max_length=100)
    duree= models.IntegerField()
    ods=models.DateTimeField(default=datetime.now, blank=True)
    geom = models.GeometryCollectionField(srid=4326)
    projet = models.ForeignKey(Projet, on_delete =models.CASCADE)
  
    def __str__(self):
        return self.name



class physique(models.Model):
    realisation_physique= models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True)
    action = models.ForeignKey(Action, on_delete =models.CASCADE)
 

class financier(models.Model):
    paiement= models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True)
    action = models.ForeignKey(Action, on_delete =models.CASCADE)

 

class Forets(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    wilaya = models.IntegerField()
    cod_de_poly = models.CharField('code de la forets', max_length=50)
    comm = models.CharField('Commune', max_length=200)
    foret = models.CharField('forets', max_length=200)
    sup = models.IntegerField()
    espece_d = models.CharField('Espece dominante', max_length=200)
    espece_s = models.CharField('Espece secondaire', max_length=200)
    obs = models.TextField()
     
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.foret
class Canton(models.Model):
    name = models.CharField('Canton',max_length=25, null= True)
    layer = models.CharField('Foret Domaniale',max_length=25)
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name

class Cantons(models.Model):
    name = models.CharField(max_length=25)
    layer = models.CharField(max_length=25)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    nature_jur = models.CharField(max_length=50)
    geom = models.MultiPolygonField(srid=4326)
    def __str__(self):
        return self.name

class Piste(models.Model):
    gid = models.IntegerField()
    long_piste = models.FloatField()
    larg_piste = models.FloatField()
    id1 = models.FloatField()
    nom_foret = models.CharField(max_length=50)
    n_piste = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=50)
    nat_piste = models.CharField(max_length=50)
    etat = models.CharField(max_length=50)
    date_ouver = models.CharField(max_length=50)
    amena_o_n = models.CharField(max_length=5)
    date_amen = models.CharField(max_length=50)
    obs = models.CharField(max_length=150)
    geom = models.MultiLineStringField(srid=4326)
    def __str__(self):
        return self.name 
class Point_eau(models.Model):
    gid = models.IntegerField()
    nom_foret = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    capacite = models.CharField(max_length=50)
    nature = models.CharField(max_length=50)
    etat = models.CharField(max_length=50)
    date_reali = models.CharField(max_length=50)
    date_d_ame = models.CharField(max_length=50)
    obs = models.CharField(max_length=150)
    etat_1 = models.CharField(max_length=50)
    geom = models.MultiPointField(srid=4326)
    def __str__(self):
        return self.name 
    class Meta:
        verbose_name_plural = "Points d'eau"

class Tpf(models.Model):
    gid = models.IntegerField()
    tenant = models.CharField(max_length=50)
    about = models.CharField(max_length=50)
    nat_tpf = models.CharField(max_length=50)
    long_tpf = models.FloatField()
    larg_tpf = models.FloatField()
    sup = models.FloatField()
    etat = models.CharField(max_length=50)
    date_ouver = models.CharField(max_length=50)
    amena_o_n = models.CharField(max_length=5)
    date_amen = models.CharField(max_length=50)
    obs = models.CharField(max_length=150)
    nom_foret = models.CharField(max_length=50)
    km = models.CharField(max_length=10)
    n_tpf_1 = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name 


class Maison_forestiere(models.Model):
    gid = models.IntegerField()
    nom_foret = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    lieu_dit = models.CharField(max_length=50)
    commune = models.CharField(max_length=50)
    sup = models.FloatField()
    usage = models.CharField(max_length=50)
    annee_cons = models.CharField(max_length=50)
    etat = models.CharField(max_length=50)
    occup = models.CharField(max_length=50)
    access = models.CharField(max_length=5)
    comp = models.CharField(max_length=50)
    comodite = models.CharField(max_length=50)
    dependance = models.CharField(max_length=50)
    date_d_reh = models.CharField(max_length=50)
    obs = models.CharField(max_length=150)
    access_1 = models.CharField(max_length=5)
    geom = models.MultiPointField(srid=4326)

    def __str__(self):
        return self.name 

class Brigade(models.Model):
    gid = models.IntegerField()
    nom_foret = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    lieu_dit = models.CharField(max_length=50)
    commune = models.CharField(max_length=50)
    usage = models.CharField(max_length=50)
    etat = models.CharField(max_length=50)
    occup = models.CharField(max_length=5)
    access = models.CharField(max_length=5)
    composi = models.CharField(max_length=50)
    comodite = models.CharField(max_length=50)
    dependance = models.CharField(max_length=50)
    date_d_ame = models.CharField(max_length=50)
    obs = models.CharField(max_length=150)
    annee_cons = models.IntegerField()
    surface = models.FloatField()
    geom = models.MultiPointField(srid=4326)
    def __str__(self):
        return self.lieu_dit 

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


class Route(models.Model):
    objectid = models.IntegerField()
    nom = models.CharField(max_length=50)
    ref = models.CharField(max_length=10)
    type_route = models.CharField(max_length=50)
    freq_route = models.CharField(max_length=50)
    entretenue = models.CharField(max_length=50)
    sens = models.CharField(max_length=50)
    carossable = models.CharField(max_length=50)
    shape_leng = models.FloatField()
    geom = models.MultiLineStringField(srid=4326)
    def __str__(self):
        return self.nom

class Route1(models.Model):
    area = models.CharField(max_length=254)
    highway = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    oneway = models.CharField(max_length=254)
    ref = models.CharField(max_length=254)
    ref_ar = models.CharField(max_length=254)
    surface = models.CharField(max_length=254)
    bridge = models.CharField(max_length=254)
    layer = models.CharField(max_length=254)
    maxspeed = models.CharField(max_length=254)
    lanes = models.CharField(max_length=254)
    junction = models.CharField(max_length=254)
    hgv = models.CharField(max_length=254)
    source = models.CharField(max_length=254)
    name_ar = models.CharField(max_length=254)
    note = models.CharField(max_length=254)
    alt_name = models.CharField(max_length=254)
    fixme = models.CharField(max_length=254)
    loc_name = models.CharField(max_length=254)
    tunnel = models.CharField(max_length=254)
    access = models.CharField(max_length=254)
    service = models.CharField(max_length=254)
    bicycle = models.CharField(max_length=254)
    foot = models.CharField(max_length=254)
    maxheight = models.CharField(max_length=254)
    footway = models.CharField(max_length=254)
    embankment = models.CharField(max_length=254)
    incline = models.CharField(max_length=254)
    name_kab = models.CharField(max_length=254)
    constructi = models.CharField(max_length=254)
    motor_vehi = models.CharField(max_length=254)
    smoothness = models.CharField(max_length=254)
    ford = models.CharField(max_length=254)
    crossing = models.CharField(max_length=254)
    passing_pl = models.CharField(max_length=254)
    bus = models.CharField(max_length=254)
    public_tra = models.CharField(max_length=254)
    name_en = models.CharField(max_length=254)
    name_fr = models.CharField(max_length=254)
    network = models.CharField(max_length=254)
    bench = models.CharField(max_length=254)
    covered = models.CharField(max_length=254)
    shelter = models.CharField(max_length=254)
    lamp_type = models.CharField(max_length=254)
    internet_a = models.CharField(max_length=254)
    geom = models.MultiLineStringField(srid=4326)
    def __str__(self):
        return self.name



class Foret_recreative(models.Model):
    name = models.CharField(max_length=200)
    layer = models.CharField(max_length=200)
    kml_folder = models.CharField(max_length=200)
    geom = models.MultiPolygonField(srid=4326)
    def __str__(self):
        return self.name
        
class Elevation(models.Model):
    name = models.CharField(max_length=100)
    rast = models.RasterField()



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

class Reboisementphysique(models.Model):
    n = models.IntegerField(null=True)
    realisation_physique= models.DecimalField(max_digits=10, decimal_places=2, null=True )
    date = models.DateField()
    reboisement = models.ForeignKey(Reboisement, on_delete =models.CASCADE)
 

class Reboisementfinancier(models.Model):
    n = models.IntegerField(null=True)
    paiement= models.DecimalField(max_digits=10, decimal_places=2,null=True)
    datefinance = models.DateField()
    reboisement = models.ForeignKey(Reboisement, on_delete =models.CASCADE)