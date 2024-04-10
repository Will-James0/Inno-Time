from django.shortcuts import render, get_list_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Personnel,Horaire,Poste,Attendance
from .forms import Part1Form, Part2Form,Part3Form
from datetime import datetime, timedelta, timezone,date
from django.core.paginator import Paginator
from django.db.models import Count



@login_required(login_url="account/login_admin")
def acceuil(request):
    
    date_j = date.today()
    attendance_dates = Horaire.objects.values_list('date_d', flat=True).distinct()
    # Séparer les dates et les nombres d'employés en deux listes distinctes
    dates_list = []
    counts_list = []
    # i=30
    # day_nbr = date.today().strftime("%d")
    # while i == 30:
    for entry in  attendance_dates:
            dates_list.append(str(entry.strftime("%d-%m-%Y")))
            present = Horaire.objects.filter(date_d=entry).count()
            counts_list.append(int(present))

    # i +=1
    total_employees = Personnel.objects.count()
    
    # Compter le nombre d'employés présents à la date donnée
    employees_present = Horaire.objects.filter(date_d=date_j).count()
    # Calculer le nombre d'employés absents
    employees_absent = total_employees - employees_present

    context={
         'total_employees':total_employees,
         'p':employees_present,
         'a':employees_absent,
        #  'dates': date_month_list, 
        'dates':dates_list,
        #  'nbre_present': present_p,
        'nbrepresent':counts_list,
      
         }



    return render(request,"profil/acceuil.html",context)


def index(request):
   
    return render(request,"profil/index.html")

# Poste
@login_required(login_url="account/login_admin")
def part1(request):
   if request.method == 'POST':
       form = Part1Form(request.POST)
       if form.is_valid():
           form.save()
     
           return redirect('profil:poste')
   else:
       form = Part1Form()
   return render(request, 'profil/part1.html', {'form': form})

# Personnel
@login_required(login_url="account/login_admin")
def part2(request):
   if request.method == 'POST':
       form = Part2Form(request.POST)
       if form.is_valid():
           form.save()
        #    request.session['field2'] = form.cleaned_data['field2']
        #    request.session['field3'] = form.cleaned_data['field3']
           # Enregistrez les données dans la base de données ou effectuez toute autre action requise
           return redirect('profil:liste_e')
   else:
       form = Part2Form()
   return render(request, 'profil/part2.html', {'form': form})

# Horaire
@login_required(login_url="account/login_admin")
def part3(request):
   if request.method == 'POST':
       form = Part3Form(request.POST)
       if form.is_valid():
           form.save()
           #request.session['field1'] = form.cleaned_data['field1']
           return redirect("profil:attendance")
   else:
       form = Part3Form()
   return render(request, 'profil/part3.html', {'form': form})



@login_required(login_url="account/login_admin")
def liste_e(request):

    #personnel = Personnel.objects.all()  # Récupérer la liste complète des employés depuis la base de données
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
    return render(request,"profil/liste_e.html",context)



@login_required(login_url="account/login_admin")
def attendance(request):
    context={'postes':Poste.objects.all(),
           'horaires':Horaire.objects.all(),
           'personnels':Personnel.objects.all(),
           'attendances':Attendance.objects.all(),
      
           }
    return render(request,"profil/attendance.html",context)

@login_required(login_url="account/login_admin")
def historique(request):
    return render(request,"profil/historique.html")

@login_required(login_url="account/login_admin")
def profil_e(request,Personnel_id): 
    context = {"Personnels": get_list_or_404(Personnel,pk=Personnel_id),
               
            }
    return render(request, "profil/profil_e.html", context)





def labels_date(date_planing):
    horaires = Horaire.objects.filter(date_d=date_planing)
    lab_date=[]
    for horaire in horaires:
        lab_date.append(horaire)

    return lab_date



@login_required(login_url="account/login_admin")
def help(request):

    
    return render(request,"Profil/help.html")

@login_required(login_url="account/login_admin")
def del_user(request,Personnel_id):
    Personne = Personnel.objects.get(pk=Personnel_id)
    Personne.delete()
    return redirect("profil:liste_e")

@login_required(login_url="account/login_admin")
def del_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:poste")




def delete_employees(request):
    if request.method == 'POST':
        selected_employees = request.POST.getlist('selected_employees')
        # Code pour supprimer les employés sélectionnés
        # selected_employees contient une liste des ID des employés sélectionnés
        Personnel.objects.filter(id__in=selected_employees).delete()
        
    
    return redirect('profil:liste_e')












# 
@login_required(login_url="account/login_admin")
def del_poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    poste.delete()
    return redirect("profil:poste")




@login_required(login_url="account/login_admin")
def edit_Poste(request,Poste_id):
    poste = Poste.objects.get(pk=Poste_id)
    if request.method == 'POST':
        form = Part1Form(request.POST,instance=poste)
        if form.is_valid():
            form.save()
            return redirect("profil:poste")
    else:
        form = Part1Form(instance=poste)
    
    return render(request,"profil/partm1.html",{"form": form})

@login_required(login_url="account/login_admin")
def edit_Personnel(request,Personnel_id):
    Personnels = Personnel.objects.get(pk=Personnel_id)
    if request.method == 'POST':
        form = Part2Form(request.POST,instance=Personnels)
        if form.is_valid():
            form.save()
            return redirect("profil:liste_e")
    else:
        form = Part2Form(instance=Personnels)
    
    return render(request,"profil/part2.html",{"form": form})

@login_required(login_url="account/login_admin")
def edit_Horaire(request,Horaire_id):
    Personnels = Personnel.objects.get(pk=Horaire_id)
    if request.method == 'POST':
        form = Part3Form(request.POST,instance=Personnels)
        if form.is_valid():
            form.save()
            return redirect("profil:attendance")
    else:
        form = Part3Form(instance=Personnels)
   
    return render(request,"profil/part3.html",{"form": form})




def calculate_daily_work_hours(personnel):
    # Récupérer toutes les présences de l'employé pour la journée spécifiée
    horaires = Horaire.objects.filter(personnel=personnel)
    total_work_hours = timedelta()
    for horaire in horaires:
        total_work_hours += horaire.calculate_duration()

    return total_work_hours

def calculate_daily_salary(personnel):
    total_work_hours = calculate_daily_work_hours(personnel)
    daily_salary = total_work_hours.total_seconds() / 3600 * (personnel.poste.somme+personnel.salary)
    daily_salary = total_work_hours.total_seconds() / 3600 * (personnel.poste.somme+personnel.salary)
    daily_salary = (total_work_hours.total_seconds() / 3600 * (personnel.poste.somme + personnel.salary))/personnel.heure_fixe #n

    return daily_salary

@login_required(login_url="account/login_admin")
def personnel_salary(request, Personnel_id):
    personnel = Personnel.objects.get(id=Personnel_id)
    daily_work_hours = calculate_daily_work_hours(personnel)
    daily_salary = calculate_daily_salary(personnel)

    context = {
        'personnel': personnel,
        'daily_work_hours': daily_work_hours,
        'daily_salary': daily_salary,
    }

    return render(request, 'profil/salaire.html', context)

@login_required(login_url="account/login_admin")
def fiche(request,personnel_id):
    personnel = Personnel.objects.get(id=personnel_id)
  
    daily_work_hours = calculate_daily_work_hours(personnel)
    daily_salary = calculate_daily_salary(personnel)

    context = {
        'personnel': personnel,
        'daily_work_hours': daily_work_hours,
        'daily_salary': daily_salary,
    }

    return render(request, 'profil/salary.html', context)


@login_required(login_url="account/login_admin")
def post(request):
    context={'postes':Poste.objects.all(),}
    return render(request, "profil/post.html",context)
