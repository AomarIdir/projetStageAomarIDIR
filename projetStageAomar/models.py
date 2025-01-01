from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
#import uuid

#class User(User):
    #uid=models.UUIDField(primary_key=True,default=uuid.uuid4)


from django.db import models

from django.db import models

class Categories(models.Model):
    categorie=models.CharField(max_length=20)
    class Meta:
        db_table='categories'

class Questions(models.Model):
    qst = models.TextField()
    categorie = models.ForeignKey(Categories,on_delete=models.CASCADE)

    class Meta:
        db_table = 'questions'

class Reponses(models.Model):
    reponse = models.CharField(max_length=100)
    qst_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    est_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'reponses'



class Historique_tests(models.Model):
    categorie = models.ForeignKey(Categories,on_delete=models.CASCADE)
    eleve=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.FloatField()
    date_du_test=models.DateTimeField(default=timezone.now)
    class Meta:
        db_table="historique_tests"  
        unique_together=('categorie','eleve','date_du_test') 