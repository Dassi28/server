from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class Region(models.Model):    
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

class Departement(models.Model):    
    nom = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete= models.CASCADE,related_name='region')
    def __str__(self):
        return self.nom

class Ville(models.Model):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete= models.CASCADE ,related_name='departement')
    def __str__(self):
        return self.nom

class Formation(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
        
class Cycle(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Etablissement(models.Model):
    nom = models.CharField(max_length=100)
    lieux = models.ForeignKey(Ville, null=True, on_delete=models.CASCADE, related_name='lieux')

    def __str__(self):
        return self.nom

class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='specialites')
    cycle = models.ForeignKey(Cycle,on_delete= models.CASCADE,related_name='specialites')
    etablissement = models.ManyToManyField(Etablissement ,related_name='specialites')
    

    def __str__(self):
        return self.nom


class Payement(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)

    def __str__(self):
        return self.transaction_id
