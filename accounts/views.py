from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from HyperAnnales.settings import EMAIL_HOST_USER
from accounts.forms import AccountAuthenticationForm
from accounts.models import *
from accounts.tokens import account_activation_token


def __test_email(email):
    host = email.split('@')
    return host[1] == "epita.fr"


def __send_verification_email(request, user, email):
    mail_subject = "Activation du compte HyperAnnales"
    current_site = get_current_site(request)
    mail_message = render_to_string('accounts/mail_template.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user=user),
        }
    )
    send_mail(mail_subject, mail_message, EMAIL_HOST_USER, [email], fail_silently=False)

    log_message = render_to_string('accounts/mail_template_log.html',
        {
            'mail': mail_message,
            'timestamp': datetime.now().strftime("%d-%m-%Y_%H:%M:%S"),
            'email': email,
            'subject': mail_subject,
        }
    )
    send_mail(mail_subject + "_log", log_message, "log@hyperion.tf", [EMAIL_HOST_USER], fail_silently=True)


def registration_view(request):
    context = {}
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print("user = " + username + " email = " + email + " pass = " + password1)
        if password1 != password2:
            context['error'] = "Les mots de passe ne correspondent pas"
        elif len(username) == 0 or len(email) == 0 or len(password1) == 0:
            context['error'] = "Veuillez remplir tous les champs"
        else:
            mail = Account.object.filter(email__exact=email)
            user = Account.object.filter(username__exact=username)
            error = False
            if len(user):
                error = True
                context['error'] = "Le pseudo a déjà été utilisé"
            if len(mail):
                if error:
                    context['error'] = "Le pseudo et le mail ont déjà été utilisés"
                else:
                    context['error'] = "L'email a déjà été utilisé"
                    error = True

            if not __test_email(email):
                context['error'] = "L'email n'est pas valide, entrez une adresse epita"
                error = True

            if not error:
                user = Account.object.create_user(email, username, password1)
                __send_verification_email(request, user, email)
                context['mail'] = "Un email de validation vient d'être expedié pour confirmer votre compte."
                return render(request, 'index.html', context)
    return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.object.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        context = {'mail': "Votre compte a été validé avec succès !"}
        return render(request, 'index.html', context)
    else:
        context = {'mail': "Echec de la validation du compte, veuillez contactez un administrateur."}
        return render(request, 'index.html', context)


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
