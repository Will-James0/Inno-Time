from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




# Create your views here.

def login_admin(request):
    if request.method =='POST':
        username_u = request.POST["username"]
        password_u = request.POST["password"]

        user = authenticate(request, username = username_u, password= password_u)

        if user is not None:
            login(request, user)
            return redirect("userprofil:acceuil")
        else:
            messages.info(request, "Identifiant ou le mot de passe incorrect")
    form = AuthenticationForm()
    return render(request,"useraccounts/login_a.html", {"form":form})


def logout_user(request):
    logout(request)
    return redirect("userprofil:index")


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("userprofil:acceuil")
    else:
        form = UserCreationForm()
        
    return render(request, "useraccounts/register.html",{"form":form})

