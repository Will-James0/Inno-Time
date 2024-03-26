import django
from django.shortcuts import render, get_list_or_404,redirect
from django.contrib.auth.decorators import login_required

from .models import Personnel
from .forms import ProfilForm


# Create your views here.
def index(request):
    context = {"nom":Personnel.objects.all()}
    return render(request,"userprofile/index.html",context)

@login_required
def liste_e(request):
    context = {"nom":Personnel.objects.all()}
    return render(request,"userprofile/liste_e.html",context)

@login_required
def acceuil(request):
    
    return render(request,"userprofile/acceuil.html")
@login_required
def attendance(request):
    return render(request,"userprofile/attendance.html")

@login_required
def edit_Personnel(request,Personnel_id):
    Personnels = Personnel.objects.get(pk=Personnel_id)
    if request.method == 'POST':
        form = ProfilForm(request.POST,instance=Personnels)
        if form.is_valid():
            form.save()
            return redirect("profil:liste_e")
    else:
        form = ProfilForm(instance=Personnels)
    return render(request,"userprofile/mod_e.html",{"form": form})

@login_required
def historique(request):
    return render(request,"userprofile/historique.html")

@login_required
def help(request):
    return render(request,"userprofile/help.html")

@login_required
def add_Profil(request):
   
    if request.method == 'POST':
        form = ProfilForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profil:liste_e")
    else:
        form = ProfilForm()
    context = {"form": form}
    return render(request,"userprofile/form.html",context)

@login_required
def profil_e(request,Personnel_id): 
    context = {"Personnel": get_list_or_404(Personnel,pk=Personnel_id),
               
            }
    return render(request, "userprofile/profil_e.html", context)

@login_required
def del_user(request,Personnel_id):
    Personne = Personnel.objects.get(pk=Personnel_id)
    Personne.delete()
    return redirect("profil:liste_e")



