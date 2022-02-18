import calendar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, OuterRef, Subquery
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.template.context_processors import csrf

from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.http import HttpResponseRedirect
from med import models
from med import forms
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Rdv
from datetime import timedelta, datetime, date
from django.views import generic
from django.utils.safestring import mark_safe

from .util import Cal
from .utils import Calendar
User = get_user_model()

def Index(request):
    context={'Nom': 'mags'}
    return render(request, 'index.html', context)




def chemin(request):
    patients = models.Patient.objects.all()

    context = {'p': patients}

    return render(request, 'chemin.html', context)


def floor(request):
    patients = models.Patient.objects.all()

    context = {'p': patients}

    return render(request, 'floor.html', context)


def op(request):
    patients = models.Patient.objects.all()

    context = {'p': patients}

    return render(request, 'op.html', context)
def PatientDetails(request, p):
    patients = models.Patient.objects.get(auto_increment_id=p)

    context = {'p': patients}

    return render(request, 'patientdetails.html', context)


def removeBed(request, p):
    pat = models.Patient.objects.get(auto_increment_id=p)
    pat.bed=0
    pat.save()
    return redirect('chemin')

    context = {'p': pat}

    return render(request, 'patientdetails.html', context)


@login_required(login_url='index')
def Patients( request):

    patients=models.Patient.objects.all()
    usr= request.user
   # rdv = models.Rdv.objects.filter(pp=d)
    doctor = models.Dctr
    a="Confirme"
    b="Non conf"
    c="Present"
    d="Absent"
    isin= False
    c1 = "Specialiste"
    c2 = "Generaliste"
    c3 = "Certeficat"
    r1 = "R1"
    r2 = "R2"
    r3 = "R3"
    fk='aa bb'

    context={'p': patients, 'dr':doctor, 'a':a, 'b':b, 'c':c, 'd':d, 'isin':isin,  'c1':c1,'c2':c2,'c3':c3, 'r1':r1,'r2':r2, 'r3':r3, 'usr':usr, 'fk':fk}
    return render(request, 'patient.html', context)
@login_required(login_url='index')

def PatientsOp( request):

    patients=models.Patient.objects.filter(isop=True)
   # rdv = models.Rdv.objects.filter(pp=d)
    doctor = models.Dctr
    a="Confirme"
    b="Non conf"
    c="Present"
    d="Absent"
    isin= False
    repeated= 0
    ori = models.Patient.objects.values('orient').annotate(Count('auto_increment_id')).filter(auto_increment_id__count__gt=3)
    orc= models.Patient.objects.filter(orient__in=[i['orient'] for i in ori])# <--- gt 0 will get all the objects having occurred in DB i.e is greater than 0
    for rep in orc:
        repeated=repeated+1
    subquery =  models.Patient.objects.filter(orient=OuterRef('orient')).values('orient').annotate(dup_count=Count('*'))
    rep=models.Patient.objects.all().annotate(dup_count=Subquery(subquery.values('orient')))
    context={'p': patients, 'dr':doctor, 'a':a, 'b':b, 'c':c, 'd':d, 'isin':isin, 'ori': orc, 'rep': rep}
    return render(request, 'oppatient.html', context)

@login_required(login_url='index')
def PatientsNonOp( request):

    patients=models.Patient.objects.filter(isop=False)
   # rdv = models.Rdv.objects.filter(pp=d)
    doctor = models.Dctr
    a="Confirme"
    b="Non conf"
    c="Present"
    d="Absent"
    e="  "

    isin= False
    context={'p': patients, 'dr':doctor, 'a':a, 'b':b, 'c':c, 'd':d, 'isin':isin, 'e':e }
    return render(request, 'patientm.html', context)

def isinn( request, p):
    ptt = models.Patient.objects.get(auto_increment_id=p)
    if ptt.isin == False:
        ptt.isin=True
    else:
        ptt.isin= False

    ptt.save()
    return redirect('patientm')
def isinnop( request, p):
    ptt = models.Patient.objects.get(auto_increment_id=p)
    if ptt.isin == False:
        ptt.isin=True
    else:
        ptt.isin= False

    ptt.save()
    return redirect('patientop')
def isinntout( request, p):
    ptt = models.Patient.objects.get(auto_increment_id=p)
    if ptt.isin == False:
        ptt.isin=True
    else:
        ptt.isin= False

    ptt.save()
    return redirect('patient')
def isinnts( request, p):
    ptt = models.Patient.objects.get(auto_increment_id=p)
    if ptt.isin == False:
        ptt.isin=True
    else:
        ptt.isin= False

    ptt.save()
    return redirect('ts')
@login_required(login_url='index')
def PatientsOfDoctor( request):
    user = request.user
    patients=models.Patient.objects.filter(drid=user.id)

    a = "Confirme"
    b = "Non conf"
    c = "Present"
    d = "Absent"
    isin = False
    c1 = "Specialiste"
    c2 = "Generaliste"
    c3 = "Certeficat"
    r1 = "R1"
    r2 = "R2"
    r3 = "R3"

    doctor = models.Dctr
    context={'p': patients, 'dr':doctor, 'a':a, 'b':b, 'c':c, 'd':d, 'isin':isin,  'c1':c1,'c2':c2,'c3':c3, 'r1':r1,'r2':r2, 'r3':r3}
    return render(request, 'drpatient.html', context)

@login_required(login_url='index')
def Medecines( request):

    meds=models.medecines.objects.all()
    food=models.food.objects.all()
    used=models.Used.objects.all()
    medtotal=0
    foodtotal=0
    usedtotal=0
    dt=date.today()


    for instance in food:
        instance.total= instance.prix * instance.quantity
    for t in meds:
        t.total= t.prix * t.quantity

    for mt in meds:
        medtotal += mt.total

    for ft in food:
        foodtotal += ft.total
    for s in used:
        s.total = s.prix * s.quantity

    for ss in used:
        usedtotal += ss.total





    context={'f': food, 'm': meds, 'mt':medtotal, 'ft':foodtotal, 'uu':used, 'ss':usedtotal, 'date':date.today()}
    #return HttpResponse('display all students here')
    return render(request, 'medecines.html', context)

@login_required(login_url='index')
def Food( request):

    fd=models.food.objects.all()


    context={'f': fd}
    #return HttpResponse('display all students here')
    return render(request, 'medecines.html', context)
def Used( request):

    fuck=models.Used.objects.all()


    context={'u': fuck}
    #return HttpResponse('display all students here')
    return render(request, 'medecines.html', context)
@login_required(login_url='index')
def Doctors( request):

    doctors=models.Dctr.objects.all()

    context={'d': doctors}
    #return HttpResponse('display all students here')
    return render(request, 'Drs.html', context)
@login_required(login_url='index')
def Assistants( request):

    assi=models.Assistant.objects.all()
    ass=models.Assistant
    dr=ass.drid




    context={'r': assi, 'dr':dr, 'm':assi}
    #return HttpResponse('display all students here')
    return render(request, 'assistants.html', context)
@login_required(login_url='index')
def Allrdvs( request):
    v = date.today()
    dt = v.day
    dm = v.month
    dy = v.year
    rdv=models.Rdv.objects.filter(rdvtime__day=dt, rdvtime__month=dm, rdvtime__year=dy)
    total = 0
    for instance in rdv:

        total += instance.paid
        print (total)

    context={'d': rdv, 'total':total}
    #return HttpResponse('display all students here')
    return render(request, 'allrdvs.html', context)
@login_required(login_url='index')
def MonthTotal( request):
    dt=date.today()
    mt=dt.month


    rdv=models.Rdv.objects.filter( rdvtime__month=mt)
    total = 0
    for instance in rdv:

        total += instance.paid
        print (total)

    context={'d': rdv, 'total':total}
    #return HttpResponse('display all students here')
    return render(request, 'monthtotal.html', context)
@login_required(login_url='index')
def YearTotal( request):
    dt=date.today()
    mt=dt.year


    rdv=models.Rdv.objects.filter( rdvtime__year=mt)
    total = 0
    for instance in rdv:

        total += instance.paid
        print (total)

    context={'d': rdv, 'total':total}
    #return HttpResponse('display all students here')
    return render(request, 'yeartotal.html', context)
@login_required(login_url='index')
def WeekTotal( request):
    dt=date.today()
    end_date = dt - timedelta(days=7)


    rdv=models.Rdv.objects.filter( rdvtime__range=(end_date, dt))
    total = 0
    for instance in rdv:

        total += instance.paid
        print (total)

    context={'d': rdv, 'total':total}
    #return HttpResponse('display all students here')
    return render(request, 'weektotal.html', context)
@login_required(login_url='index')
def DailyIncome(request, did):
    dt=datetime.today()
    v = date.today()
    dt = v.day
    dm = v.month
    dy = v.year
    yesterday = datetime.today() - timedelta(days=1)
    rdv = models.Rdv.objects.filter(dr=did, rdvtime__day=dt, rdvtime__month=dm, rdvtime__year=dy)
    total = 0
    for instance in rdv:
        total += instance.paid
        print(total)

    context = {'dd': rdv, 'total': total, 'did': did, 'y':yesterday}
    # return HttpResponse('display all students here')
    return render(request, 'drrdv.html', context)
@login_required(login_url='index')
def WeeklyIncome(request, did):

    v = date.today()
    end_date = v - timedelta(days=7)

    yesterday = datetime.today() - timedelta(days=1)
    rdv = models.Rdv.objects.filter(dr=did, rdvtime__range=(end_date, v))
    total = 0
    for instance in rdv:
        total += instance.paid
        print(total)

    context = {'dd': rdv, 'total': total, 'did': did, 'y':yesterday}
    # return HttpResponse('display all students here')
    return render(request, 'weeklyincome.html', context)
@login_required(login_url='index')
def DailyDr(request):
    dt=datetime.today()
    usr=request.user
    v = date.today()
    dt = v.day
    dm = v.month
    dy = v.year
    yesterday = datetime.today() - timedelta(days=1)
    rdv = models.Rdv.objects.filter(dr=usr.id, rdvtime__day=dt, rdvtime__month=dm, rdvtime__year=dy)
    total = 0
    for instance in rdv:
        total += instance.paid
        print(total)

    context = {'dd': rdv, 'total': total, 'did': usr, 'y':yesterday}
    # return HttpResponse('display all students here')
    return render(request, 'drrdv.html', context)
@login_required(login_url='index')
def WeeklyDr(request):
    usr=request.user
    v = date.today()
    end_date = v - timedelta(days=7)

    yesterday = datetime.today() - timedelta(days=1)
    rdv = models.Rdv.objects.filter(dr=usr.id, rdvtime__range=(end_date, v))
    total = 0
    for instance in rdv:
        total += instance.paid
        print(total)

    context = {'dd': rdv, 'total': total, 'did': usr, 'y':yesterday}
    # return HttpResponse('display all students here')
    return render(request, 'weeklyincome.html', context)
@login_required(login_url='loginmed')
def MonthIncome( request, did):
    v = date.today()
    dt = v.month
    rdv = models.Rdv.objects.filter(dr=did, rdvtime__month=dt)
    total = 0
    for n in rdv:
        total += n.paid
    context={'dd': rdv, 'total':total, 'did':did, 'dt': dt}
    #return HttpResponse('display all students here')
    return render(request, 'monthincome.html', context)
@login_required(login_url='loginmed')
def MonthDr( request):
    v = date.today()
    usr=request.user
    dt = v.month
    rdv = models.Rdv.objects.filter(dr=usr.id, rdvtime__month=dt)
    total = 0
    for n in rdv:
        total += n.paid
    context={'dd': rdv, 'total':total, 'did':usr, 'dt': dt}
    #return HttpResponse('display all students here')
    return render(request, 'monthincome.html', context)
@login_required(login_url='login')
def YearIncome( request, did):
    v = date.today()

    dt = v.year
    rdv = models.Rdv.objects.filter(dr=did, rdvtime__year=dt)
    drr=models.Dctr.objects.filter(user_id=did)
    total = 0
    for n in rdv:
        total += n.paid
    context={'dd': rdv, 'total':total, 'did':did, 'dt': dt, 'drr':drr}
    #return HttpResponse('display all students here')
    return render(request, 'yearincome.html', context)

@login_required(login_url='index')
def YearDr( request):
    v = date.today()
    usr=request.user

    dt = v.year
    rdv = models.Rdv.objects.filter(dr=usr.id, rdvtime__year=dt)
    #drr=models.Dctr.objects.filter(user_id=did)
    total = 0
    for n in rdv:
        total += n.paid
    context={'dd': rdv, 'total':total, 'did':usr, 'dt': dt}
    #return HttpResponse('display all students here')
    return render(request, 'yearincome.html', context)
@login_required(login_url='index')

def test(request):
    return render(request, 'test.html')

def Register(request):
    fd=forms.UserReg(request.POST or None)
    dt=date.today()

    msg = ''
    if fd.is_valid():
        pt= models.Patient()

       # r=models.Event(pp=pt.objects.get(auto_increment_id=pt.auto_increment_id))
        r=models.Rdv()
        pt.firstname = fd.cleaned_data['Prenom']
        pt.lastname = fd.cleaned_data['Nom']
        pt.age_patient = fd.cleaned_data['Age']
        pt.phonep = fd.cleaned_data['Phone']
        pt.addressp = fd.cleaned_data['Adresse']
        r.pp=pt
        pt.drid = fd.cleaned_data['Medcin']
        pt.currentstate = fd.cleaned_data['Cas']
        pt.casp=fd.cleaned_data['Prestation']
        pt.cast=fd.cleaned_data['Autre_Prestation_Si_Exist']
        pt.prix=fd.cleaned_data['Prix']
        r.title= fd.cleaned_data['Prestation']
        r.rdvtime= fd.cleaned_data['rdvtime']
        r.hr = fd.cleaned_data['Heur']
        r.mn = fd.cleaned_data['Minute']
        r.paid = fd.cleaned_data['Prix']

        r.dr=pt.drid


       # pt.rdv.title = fd.cleaned_data['cas']

        pt.save()
        r.save()

        msg = 'data is saved'
        return redirect('patient')

    context = {'formreg': fd,

               'msg': msg
    }

    return render(request, 'register.html', context)


def draddpat(request):
    fd = forms.UserReg(request.POST or None)
    dt = date.today()

    msg = ''
    if fd.is_valid():
        pt = models.Patient()

        # r=models.Event(pp=pt.objects.get(auto_increment_id=pt.auto_increment_id))
        r = models.Rdv()
        pt.firstname = fd.cleaned_data['First_Name']
        pt.lastname = fd.cleaned_data['Last_Name']
        pt.age_patient = fd.cleaned_data['Age']
        pt.phonep = fd.cleaned_data['Phone']
        pt.addressp = fd.cleaned_data['Address']
        r.pp = pt
        pt.drid = fd.cleaned_data['doctor']
        pt.currentstate = fd.cleaned_data['currentstate']
        pt.casp = fd.cleaned_data['Prestation']
        pt.cast = fd.cleaned_data['Autre_Prestation_Si_Exist']
        pt.prix = fd.cleaned_data['Prix']
        r.title = fd.cleaned_data['Prestation']
        r.rdvtime = fd.cleaned_data['rdvtime']
        r.hr = fd.cleaned_data['Heur']
        r.mn = fd.cleaned_data['Minute']
        r.paid = fd.cleaned_data['Prix']

        r.dr = pt.drid

        # pt.rdv.title = fd.cleaned_data['cas']

        pt.save()
        r.save()

        msg = 'data is saved'
        return redirect('pd')

    context = {'formreg': fd,

               'msg': msg
               }

    return render(request, 'draddpat.html', context)
def AjoutPatOp(request):
    fd=forms.AddOperatedPatient(request.POST or None)
    dt=date.today()

    msg = ''
    if fd.is_valid():
        pt= models.Patient()

       # r=models.Event(pp=pt.objects.get(auto_increment_id=pt.auto_increment_id))
        r=models.Rdv()
        pt.isop=True
        pt.firstname = fd.cleaned_data['Prenom']
        pt.lastname = fd.cleaned_data['Nom']
        pt.age_patient = fd.cleaned_data['Age']
        pt.phonep = fd.cleaned_data['Phone']
        pt.addressp = fd.cleaned_data['Adresse']
        r.pp=pt
        pt.drid = fd.cleaned_data['Medcin']
        pt.currentstate = fd.cleaned_data['Cas']
        pt.nature=fd.cleaned_data['Nature_Chirugie']
        pt.prixprop=fd.cleaned_data['Pix_propose']
        pt.prix=fd.cleaned_data['Prix']
        pt.orient=fd.cleaned_data['Oriente']
        pt.bed=fd.cleaned_data['Lit']

        pt.casp="Cherigie"
        r.rdvtime= fd.cleaned_data['Date']
        r.hr = fd.cleaned_data['Heur']
        r.mn = fd.cleaned_data['Minute']
        r.paid = fd.cleaned_data['Prix']
      #  r.prixprop = fd.cleaned_data[' Pix_propose']
       # r.nature = fd.cleaned_data[' Nature_Chirugie']
        r.dr=pt.drid
       # pt.rdv.title = fd.cleaned_data['cas']

        pt.save()
        r.save()

        msg = 'data is saved'
        return redirect('ts')

    context = {'formreg': fd,

               'msg': msg
    }
    return render(request, 'ajoutpatop.html', context)
@login_required(login_url='index')


def DrAjoutPatOp(request):
    fd=forms.AddOperatedPatient(request.POST or None)
    dt=date.today()

    msg = ''
    if fd.is_valid():
        pt= models.Patient()

       # r=models.Event(pp=pt.objects.get(auto_increment_id=pt.auto_increment_id))
        r=models.Rdv()
        pt.isop=True
        pt.firstname = fd.cleaned_data['Prenom']
        pt.lastname = fd.cleaned_data['Nom']
        pt.age_patient = fd.cleaned_data['Age']
        pt.phonep = fd.cleaned_data['Phone']
        pt.addressp = fd.cleaned_data['Adresse']
        r.pp=pt
        pt.drid = fd.cleaned_data['Medcin']
        pt.currentstate = fd.cleaned_data['Cas']
        pt.nature=fd.cleaned_data['Nature_Chirugie']
        pt.prixprop=fd.cleaned_data['Pix_propose']
        pt.prix=fd.cleaned_data['Prix']
        pt.orient=fd.cleaned_data['Oriente']
        pt.bed=fd.cleaned_data['Lit']

        pt.casp="Cherigie"
        r.rdvtime= fd.cleaned_data['Date']
        r.hr = fd.cleaned_data['Heur']
        r.mn = fd.cleaned_data['Minute']
        r.paid = fd.cleaned_data['Prix']
      #  r.prixprop = fd.cleaned_data[' Pix_propose']
       # r.nature = fd.cleaned_data[' Nature_Chirugie']
        r.dr=pt.drid
       # pt.rdv.title = fd.cleaned_data['cas']

        pt.save()
        r.save()

        msg = 'data is saved'
        return redirect('pd')

    context = {'formreg': fd,

               'msg': msg
    }
    return render(request, 'draddpatp.html', context)
@login_required(login_url='index')



def AddRdv (request, pk):
    fd = forms.addrdv(request.POST or None)
    ptt = models.Patient.objects.get(auto_increment_id=pk)
    dt = date.today()

    if fd.is_valid():
         # r=models.Event(pp=pt.objects.get(auto_increment_id=pt.auto_increment_id))
        r = models.Rdv()
        r.title = fd.cleaned_data['Prestation']
        r.description = fd.cleaned_data['Commentaire']
        r.rdvtime = fd.cleaned_data['rdvtime']

        r.hr=fd.cleaned_data['Heur']
        r.mn=fd.cleaned_data['Minute']
        r.paid = fd.cleaned_data['Prix']

        r.dr=ptt.drid

        r.pp = ptt
        r.save()
        return redirect('allrdvs')

    context = {'formi': fd }
    return render(request, 'addrdv.html', context)

@login_required(login_url='index')

def AddTime (request):

    fd = forms.addts(request.POST or None)
    if fd.is_valid():
        ts = models.TimeSlot()
        ts.h = fd.cleaned_data['H']
        ts.m = fd.cleaned_data['M']
        ts.save()
    v = date.today()
    es="     "
    dt = v.day
    dm = v.month
    dy = v.year
    tss = models.TimeSlot.objects.all()
    dd = models.Dctr.objects.all()
    dc=''


    a = "Confirme"
    b = "Non conf"
    c = "Present"
    d = "Absent"

    dv=models.Rdv.objects.all()
   # dv=models.Rdv.objects.filter(rdvtime__day=dt, rdvtime__month=dm, rdvtime__year=dy )
    for hal in dv:
        {'fff': hal}

    context = {'formi': fd, 'ts':tss , 'd':dd, 'v':v, 'dv':dv, 'a':a, 'b':b, 'c':c, 't':d, 'es':es,  "data" : [dd]}
    return render(request, 'timeslot.html', context)

@login_required(login_url='index')

@login_required(login_url='index')
def TimeSlotDoctor (request):

    fd = forms.addts(request.POST or None)
    usr=request.user
    if fd.is_valid():
        ts = models.TimeSlot()
        ts.h = fd.cleaned_data['H']
        ts.m = fd.cleaned_data['M']
        ts.save()
    v = date.today()
    dt = v.day
    dm = v.month
    dy = v.year
    tss = models.TimeSlot.objects.all()
    dd = models.Dctr.objects.get( user_id=usr.id)
    a = "Confirme"
    b = "Non conf"
    c = "Present"
    d = "Absent"
    #dv=models.Rdv.objects.filter(dr=usr.id)
    dv=models.Rdv.objects.filter(rdvtime__day=dt, rdvtime__month=dm, rdvtime__year=dy)
    for hal in dv:
        {'fff': hal}

    context = {'formi': fd, 'ts':tss , 'd':dd, 'v':v, 'dv':dv, 'a':a, 'b':b, 'c':c, 't':d}
    return render(request, 'timeslotdr.html', context)

@login_required(login_url='index')

def TimeSlotAssistsnt (request):

    fd = forms.addts(request.POST or None)
    usr=request.user
    ass=models.Assistant.objects.get(user_id=usr)

    if fd.is_valid():
        ts = models.TimeSlot()
        ts.h = fd.cleaned_data['H']
        ts.m = fd.cleaned_data['M']
        ts.save()

    bbb=ass.drid
    v = date.today()
    dt = v.day
    dm = v.month
    dy = v.year
    tss = models.TimeSlot.objects.all()
    dd = models.Dctr.objects.all()
    a = "Confirme"
    b = "Non conf"
    c = "Present"
    d = "Absent"
    dv=models.Rdv.objects.all()
   # dv=models.Rdv.objects.filter(rdvtime__day=dt, rdvtime__month=dm, rdvtime__year=dy )


    context = {'formi': fd, 'ts':tss , 'd':dd, 'v':v, 'dv':dv, 'a':a, 'b':b, 'c':c, 't':d, 'bbb':bbb, 'ass':ass}
    return render(request, 'assistant.html', context)

@login_required(login_url='index')

def AddMed (request):
    form = forms.AddMedecines()
    if request.method == 'POST':
        form = forms.AddMedecines(request.POST)
        if form.is_valid():
            food = form.save()
            food.save()
            return redirect('medecines')

    context = {'form': form}
    return render(request, 'addmed.html', context)


@login_required(login_url='index')

def Addfood (request):
     form = forms.AddFood()
     if request.method == 'POST':
         form = forms.AddFood(request.POST)
         if form.is_valid():
             food = form.save()
             food.save()
             return redirect('medecines')


     context = {'form': form}
     return render(request, 'addfood.html', context)


@login_required(login_url='index')

def AddUsed (request):
     form = forms.AddUsed()
     if request.method == 'POST':
         form = forms.AddUsed(request.POST)
         if form.is_valid():
             usd = form.save()
             usd.save()
             return redirect('medecines')


     context = {'form': form}
     return render(request, 'addused.html', context)


'''''

def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
        )
        #return HttpResponseRedirect(reverse("calendar"))
    return render(request, "register.html", {"form": form})
    '''

def loginUser(request):
    page = 'login'
    if request.method == 'POST':



        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_doctor== False and user.is_assistant == False:
                login(request, user)
                return redirect('patient')


    return render(request, 'login.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('index')


def addadmin(request):


    form = CustomUserCreationForm()
    models.User.is_doctor == False
    models.User.is_assistant == False
    models.User.is_admin == True

    if request.method == 'POST':
        models.User.is_admin == True
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            models.User.is_admin == True
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('patient')

    context = {'form': form}
    return render(request, 'addadmin.html', context)

def registerUser(request):
    page = 'reg'

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('patient')

    context = {'form': form, 'page': page}
    return render(request, 'login.html', context)


def search(request):


    if request.method == "POST":

        searched = request.POST['searched']

        pts = models.Patient.objects.filter(lastname=searched)

        return render(request, 'search.html', {'searched': searched, 'pts': pts})
    else:
        return render(request, 'search.html')


def drsearch(request):
    usr = request.user
    if request.method == "POST":

        searched = request.POST['searched']
        pts = models.Patient.objects.filter(lastname=searched, drid=usr.id)

        return render(request, 'drsearch.html', {'searched': searched, 'pts': pts})
    else:
        return render(request, 'drsearch.html')
@login_required(login_url='index')
def deletePatient(request, pk):
	order = models.Patient.objects.get(auto_increment_id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('patient')

	context = {'item':order}
	return render(request, 'delete.html', context)
@login_required(login_url='index')
def updatePatient(request, pk):

	pp = models.Patient.objects.get(auto_increment_id=pk)

	form = forms.PatForm(instance=pp)

	if request.method == 'POST':
		form = forms.PatForm(request.POST, instance=pp)

		if form.is_valid():
			form.save()

			return redirect('patient')

	context = {'form':form, 'pp':pp}
	return render(request, 'test.html', context)




def updateRdv(request, p):
    rd = models.Rdv.objects.get(id=p)
    f = forms.updateRdv(instance=rd)

    if request.method == 'POST':
        f = forms.updateRdv(request.POST, instance=rd)

        if f.is_valid():
            f.save()
            return redirect('patient')


    context = {'f': f, 'ss':rd}
    return render(request, 'updaterdv.html', context)

    """""
    if request.method == 'POST':
        t.paid = request.POST["po"]

        t.save(update_fields=["paid"])
    context={'ff':f}
    return render(request, 'rdvs.html', context)
    """

@login_required(login_url='index')

def deleteDoctor(request, pk):
	dr = models.Dctr.objects.get(user_id=pk)
	if request.method == "POST":
		dr.delete()
		return redirect('Drs')

	context = {'item':dr}
	return render(request, 'deletedr.html', context)

def deleteAssistant(request, pk):
	dr = models.Assistant.objects.get(user_id=pk)
	if request.method == "POST":
		dr.delete()
		return redirect('assistants')

	context = {'item':dr}
	return render(request, 'deleteass.html', context)

@login_required(login_url='index')

def deleteRdv(request, pk):
	rdv = models.Rdv.objects.get(id=pk)
	if request.method == "POST":
		rdv.delete()

	context = {'item':rdv}
	return render(request, 'rdvs.html', context)

def deletets(request, pk):
	rdv = models.TimeSlot.objects.get(id=pk)
	if request.method == "POST":
		rdv.delete()


	context = {'item':rdv}
	return render(request, 'timeslot.html', context)


def deleteMed(request, pk):
	mmmm = models.medecines.objects.get(id=pk)
	if request.method == "POST":
	    mmmm.delete()

	return redirect('medecines')
def deleteFood(request, p):
	foods = models.food.objects.get(id=p)
	if request.method == "POST":
		foods.delete()


	return redirect('medecines')

def deleteUsed(request, p):
	foods = models.food.objects.get(id=p)
	if request.method == "POST":
		foods.delete()


	return redirect('medecines')
def login_view(request):
    form = forms.LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if models.user.is_assistant==True :

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_admin:
                    login(request, user)
                    return redirect('drreg')
                elif user is not None and user.is_customer:
                    login(request, user)
                    return redirect('patient')

                else:
                    msg= 'invalid credentials'
            else:
                msg = 'error validating form'
        else:
            msg = 'Utilisateur peut etre pas assistant'
    return render(request, 'loginass.html', {'form': form, 'msg': msg})


class doctor_register(CreateView):

    model = models.User
    form_class = forms.Drreg
    template_name = '../templates/drreg.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('Drs')

class reciptionist_register(CreateView):

    model = models.User
    form_class = forms.Recreg
    template_name = '../templates/addrec.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('ts')

class assistant_register(CreateView):
    msg=' '
    model = models.User
    form_class = forms.Assistant
    template_name = '../templates/assreg.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('assistants')

class draddass(CreateView):
    msg=' '
    model = models.User
    form_class = forms.Assistant
    template_name = '../templates/assreg.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('pd')

def getrdv(request, pk):
    #rdv = models.Event.objects.filter(pp=p)

    p = models.Patient.objects.get(auto_increment_id=pk)
    rdv = models.Rdv.objects.filter(pp=p)
    rd = models.Rdv.objects.all()



    context = {'rdv': rdv, 'ppp':p, 'rd':rd}

    return render(request, 'rdvs.html', context)

def login_request(request):


    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                if user.is_doctor == True:
                    login(request,user)
                    return redirect('pd')
                else:
                    messages.error(request, "User is not Doctor")


            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")

    return render(request, '../templates/loginmed.html',
    context={'form':AuthenticationForm()})
def login_ass(request):


    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :

                if user.is_assistant == True:
                    login(request, user)
                    return redirect('tsa')
                else:
                    messages.error(request, "User is not Assistant")



            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")

    return render(request, '../templates/loginass.html',
    context={'form':AuthenticationForm()})

def login_rec(request):


    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :

                if user.is_receptionist == True:
                    login(request, user)
                    return redirect('ts')
                else:
                    messages.error(request, "User is not Receptionist")



            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")

    return render(request, '../templates/loginrec.html',
    context={'form':AuthenticationForm()})
def logout_view(request):
    logout(request)
    return redirect('/')


class CalendarView(generic.ListView):
    model = Rdv
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        m = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(m)
        context['next_month'] = next_month(m)



        # Instantiate our calendar class with today's year and date
        cal = Calendar(m.year, m.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        dt = date.today()
        mt = dt.month

        rdv = models.Rdv.objects.filter( rdvtime__month=m.month)
        total = 0
        for instance in rdv:
            total += instance.paid
            print(total)
        context['d'] = rdv
        context['total'] = total
        # return HttpResponse('display all students here')


        return context



def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(m):
    first = m.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(m):
    days_in_month = calendar.monthrange(m.year, m.month)[1]
    last = m.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

