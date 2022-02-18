from datetime import datetime, date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import ModelForm, ModelChoiceField, DateInput, TimeInput
from django.contrib.auth.models import User
from med import models
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm, forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Entre Nom_Prenom...'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password...'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm password...'})

        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email...'})




class addrdv(forms.Form):

    cass = [
        ('C', [
                ('Specialiste', 'Specialiste'),
                ('Generaliste', 'Generaliste'),
                ('Certeficat', 'Certeficat'),
                           ]),
        ('R', [
                ('1R', '1R'),
                ('2R', '2R'),
                ('3R', '3R'),
                           ]),
        ('P.CH', 'P.CH'),
        ('Lab', 'Lab'),
        ('Plat', 'Plat'),
        ('Av, An', 'Av, An'),
        ('ECG', 'ECG')


    ]
    hours = [
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16')
    ]
    minutes = [
        ('00', '00'),
        ('15', '15'),
        ('30', '30'),
        ('45', '45'),

    ]

    Prestation = forms.CharField(widget=forms.Select(choices=cass))
    Comment = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter event comment"}))
    rdvtime = forms.DateTimeField(required=True,
                                  widget=DateInput(attrs={"type": "datetime-local", "class": "form-control"},
                                                   format="%Y-%m-%d"))
    paid = forms.DecimalField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Heur = forms.CharField(widget=forms.Select(choices=hours))
    Minute= forms.CharField(widget=forms.Select(choices=minutes))

class addts(forms.Form):
    hours = [
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16')
    ]
    minutes = [
        ('00', '00'),
        ('15', '15'),
        ('30', '30'),
        ('45', '45'),

    ]
    H = forms.CharField(widget=forms.Select(choices=hours))
    M = forms.CharField(widget=forms.Select(choices=minutes))


class UserReg(forms.Form):
    status = [
        ('Confirme', 'Confirme'),
        ('Non conf', 'Non conf'),
        ('Present', 'Present'),
        ('Absent', 'Absent')


    ]
    cass = [
        ('-----', '-----'),
        (
         'C', [
            ('Specialiste', 'Specialiste'),
            ('Generaliste', 'Generaliste'),
            ('Certeficat', 'Certeficat'),
        ]),
        ('R', [
            ('1R', '1R'),
            ('2R', '2R'),
            ('3R', '3R'),
        ]),
        ('P.CH', [
            ('P.CH', 'P.CH'),
            ('Circusi', 'Circusi')

        ]),
        ('Lab', 'Lab'),
        ('Plat', 'Plat'),
        ('Av, An', 'Av, An'),
        ('ECG', 'ECG')

    ]
    hours = [
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16')
    ]
    minutes = [
        ('00', '00'),
        ('15', '15'),
        ('30', '30'),
        ('45', '45'),

    ]
    Nom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prenom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Age = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Phone= forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Adresse = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    Commentaire = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
   # currentstate = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=status)
    Cas = forms.CharField(widget=forms.Select(choices=status))

    #drid= forms.ChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}))
    #drid= forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'})
   # drid= forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'})
    Medcin= ModelChoiceField(queryset=models.Dctr.objects.all())

  #  drid= forms.SelectMultiple(attrs={'class': 'form-field', 'placeholder': 'Attendees'})
    #cas = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    """datereg = forms.DateTimeField(required=True, widget=forms.DateTimeField(attrs={'class': 'form-control'}))"""
    Prestation= forms.CharField(widget=forms.Select(choices=cass))
    Autre_Prestation_Si_Exist= forms.CharField(widget=forms.Select(choices=cass))
    rdvtime= forms.DateTimeField(required=True, widget= DateInput(  attrs={"type": "datetime-local", "class": "form-control"},  format="%Y-%m-%dT" ))
    Heur= forms.CharField(widget=forms.Select(choices=hours))
    Minute= forms.CharField(widget=forms.Select(choices=minutes))

    Prix = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class AddOperatedPatient(forms.Form):
    status = [
        ('Confirme', 'Confirme'),
        ('Non conf', 'Non conf'),
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]
    cass = [
        (('-----', '-----'),
            'C', [

            ('Specialiste', 'Specialiste'),
            ('Generaliste', 'Generaliste'),
            ('Certeficat', 'Certeficat'),
        ]),
        ('R', [
            ('1R', '1R'),
            ('2R', '2R'),
            ('3R', '3R'),
        ]),
        ('P.CH', [
            ('P.CH', 'P.CH'),
            ('Circusi', 'Circusi')

        ]),
        ('Lab', 'Lab'),
        ('Plat', 'Plat'),
        ('Av, An', 'Av, An'),
        ('ECG', 'ECG')

    ]
    hours = [
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16')
    ]
    minutes = [
        ('00', '00'),
        ('15', '15'),
        ('30', '30'),
        ('45', '45'),

    ]
    Nom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prenom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Age = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Phone= forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Adresse  = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    Commentaire = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
   # currentstate = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=status)
    Cas = forms.CharField(widget=forms.Select(choices=status))

    #drid= forms.ChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-select'}))
    #drid= forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'})
   # drid= forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'})
    Medcin= ModelChoiceField(queryset=models.Dctr.objects.all())

  #  drid= forms.SelectMultiple(attrs={'class': 'form-field', 'placeholder': 'Attendees'})
    #cas = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    """datereg = forms.DateTimeField(required=True, widget=forms.DateTimeField(attrs={'class': 'form-control'}))"""
    Date= forms.DateTimeField(required=True, widget= DateInput(  attrs={"type": "datetime-local", "class": "form-control"},  format="%Y-%m-%dT"))
    Heur= forms.CharField(widget=forms.Select(choices=hours))
    Minute= forms.CharField(widget=forms.Select(choices=minutes))
    Nature_Chirugie= forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Pix_propose= forms.FloatField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prix = forms.FloatField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    Oriente = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    Lit = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'form-control'}))



class AddMedecines(forms.Form):
    types = [
        ('med1', 'med1'),
        ('med2', 'med2'),
        ('med3', 'med3'),
        ('med4', 'med4')

    ]
    Nom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Type= forms.CharField(widget=forms.Select(choices=types))
    Quantity = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prix = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = models.food
        fields = ['name', 'type', 'quantity', 'prix']


    @transaction.atomic
    def save(self):
        fd = models.medecines.objects.create()
        fd.name = self.cleaned_data.get('Nom')
        fd.type = self.cleaned_data.get('Type')
        fd.quantity = self.cleaned_data.get('Quantity')
        fd.prix = self.cleaned_data.get('Prix')
        fd.save()
        return fd


class AddFood(forms.Form):
    types = [
        ('des légumes ', 'des légumes '),
        ('des fruits', 'des fruits'),
        ('pain', 'pain'),
        ('eau', 'eau'),
        ('jus', 'jus'),
        (' lampes ', ' lampes '),
        ('gadgets', 'gadgets'),
        ('autres', 'autres'),

    ]
    Name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Type= forms.CharField(widget=forms.Select(choices=types))
    Quantity = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prix = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.food
        fields = ['name', 'type', 'quantity', 'prix']


    @transaction.atomic
    def save(self):
        fd = models.food.objects.create()
        fd.name = self.cleaned_data.get('Name')
        fd.type = self.cleaned_data.get('Type')
        fd.quantity = self.cleaned_data.get('Quantity')
        fd.prix = self.cleaned_data.get('Prix')
        fd.save()
        return fd


class AddUsed(forms.Form):
    types = [
        ('Medicamentd ',  [
        ('med1', 'med1'),
        ('med2', 'med2'),
        ('med3', 'med3'),
        ('med4', 'med4')

    ]),

        ('aliments', [
        ('des légumes ', 'des légumes '),
        ('des fruits', 'des fruits'),
        ('pain', 'pain'),
        ('eau', 'eau'),
        ('jus', 'jus'),
        (' lampes ', ' lampes '),
        ('gadgets', 'gadgets'),


    ]),

        ('autre', 'autre')

    ]
    Name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Type= forms.CharField(widget=forms.Select(choices=types))
    Quantity = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prix = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Used
        fields = ['name', 'type', 'quantity', 'prix']


    @transaction.atomic
    def save(self):
        fuck = models.Used.objects.create()
        fuck.name = self.cleaned_data.get('Name')
        fuck.type = self.cleaned_data.get('Type')
        fuck.quantity = self.cleaned_data.get('Quantity')
        fuck.prix = self.cleaned_data.get('Prix')
        fuck.save()
        return fuck

class Recreg(UserCreationForm):
    Nom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prenom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Age = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Adresse = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.is_receptionist = True
        user.fn = self.cleaned_data.get('Nom')
        user.ln = self.cleaned_data.get('Prenom')
        user.phone = self.cleaned_data.get('Phone')
        user.address = self.cleaned_data.get('Adresse')
        user.age = self.cleaned_data.get('Age')
        user.save()
        r = models.Rec.objects.create(user=user)
        r.save()
        return user

class Drreg(UserCreationForm):
    sectors = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E')

    ]

    Nom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prenom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Speciality = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Poucentage = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Poucentage_Chirurgie = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #payment = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    """datereg = forms.DateTimeField(required=True, widget=forms.DateTimeField(attrs={'class': 'form-control'}))"""

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.is_doctor = True
        user.fn = self.cleaned_data.get('Nom')
        user.ln = self.cleaned_data.get('Prenom')
        user.phone = self.cleaned_data.get('Phone')
        user.save()
        doctor = models.Dctr.objects.create(user=user)
        doctor.spec = self.cleaned_data.get('Speciality')
        doctor.prc=  self.cleaned_data.get('Poucentage')
        doctor.prccherg=  self.cleaned_data.get('Poucentage_Chirurgie')
        doctor.save()
        return user

class Assistant(UserCreationForm):

    Nom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Prenom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Age = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Adresse = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #role = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #role = forms.ChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=roles)
    Medcin= ModelChoiceField(queryset=models.Dctr.objects.all())
    Medcin2= ModelChoiceField(queryset=models.Dctr.objects.all())
    Medcin3= ModelChoiceField(queryset=models.Dctr.objects.all())
    """datereg = forms.DateTimeField(required=True, widget=forms.DateTimeField(attrs={'class': 'form-control'}))"""

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.is_assistant = True
        user.fn = self.cleaned_data.get('Prenom')
        user.ln = self.cleaned_data.get('Nom')
        user.phone = self.cleaned_data.get('Phone')
        user.address = self.cleaned_data.get('Adresse')
        user.age = self.cleaned_data.get('Age')
        user.save()
        assistant = models.Assistant.objects.create(user=user)
        assistant.drid.add(self.cleaned_data.get('Medcin'))
        assistant.drid.add(self.cleaned_data.get('Medcin2'))
        assistant.drid.add(self.cleaned_data.get('Medcin3'))
        assistant.save()
        return user

from .models import Patient, Dctr, Rdv


class PatForm(ModelForm):
    c = [
        ('Confirme', 'Confirme'),
        ('Non conf', 'Non conf'),
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]

    class Meta:
        model = Patient

        fields = ['prix', 'currentstate']

    def __init__(self, *args, **kwargs):
        super(PatForm, self).__init__(*args, **kwargs)
        self.fields['prix'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Entre Nom_Prenom...'})
        self.fields['currentstate'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Entre Nom_Prenom...'})






class updateRdv (forms.ModelForm):
    class Meta:
        model = Rdv

        fields = ['paid', 'rdvtime']

    def __init__(self, *args, **kwargs):
        super(updateRdv, self).__init__(*args, **kwargs)
        self.fields['paid'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'changer payment...'})
        self.fields['rdvtime'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'date...'})


       # Rdv.save(update_fields=["paid"])


