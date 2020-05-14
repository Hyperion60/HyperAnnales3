from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from accounts.forms import RegistrationForm, AccountAuthenticationForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect("index")
        else:
            context['error'] = "Echec de la création du compte. Veuillez réessayer."
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
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
