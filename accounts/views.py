from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from accounts.forms import RegistrationForm, AccountAuthenticationForm
from accounts.models import *


def registration_view(request):
    context = {}
    if request.POST:
        try:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            print("user = " + username + " email = " + email + " pass = " + password1)
            if password1 != password2:
                context['error'] = "Les mots de passe ne correspondent pas"
            elif len(username) == 0 or not len(email) or not len(password1) or not len(password2):
                print("here1")
                context['error'] = "Veuillez remplir tous les champs"
            else:
                print("here2")
                u = Account.object.create_user(email, username, password1)
                print("here3")
                login(request, u)
                print("here4")
                context['error'] = None
                return redirect("home")
        except:
            context['error'] = "Une erreur s'est produite. Veuillez réessayer"
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("index")

    context = {}
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("index")

        context['error'] = 'Nom d\'utilisateur et/ou mot de passe invalide'
        context['login_form'] = form
    return render(request, "accounts/login.html", context)
