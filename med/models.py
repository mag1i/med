from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now



class User(AbstractUser):

    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    is_assistant = models.BooleanField(default=False)
    is_receptionist = models.BooleanField(default=False)

    fn = models.CharField(max_length=25, default='')
    ln = models.CharField(max_length=25, default='')
    age = models.IntegerField(default=0)
    phone = models.IntegerField(default=0)
    address = models.CharField(max_length=30, default='')


    def __str__(self):
        return self.fn + " " + self.ln

class Rec (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)

class Dctr (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    sector = models.CharField(max_length=30, default='')
    spec = models.CharField(max_length=25, default='')
    prc = models.CharField(max_length=25, default='')
    prccherg = models.CharField(max_length=25, default='')
    paymanet= models.FloatField(default=0)
    def __str__(self):
        return self.user.fn + " " + self.user.ln



class Assistant (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    drid=models.ManyToManyField(Dctr)



    def __str__(self):
        return self.user.fn + " " + self.user.ln

    def get_drid_ids(self):
        ret = ''

        for dept in self.drid.all():
            ret = dept.user.id
        # remove the last ',' and return the value.

        return ret

    def get_drid_values(self):
        ret = ''
        for dept in self.drid.all():
            ret = ret + dept.user.fn + '  ,'
        # remove the last ',' and return the value.
        return ret[:-1]




class Patient (models.Model):
    c = [
        ('Confirme', 'Confirme'),
        ('Non conf', 'Non conf'),
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]
    auto_increment_id = models.AutoField(primary_key=True)
    drid=models.ForeignKey(Dctr, on_delete=models.SET_NULL, null=True, blank=True)
    #rdv = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    firstname = models.CharField(max_length=25, default='')
    lastname = models.CharField(max_length=25, default='')
    age_patient = models.IntegerField(default=0)
    phonep = models.IntegerField(default=0)
    addressp = models.CharField(max_length=30)
    currentstate=models.CharField(max_length=15, choices=c)

    casp=models.CharField(max_length=15, default='')
    cast=models.CharField(max_length=15, default='')
    isop= models.BooleanField(default=False)
    nature = models.CharField(max_length=20, default='')
    prixprop = models.DecimalField(blank=True, max_digits=8, decimal_places=2, default=0)
    prix = models.DecimalField(blank=True,max_digits=8, decimal_places=2, default=0)
    orient = models.CharField(blank=True, max_length=20, default='')
    bed=models.IntegerField(blank=True, default=0)
    isin=models.BooleanField(default=False)

    def __str__(self):
        return self.firstname + " " +self.lastname

class Rdv(models.Model):
    pp = models.ForeignKey(Patient, on_delete=models.CASCADE,  null=True, blank=True)
    dr = models.ForeignKey(Dctr, on_delete=models.CASCADE,  null=True, blank=True)

 #   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    paid= models.DecimalField ( max_digits = 8, decimal_places=2 )
    rdvtime = models.DateTimeField()
    hr=models.IntegerField()
    mn=models.CharField(max_length=2)



    def __str__(self):
        return self.title

class medecines (models.Model):
    name = models.CharField(max_length=25, default='')
    type = models.CharField(max_length=25, default='')
    quantity= models.IntegerField(default=1)
    prix=models.FloatField(default=0)
    total=models.FloatField(default=0)
    dt=models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class food (models.Model):
    name = models.CharField(max_length=25, default='')
    type = models.CharField(max_length=25, default='')
    quantity= models.IntegerField(default=1)
    prix = models.FloatField(default=0)
    total = models.FloatField(default=0)
    dt=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
class Used (models.Model):
    name = models.CharField(max_length=25, default='')
    type = models.CharField(max_length=25, default='')
    quantity= models.IntegerField(default=1)
    prix = models.FloatField(default=0)
    total = models.FloatField(default=0)
    dt=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name

class TimeSlot (models.Model):
    h=models.IntegerField()
    m=models.CharField(max_length=2)

"""""
    #event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_members"
    )

  #  class Meta:        unique_together = ["event", "user"]

    def __str__(self):
        return str(self.user)
    """""