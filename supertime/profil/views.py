from django.shortcuts import render, get_list_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Horaire,Poste, Salaire,Zklecteur,Personnel,Attendance
from .forms import HoraireForm,ZKTecoForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone,date,time
from django.core.paginator import Paginator
from django.db.models import Count, Q
import subprocess
from zk import ZK, const
import threading
from threading import Thread
import os
import sys
import asyncio
from django.utils import timezone
import calendar
from django.db.models import Min, Max
from dateutil.relativedelta import relativedelta




CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)



@login_required(login_url="/account/login_admin/")
def terminal_list(request):
    lecteurs = Zklecteur.objects.all()
    status_list = []
    messages = []

    def check_status(lecteur):
        zk = ZK(lecteur.ip_adresse, lecteur.n_port, timeout=1)
        conn = None
        status = False

        try:
            conn = zk.connect()
            status = conn.is_connect
            status_list.append(status)
        except Exception as e:
            messages.append("Erreur de connexion avec le lecteur {}: {}".format(lecteur.id, e))
        finally:
            if conn is not None and conn.is_connect:
                conn.disconnect()

    def check_all_statuses():
        threads = []
        for lecteur in lecteurs:
            thread = threading.Thread(target=check_status, args=(lecteur,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    check_all_statuses()

    return render(request, 'profil/liste_drive.html', {'zklect': lecteurs, 'status_list': status_list, 'messages': messages})


#-------------------------------------------------------------------------------------------------------------#
@login_required(login_url="/account/login_admin/")
def add_users(request, lecteur_id):
    statut=None
    lecteurs = Zklecteur.objects.get(pk=lecteur_id)
    conn = None
    zk = ZK(lecteurs.ip_adresse, port=lecteurs.n_port, timeout=2)
    try:
        conn = zk.connect()
        print('Disabling device ...')
        conn.disable_device()
        print('--- Get User ---')
        users = conn.get_users()
        
        for user in users:
            zkteco_username = user.name
            zkteco_user_id = user.user_id
            pw = user.password
            print(zkteco_user_id, zkteco_username, pw)
            
            try:
                django_user = User.objects.get(username=zkteco_user_id)
                # Si l'utilisateur existe, mettez à jour ses informations
                django_user.zkteco_user_id = zkteco_user_id
                django_user.save()
                pass
            except User.DoesNotExist:
                # Si l'utilisateur n'existe pas, créez un nouvel utilisateur Django
                django_user = User.objects.create_user(username=zkteco_user_id,password=pw)
                django_user.zkteco_user_id = zkteco_user_id
                django_user.save()
                if user.privilege == const.USER_ADMIN:  # Assurez-vous que votre appareil ZKTeco fournit cette information
                    django_user.is_superuser = True
                    django_user.save()
               
    
            
            # Vérifier le statut de l'utilisateur dans le lecteur
            
                
        print('Enabling device ...')
        conn.enable_device()
            
    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if conn is not None and conn.is_connect:
            conn.disconnect()
            
    return render(request, "profil/liste_user.html", {'statut':statut})


@login_required(login_url="/account/login_admin/")
def raw_data(request):
    attendance_list=Attendance.objects.order_by('-date','-heure_punch')
    if request.method == "GET":
        
        # date_search=request.GET.get('date_search')
        personnel_search=request.GET.get('user_search')
        if personnel_search is not None: 
            
            attendance_list = Attendance.objects.filter(personnel_a=personnel_search)
          
    paginator = Paginator(attendance_list, 10)  # Paginer la liste avec 10 employés par page
    
    page_number = request.GET.get('page')  # Récupérer le numéro de page depuis les paramètres GET
    page_obj = paginator.get_page(page_number)  # Obtenir l'objet Page pour la page demandée
    context = {'page_obj': page_obj,
               
               
               }
    return render(request,'profil/logs.html',context)



@login_required(login_url="/account/login_admin/")
def user_list(request):
    users=User.objects.all()
    return render(request,'profil/liste_user.html',{"users":users})



@login_required(login_url="/account/login_admin/")
def get_log_data(request, lecteur_id):
    lecteurs = Zklecteur.objects.get(pk=lecteur_id)
    zk = ZK(lecteurs.ip_adresse, lecteurs.n_port, timeout=2)
    try:
        conn = zk.connect()
        print('Disabling device ...')
        conn.disable_device()
        print('--- Get Attendance ---')
        attendance = conn.get_attendance()
        print(type(attendance))
        print(attendance)

        for user in attendance:
            id_atendance = user.uid
            check_heure = user.timestamp
            status_a = user.status
            user_id = user.user_id
            punch_attendance = user.punch
            try:
                existing_attendance = Attendance.objects.filter(id_att=id_atendance).first()
                if existing_attendance:
                    Attendance.objects.get(id_att=id_atendance)
                    # Check if the model of the device matches
                    if existing_attendance.lecteur.model_drive == lecteurs.model_drive:
                        print("Matching model, passing.")
                        continue
                    else:
                        user_id_zk =User.objects.get(username=user_id)
                        pk_user=user_id_zk.pk
                        user_c = Personnel.objects.get(user=pk_user)
                        # Si le Personnel existe, crée une nouvelle instance du modèle Attendance
                        django_user = Attendance.objects.create(id_att=id_atendance, personnel_a=user_c, date=check_heure.date(), status=status_a, punch=punch_attendance, heure_punch=check_heure,lecteur=lecteurs.pk)
                        django_user.save()
                else:
                    user_id_zk =User.objects.get(username=user_id)
                    pk_user=user_id_zk.pk
                    user_c = Personnel.objects.get(user=pk_user)
                    # Si le Personnel existe, crée une nouvelle instance du modèle Attendance
                    django_user = Attendance.objects.create(id_att=id_atendance, personnel_a=user_c, date=check_heure.date(), status=status_a, punch=punch_attendance, heure_punch=check_heure,lecteur=lecteurs.pk)
                    django_user.save()

                # try:
                #     # Tentative de récupération de l'objet Attendance avec l'identifiant spécifié
                #     django_user = Attendance.objects.get(id_att=id_atendance)
                #     pass
                # except Attendance.DoesNotExist:
                    
                #         # Tentative de récupération de l'objet Personnel associé à l'identifiant
                #     user_id_zk =User.objects.get(username=user_id)
                #     pk_user=user_id_zk.pk
                #     user_c = Personnel.objects.get(user=pk_user)
                # # Si le Personnel existe, crée une nouvelle instance du modèle Attendance
                #     django_user = Attendance.objects.create(id_att=id_atendance, personnel_a=user_c, date=check_heure.date(), status=status_a, punch=punch_attendance, heure_punch=check_heure)
                #     django_user.save()
                    
            except:
                pass
            
    
        print('Enabling device ...')
        conn.enable_device()
    except Exception as e:
        print("Processus interrompu :", e)
    finally:
        if conn is not None and conn.is_connect:
            conn.disconnect()




    message = "Données téléchargées avec succès"
    return redirect('profil:liste_drive')

@login_required(login_url="/account/login_admin/")  
def delete_drive(request,lecteur_id):
    lecteur = Zklecteur.objects.get(pk=lecteur_id)
    lecteur.delete()
    return redirect("profil:liste_drive")



@login_required(login_url="/account/login_admin/")
def edit_drive(request,lecteur_id):
    lecteur = Zklecteur.objects.get(pk=lecteur_id)
    if request.method == 'POST':
        form = ZKTecoForm(request.POST,instance=lecteur)
        if form.is_valid():
            form.save()
            return redirect("profil:liste_drive")
    else:
        form = ZKTecoForm(instance=lecteur)
    
    return render(request,"profil/modife_drive.html",{"form": form})



@login_required(login_url="/account/login_admin/")
def dashboard(request):
    # maintenant=datetime.now()
    maintenant=datetime.now()

    annee = maintenant.year
    mois = mois = maintenant.month

    # Nombre de jours à récupérer
    nb_jours = calendar.monthrange(annee, mois)[1]
    nombre_jours = nb_jours

    # Liste pour stocker les dates
    dates_du_jour = []

    # Récupération des dates du jour
    # aujourd_hui = datetime.now().date()
    aujourd_hui = date(annee, mois, 1)
    for i in range(nombre_jours):
        date_day = aujourd_hui + timedelta(days=i)
        dates_du_jour.append(date_day)

    # Affichage des dates
    # for date in dates_du_jour:
    #      print(date)

    date_j = date.today()
    attendance_dates = Horaire.objects.values_list('date_check', flat=True).distinct()
    # Séparer les dates et les nombres d'employés en deux listes distinctes
    dates_list = []
    counts_list = []
    # i=30
    # day_nbr = date.today().strftime("%d")
    # while i == 30:
    for entry in  dates_du_jour:
            dates_list.append(str(entry.strftime("%d-%m-%Y")))
            present = Horaire.objects.filter(start_time__startswith=entry).count()
            counts_list.append(int(present))

    # i +=1
    total_employees = Personnel.objects.count()
    
    # Compter le nombre d'employés présents à la date donnée
    employees_present = Horaire.objects.filter(start_time__startswith=date_j).count()
    # Calculer le nombre d'employés absents
    employees_absent = total_employees - employees_present

    context={
         'total_employees':total_employees,
         'p':employees_present,
         'a':employees_absent,
        #  'dates': dates_du_jour , 
        'dates':dates_list,
        #  'nbre_present': present_p,
        'nbrepresent':counts_list,
      
         }



    return render(request,"profil/dashboard.html",context)
    # return render(request, 'profil/liste_drive.html')


def index(request):
   
    return render(request,"profil/index.html")


def first_time_user(request):
    # Vérifier si un utilisateur existe déjà dans la base de données
    existing_users = User.objects.all()
    
    if existing_users:
        # Si des utilisateurs existent, rediriger vers une autre vue ou effectuer toute autre action
        return render(request,"profil/index.html")
    else:
        if request.method == 'POST':
            # Récupérer les données du formulaire
            username = request.POST['username']
            password = request.POST['password']
            
            # Créer un nouvel utilisateur
            User.objects.create_user(username=username, password=password)
            
            # Rediriger vers une autre vue ou effectuer toute autre action
            return render(request,"profil/index.html")
    
    # Afficher le formulaire d'inscription pour le premier utilisateur
    return render(request, 'accounts/register.html')

# Poste
@login_required(login_url="/account/login_admin/")
def add_poste(request):
   if request.method == 'POST':
       as_poste = request.POST.get('as_poste')
       poste = request.POST.get('poste')
       salary = request.POST.get('salary')
       debut = request.POST.get('debut')
       tolerance_time = request.POST.get('tolerance_time')
       fin = request.POST.get('fin')
       time_work = request.POST.get('time_work')

       poste = Poste(as_poste = as_poste, name_poste = poste, salary = salary, start_time = debut,  tolerance_time = tolerance_time,end_time = fin, time_work = time_work)
       poste.save()
       return redirect('profil:liste_poste')
   return render(request, 'profil/save_poste.html')

@login_required(login_url="/account/login_admin/")
def add_personnel(request):
        if request.method == 'POST':
                nom = request.POST.get('nom')
                email = request.POST.get('email')
                prenom = request.POST.get('prenom')
                gender = request.POST.get('gender')
                heure_fixe = request.POST.get('heure_fixe')
                salary = request.POST.get('salary')
                poste_id = request.POST.get('poste')
                user_id = request.POST.get('user_id')
                time_a = request.POST.get('time_a')
                tolerance_time = request.POST.get('tolerance_time')
                time_s = request.POST.get('time_s')
                photo = request.FILES.get('photo')
                # Récupérer le poste sélectionné à partir de son ID
                if poste_id or user_id:
                    try:
                        poste = Poste.objects.get(pk=poste_id)
                        users = User.objects.get(pk=user_id)
                    except Poste.DoesNotExist or User.DoesNotExist:
                        # Gérer l'erreur si le poste n'existe pas
                        return redirect('error')

                personnel = Personnel(name=nom,email=email,first_name=prenom, gender=gender,
                                      time_works=heure_fixe,salary=salary, start_time = time_a, tolerance_time = tolerance_time, end_time = time_s,poste=poste,user=users, photo = photo)
                personnel.save()
                return redirect('profil:liste_employe')
        else:
            users_not_linked = User.objects.exclude(personnel__isnull=False)

        return render(request, 'profil/save_employe.html', {"postes":Poste.objects.all(),"users":users_not_linked} )

def edit_poste(request, poste_id):
    try:
        poste = Poste.objects.get(pk=poste_id)  # Get the position to modify
    except Poste.DoesNotExist:
        # Handle the case where the position is not found
        return redirect('profil:liste_poste')  # Redirect to list view on error

    if request.method == 'POST':
        as_poste = request.POST['as_poste']
        name_poste = request.POST['poste']
        salary = request.POST['salary']  # Assuming this is the intended field name
        debut = request.POST['debut']
        tolerance_time = request.POST['tolerance_time']
        fin = request.POST['fin']
        time_work = request.POST['time_work']

        poste.as_poste = as_poste
        poste.name_poste = name_poste
        poste.salary= salary
        poste.start_time = debut
        poste.tolerance_time = tolerance_time
        poste.end_time = fin
        poste.time_work = time_work
        poste.save()

        return redirect('profil:liste_poste')  # Redirect to list view on successful update

    context = {'poste': poste}
    return render(request, 'profil/modife_employe.html', context)

@login_required(login_url="/account/login_admin/")
def edit_personnel(request, personnel_id):
    try:
        personnel = Personnel.objects.get(id=personnel_id)
    except Personnel.DoesNotExist:
        return redirect('profil:liste_employe')
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        prenom = request.POST.get('prenom')
        gender = request.POST.get('gender')
        heure_fixe = request.POST.get('heure_fixe')
        salary = request.POST.get('salary')
        poste_id = request.POST.get('poste')
        time_a = request.POST.get('time_a')
        tolerance_time = request.POST.get('tolerance_time')
        time_s = request.POST.get('time_s')
        user_id = request.POST.get('user_id')
        photo = request.FILES.get('photo')  # Utiliser request.FILES pour récupérer le fichier téléchargé

        if poste_id:
            try:
                poste = Poste.objects.get(pk=poste_id)
            except Poste.DoesNotExist:
                return redirect('error')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return redirect('error')

        # Mettre à jour les données du personnel
        personnel.name = nom
        personnel.email = email
        personnel.first_name = prenom
        personnel.gender = gender
        personnel.time_works = heure_fixe
        if salary:
            personnel.salary = salary
        personnel.poste = poste
        personnel.start_time = time_a
        personnel.tolerance_time = tolerance_time
        personnel.end_time = time_s
        personnel.user = user
        if photo:  # Vérifier si une nouvelle photo a été téléchargée
            personnel.photo = photo  # Mettre à jour la photo uniquement si un fichier a été téléchargé
        personnel.save()

        return redirect('profil:liste_employe')
    
    # Filtrer les utilisateurs pour exclure ceux qui sont déjà liés à l'employé
    users = User.objects.filter(Q(personnel__isnull=True) | Q(personnel=personnel))

    context = {
        'personnel': personnel,
        'postes': Poste.objects.all(),
        'users': users
    }
    return render(request, 'profil/modife_employe.html', context)



@login_required(login_url="/account/login_admin/")
def personnel_list(request):
    employee_list = Personnel.objects.all()
    if request.method == "GET":
        
        name=request.GET.get('rechercher')
        if name is not None:
            #employee_list = Personnel.objects.filter(name__icontains=name)
            employee_list = Personnel.objects.filter(name__startswith=name)
    


    paginator = Paginator(employee_list, 10)  # Paginer la liste avec 10 employés par page
    
    page_number = request.GET.get('page')  # Récupérer le numéro de page depuis les paramètres GET
    page_obj = paginator.get_page(page_number)  # Obtenir l'objet Page pour la page demandée
    context = {'page_obj': page_obj,
               
               
               }
    return render(request,"profil/liste_employe.html",context)



@login_required(login_url="/account/login_admin/")
def attendance(request):
    # date_filter=datetime.date()

    # attendance=Horaire.objects.filter(date_d__startswith=date_filter)
    attendance=Horaire.objects.all()
    context={
           'horaires':Horaire.objects.order_by('-date_check','-start_time'),
           }
    return render(request,"profil/attendance.html",context)
    

@login_required(login_url="/account/login_admin/")
def historique(request):
    context={
           'horaires':Horaire.objects.order_by('-date_check','-start_time'),
           }
    return render(request,"profil/historique.html",context)

@login_required(login_url="/account/login_admin/")
def personnel_profil(request,Personnel_id): 
    context = {"Personnels": get_list_or_404(Personnel,pk=Personnel_id),
               
            }
    return render(request, "profil/profil_employe.html", context)
  

@login_required(login_url="/account/login_admin/")
def help(request):
   
    
    return render(request,"Profil/help.html")

@login_required(login_url="/account/login_admin/")
def delete_personnel(request,Personnel_id):
    Personne = Personnel.objects.get(pk=Personnel_id)
    Personne.delete()
    return redirect("profil:liste_employe")

@login_required(login_url="/account/login_admin/")
def delete_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:liste_poste")



@login_required(login_url="/account/login_admin/")
def delete_employees(request):
    if request.method == 'POST':
        selected_employees = request.POST.getlist('selected_employees')
        # Code pour supprimer les employés sélectionnés
        # selected_employees contient une liste des ID des employés sélectionnés
        Personnel.objects.filter(id__in=selected_employees).delete()
        
    
    return redirect('profil:liste_employe')


@login_required(login_url="/account/login_admin/")
def delete_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:liste_poste")

def user_profil(request):
    return render(request, 'profil/profil_user.html')


#@login_required(login_url="/account/login_admin/")
# def edit_Poste(request,Poste_id):
#     poste = Poste.objects.get(pk=Poste_id)
#     if request.method == 'POST':
#         form = PosteForm(request.POST,instance=poste)
#         if form.is_valid():
#             form.save()
#             return redirect("profil:poste")
#     else:
#         form = PosteForm(instance=poste)
    
#     return render(request,"profil/partm1.html",{"form": form})
   

#@login_required(login_url="/account/login_admin/")
# def edit_Personnel(request,Personnel_id):
#     Personnels = Personnel.objects.get(pk=Personnel_id)
#     if request.method == 'POST':
#         form = PersonnelForm(request.POST,instance=Personnels)
#         if form.is_valid():
#             form.save()
#             return redirect("profil:liste_e")
#     else:
#         form = PersonnelForm(instance=Personnels)
    
#     return render(request,"profil/part2.html",{"form": form})
   

@login_required(login_url="/account/login_admin/")
def edit_attendance(request,Horaire_id):
    Personnels = Personnel.objects.get(pk=Horaire_id)
    if request.method == 'POST':
        form = HoraireForm(request.POST,instance=Personnels)
        if form.is_valid():
            form.save()
            return redirect("profil:attendance")
    else:
        form = HoraireForm(instance=Personnels)
   
    return render(request,"profil/save_attendance.html",{"form": form})
    

def calculate_daily_work_hours(personnel, annee, mois):
    # Récupérer toutes les présences de l'employé pour la journée spécifiée
    # horaires = Horaire.objects.filter(personnel=personnel, date_check__startswith=date_month)
    horaires = Horaire.objects.filter(
        personnel=personnel,
        date_check__year=annee,
        date_check__month=mois
    )
    total_work_hours = timedelta()  # Initialiser la durée totale à zéro
    total_work_hours_time = timedelta()  # Initialiser la durée totale à zéro
    total_work_hours_all= timedelta()  # Initialiser la durée totale à zéro
    
    for horaire in horaires:
        if isinstance(horaire, datetime):  # Vérifier si horaire est un objet datetime
            duration_timedelta = timedelta(hours=horaire.calculate_duration().hour, minutes=horaire.calculate_duration().minute, seconds=horaire.calculate_duration().second)
            total_work_hours += duration_timedelta
        elif isinstance(horaire, time):  # Vérifier si horaire est un objet time
            total_work_hours_time += horaire.calculate_duration()
    total_work_hours_all += total_work_hours+total_work_hours_time
    return total_work_hours_all


def calculate_daily_salary(personnel, annee, mois):
    total_work_hours = calculate_daily_work_hours(personnel, annee, mois)
    daily_salary = (total_work_hours.total_seconds() / 3600 *  personnel.salary)/personnel.time_works #n

    return daily_salary

@login_required(login_url="/account/login_admin/")
def personnel_salary(request, Personnel_id):
    # Récupérer la date actuelle
    current_date = datetime.now()
    # Formater la date selon le format Année-Mois
    date_month_actuel = current_date.strftime("%Y-%m")
    # Déterminez le premier jour du mois actuel
    first_day_of_month = current_date.replace(day=1)
    # Déterminez le dernier jour du mois actuel
    last_day_of_month = first_day_of_month + relativedelta(months=1) - relativedelta(days=1)
    date_actuelle = datetime.now()
    annee = date_actuelle.year
    mois = date_actuelle.month
    
    
    personnel = Personnel.objects.get(id=Personnel_id)
    
    daily_work_hours = calculate_daily_work_hours(personnel, annee, mois)
    daily_salary = calculate_daily_salary(personnel, date_month_actuel)
    
    today = datetime.today()
    today = today.strftime("%Y-%m-%d")
    
    if today == first_day_of_month.strftime("%Y-%m-%d"):
        salaire_month = Salaire(date_month=date_month_actuel, personnel=personnel, montant=daily_salary)
        salaire_month.save()
    else:
        pass
    
    context = {
        'personnel': personnel,
        'daily_work_hours': daily_work_hours,
        'daily_salary': daily_salary,
        'first_month': first_day_of_month,
        'last_month': last_day_of_month
    }

    return render(request, 'profil/salaire.html', context)


@login_required(login_url="/account/login_admin/")
def poste_list(request):
    context={'postes':Poste.objects.all(),}
    return render(request, "profil/liste_poste.html",context)
   



 # ajoute un lecteur   

@login_required(login_url="/account/login_admin/")
def add_drive(request):
    if request.method == 'POST':
       form = ZKTecoForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect("profil:liste_drive")
    else:
       form = ZKTecoForm()
    
    return render(request, "profil/add_drive.html", {'form': form})

@login_required(login_url="/account/login_admin/")    
def get_attendance_data(request):
    # Récupérer tous les enregistrements de la table Attendance
    attendances = Attendance.objects.all()

    for attendance in attendances:
        # Récupérer la date et le personnel de l'entrée d'assistance
        date = attendance.date.date()  # Récupérer uniquement la date sans l'heure
        personnel = attendance.personnel_a
        punch = attendance.punch

        # Récupérer tous les enregistrements pour ce personnel et cette date
        attendance_records = Attendance.objects.filter(personnel_a=personnel, date__date=date)

        # Si des enregistrements existent pour ce jour et ce personnel
        if attendance_records.exists():
            # Trier les enregistrements par heure_punch
            sorted_records = attendance_records.order_by('heure_punch')

            # Associer le premier heure_punch à arrival time et le dernier à end_time
            first_punch = sorted_records.first()
            last_punch = sorted_records.last()

            # Si les heures de premier et dernier punch sont égales, 
            # définir last_punch.heure_punch à None et last_punch.status à None
            if first_punch.heure_punch == last_punch.heure_punch:
                last_punch.heure_punch = None
                last_punch.status = None

            # Récupérer ou créer tous les objets Horaire correspondant à ces critères
            horaires = Horaire.objects.filter(date_check=date, personnel=personnel)

            if horaires.exists():
                # Il existe déjà un ou plusieurs objets Horaire pour cette date et ce personnel
                for horaire in horaires:
                    # Mettre à jour les champs arrival time et end_time
                    horaire.start_time = first_punch.heure_punch
                    horaire.end_time = last_punch.heure_punch

                    # Mettre à jour les champs status et statute
                    if first_punch.status == "1":
                        horaire.status = "fingerprint"
                    elif first_punch.status == "3":
                        horaire.status = "pass word"
                    elif first_punch.status == "4":
                        horaire.status = "card"
                    
                    if last_punch.status == "1":
                        horaire.statute = "fingerprint"
                    elif last_punch.status == "3":
                        horaire.statute = "pass word"
                    elif last_punch.status == "4":
                        horaire.statute = "card"
                    
                    horaire.save()
            else:
                # Aucun objet Horaire trouvé, créer un nouvel objet Horaire
                horaire = Horaire.objects.create(
                    date_check=date,
                    start_time=first_punch.heure_punch,
                    end_time=last_punch.heure_punch,
                    personnel=personnel
                )

                # Mettre à jour les champs status et statute
                if first_punch.status == "1":
                    horaire.status = "fingerprint"
                elif first_punch.status == "3":
                    horaire.status = "pass word"
                elif first_punch.status == "4":
                    horaire.status = "card"
                
                if last_punch.status == "1":
                    horaire.statute = "fingerprint"
                elif last_punch.status == "3":
                    horaire.statute = "pass word"
                elif last_punch.status == "4":
                    horaire.statute = "card"
                
                horaire.save()

    # Renvoyer tous les horaires pour affichage
    return redirect("profil:attendance")

@login_required(login_url="/account/login_admin/")
def get_somme_for_poste(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'somme': poste.salary})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="/account/login_admin/")
def get_start(request):
  if request.method == 'GET' and 'poste_id' in request.GET:
    poste_id = request.GET.get('poste_id')
    try:
      poste = Poste.objects.get(pk=poste_id)
      return JsonResponse({'start': poste.start_time})
    except Poste.DoesNotExist:
      return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
  else:
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required(login_url="/account/login_admin/")    
def get_end(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'end': poste.end_time})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="/account/login_admin/")    
def get_time_work(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'time_work': poste.time_work})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required(login_url="/account/login_admin/")    
def get_tolerance_time(request):
    if request.method == 'GET' and 'poste_id' in request.GET:
        poste_id = request.GET.get('poste_id')
        try:
            poste = Poste.objects.get(pk=poste_id)
            return JsonResponse({'tolerance_time': poste.tolerance_time})
        except Poste.DoesNotExist:
            return JsonResponse({'error': 'Le poste spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


# from django.shortcuts import render
# from .models import Employe, Attendance
# from datetime import date, timedelta

# def calculer_salaire(request):
#     # Récupérer la date actuelle
#     date_actuelle = date.today()

#     # Récupérer tous les employés
#     employes = Employe.objects.all()

#     # Parcourir tous les employés
#     for employe in employes:
#         # Récupérer toutes les présences de l'employé pour le mois en cours
#         presences = employe.attendance_set.filter(date__year=date_actuelle.year, date__month=date_actuelle.month)

#         # Calculer le total des heures de travail pour le mois
#         total_heures_travail = timedelta()

#         for presence in presences:
#             duree_travail = presence.heure_sortie - presence.heure_entree
#             total_heures_travail += duree_travail

#         # Calculer le salaire de l'employé en fonction du total des heures de travail
#         salaire = total_heures_travail.total_seconds() / 3600 * employe.taux_horaire

#         # ...
#         # Suite du code pour enregistrer le salaire dans la table "Salaire" (comme expliqué dans la réponse précédente)

#     return render(request, 'salaire.html')


# def calculer_heures_travail_journalieres(personnel, date_mois):
#     # Récupérer toutes les présences de l'employé pour le mois spécifié
#     horaires = Horaire.objects.filter(personnel=personnel, date_check__startswith=date_mois)
    
#     total_heures_travail = timedelta()  # Initialiser la durée totale à zéro
    
#     for horaire in horaires:
#         duree = timedelta(hours=horaire.calculate_duration().hour, minutes=horaire.calculate_duration().minute, seconds=horaire.calculate_duration().second)
#         total_heures_travail += duree
    
#     return total_heures_travail

# def calculer_salaire_journalier(personnel, date_mois):
#     total_heures_travail = calculer_heures_travail_journalieres(personnel, date_mois)
#     salaire_journalier = (total_heures_travail.total_seconds() / 3600 * personnel.salary) / personnel.time_works

#     return salaire_journalier

# def calculer_et_afficher_salaire(request):
#     mois_actuel = timezone.now().strftime("%Y-%m")
#     personnels = Personnel.objects.all()
#     infos_salaire = []
    
#     for personnel in personnels:
#         salaire_journalier = calculer_salaire_journalier(personnel, mois_actuel)
#         total_heures_mensuelles = calculer_heures_travail_journalieres(personnel, mois_actuel)
#         salaire_mensuel = (total_heures_mensuelles.total_seconds() / 3600 * personnel.salary) / personnel.time_works

#         # Enregistrer le salaire mensuel à la fin du mois
#         if timezone.now().day == timezone.now().days_in_month:
#             personnel.salaire_mensuel = salaire_mensuel
#             personnel.save()

#         infos_salaire.append({
#             'personnel': personnel,
#             'salaire_journalier': salaire_journalier,
#             'salaire_mensuel': salaire_mensuel,
#         })

#     return render(request, 'infos_salaire.html', {'infos_salaire': infos_salaire})



def get_all_log_data(request):
    lecteurs = Zklecteur.objects.all()  # Récupérer tous les lecteurs
    for lecteur in lecteurs:
        zk = ZK(lecteur.ip_adresse, lecteur.n_port, timeout=2)
        try:
            conn = zk.connect()
            print(f'Disabling device {lecteur.ip_adresse} ...')
            conn.disable_device()
            print(f'--- Get Attendance from {lecteur.ip_adresse} ---')
            attendance = conn.get_attendance()
            print(type(attendance))
            print(attendance)

            for user in attendance:
                id_attendance = user.uid
                check_heure = user.timestamp
                status_a = user.status
                user_id = user.user_id
                punch_attendance = user.punch
                try:
                    existing_attendance = Attendance.objects.filter(id_att=id_attendance).first()
                    if existing_attendance:
                        # Check if the model of the device matches
                        if existing_attendance.lecteur.model_drive == lecteur.model_drive:
                            print("Matching model, passing.")
                            continue
                        else:
                            user_id_zk = User.objects.get(username=user_id)
                            pk_user = user_id_zk.pk
                            user_c = Personnel.objects.get(user=pk_user)
                            # Si le Personnel existe, crée une nouvelle instance du modèle Attendance
                            django_user = Attendance.objects.create(
                                id_att=id_attendance, 
                                personnel_a=user_c, 
                                date=check_heure.date(), 
                                status=status_a, 
                                punch=punch_attendance, 
                                heure_punch=check_heure, 
                                lecteur=lecteur.pk
                            )
                            django_user.save()
                    else:
                        user_id_zk = User.objects.get(username=user_id)
                        pk_user = user_id_zk.pk
                        user_c = Personnel.objects.get(user=pk_user)
                        # Si le Personnel existe, crée une nouvelle instance du modèle Attendance
                        django_user = Attendance.objects.create(
                            id_att=id_attendance, 
                            personnel_a=user_c, 
                            date=check_heure.date(), 
                            status=status_a, 
                            punch=punch_attendance, 
                            heure_punch=check_heure, 
                            lecteur=lecteur.pk
                        )
                        django_user.save()
                except Exception as e:
                    print(f"Error processing attendance for user ----------------------{user_id}: {str(e)}")
            conn.enable_device()
            if conn is not None and conn.is_connect:
                conn.disconnect()
        except Exception as e:
            print(f"Connection error with lecteur ++++++++++++++++++++++++++++++++++++++ {lecteur.ip_adresse}: {str(e)}")
            conn.enable_device()
        finally:
            if conn is not None and conn.is_connect:
                conn.disconnect()
    return render(request,'profil/get_all_log_data')

