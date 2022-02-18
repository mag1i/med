"""medapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import url
from med.views import Index, updateRdv, DailyIncome, MonthIncome, YearIncome, MonthTotal, CalendarView, YearTotal, \
    AddTime, deletets, isinn, AjoutPatOp, AddUsed, deleteUsed, Used, PatientsOp, PatientsNonOp, login_view, isinnop, \
    isinntout, PatientsOfDoctor, reciptionist_register, login_ass, login_rec, DailyDr, MonthDr, YearDr, TimeSlotDoctor, \
    isinnts, TimeSlotAssistsnt, Assistants, WeekTotal, WeeklyIncome, WeeklyDr, chemin, PatientDetails, floor, op, \
    removeBed, draddpat, DrAjoutPatOp, deleteAssistant, drsearch, draddass

from med.views import Patients,  deleteDoctor,  addadmin, AddMed, Addfood, Medecines, Food, getrdv, Allrdvs, deleteRdv, deleteMed, deleteFood, AddRdv
#from med.views import CalendarView, AllEventsListView, EventEdit, RunningEventsListView,
from med.views import Doctors
from med.views import Register, test, loginUser, logoutUser, registerUser, deletePatient, updatePatient, search, doctor_register, login_request, assistant_register, Doctors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Index, name='index'),
    path('patient/',Patients, name='patient'),
    path('patientop/',PatientsOp, name='patientop'),
    path('patientm/',PatientsNonOp, name='patientm'),
    path('doctor/',Doctors, name='doctor'),
    path('register/',Register, name='register'),
    path('test/',test, name='test'),
    path('login/',loginUser, name='login'),
    path('loginass/',login_ass, name='loginass'),
    path('logout/',logoutUser, name='logout'),
    path('delete/<str:pk>/',deletePatient, name='delete'),
    path('deleteRdv/<str:pk>/',deleteRdv, name='deleteRdv'),
    path('deleteFood/<str:p>/',deleteFood, name='deleteFood'),
    path('deleteMed/<str:pk>/',deleteMed, name='deleteMed'),
    path('deleteused/<str:pk>/',deleteUsed, name='deleteused'),
    path('deleteass/<str:pk>/',deleteAssistant, name='deleteass'),
    path('updaterdv/<str:p>/',updateRdv, name='updaterdv'),
    path('update/<str:pk>/',updatePatient, name='update'),

    path('getrdv/<str:pk>/',getrdv, name='getrdv'),
    path('addrdv/<str:pk>/',AddRdv, name='addrdv'),
    path('drrdv/<str:did>/',DailyIncome, name='drrdv'),
    path('weekincome/<str:did>/',WeeklyIncome, name='weekincome'),
    path('monthincome/<str:did>/',MonthIncome, name='monthincome'),
    path('yearincome/<str:did>/',YearIncome, name='yearincome'),
    path('search/',search, name='search'),
    path('drsearch/',drsearch, name='drsearch'),
    path('drreg/', doctor_register.as_view(), name='drreg'),
    path('assreg/', assistant_register.as_view(), name='assreg'),
    path('loginmed/', login_request, name='loginmed'),
    path('logirec/', login_rec, name='loginrec'),
    path('Drs/', Doctors, name='Drs'),
    path('reg/', registerUser, name='reg'),
    path('deletedr/<str:pk>/', deleteDoctor, name='deletedr'),
    path('addadmin/', addadmin, name='addadmin'),
    path('addfood/', Addfood, name='addfood'),
    path('addused/', AddUsed, name='addused'),
    path('addmed/', AddMed, name='addmed'),
    path('medecines/', Medecines, name='medecines'),
    path('medecines/', Food, name='medecines'),
    path('used/', Used, name='used'),
    path('allrdvs/', Allrdvs, name='allrdvs'),
    path('monthtotal/', MonthTotal, name='monthtotal'),
    path('weektotal/', WeekTotal, name='weektotal'),
    path('calendar/',  CalendarView.as_view(), name='calendar'),
    path('yt/',  YearTotal, name='yt'),
    path('ts/',  AddTime, name='ts'),
    path('tsd/',  TimeSlotDoctor, name='tsd'),
    path('tsa/',  TimeSlotAssistsnt, name='tsa'),
    path('deletets/<str:pk>/',  deletets, name='deletets'),
    path('istrue/<str:p>',  isinn, name='istrue'),
    path('istruets/<str:p>',  isinnts, name='istruets'),
    path('ist/<str:p>',  isinnop, name='ist'),
    path('istt/<str:p>',  isinntout, name='istt'),
    path('patdet/<str:p>',  PatientDetails, name='patdet'),
    path('apo',  AjoutPatOp, name='apo'),
    path('pd',  PatientsOfDoctor, name='pd'),
    path('rr',  reciptionist_register.as_view(), name='rr'),
    path('dass',  draddass.as_view(), name='dass'),
    path('dd',  DailyDr, name='dd'),
    path('md',  MonthDr, name='md'),
    path('wd',  WeeklyDr, name='wd'),
    path('yd',  YearDr, name='yd'),
    path('assistants',  Assistants, name='assistants'),
    path('chemin',  chemin, name='chemin'),
    path('floor',  floor, name='floor'),
    path('op',  op, name='op'),
    path('rb/<str:p>',  removeBed, name='rb'),
    path('draddpat',  draddpat, name='draddpat'),
    path('dapo',  DrAjoutPatOp, name='dapo'),


    #path("calendars/", CalendarViewNew.as_view(), name="calendars"),
    #path("calendar/", CalendarView.as_view(), name="calendar"),
    #path("event/new/", create_event, name="event_new"),
    #path("event/edit/<int:pk>/", EventEdit.as_view(), name="event_edit"),



   # path("all-event-list/", AllEventsListView.as_view(), name="all_events"),
   # path(   "running-event-list/",  RunningEventsListView.as_view(),  name="running_events",  ),



]
