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
    send_mail(mail_subject + "_log", log_message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=True)


def __send_mail_reset_password(request, user):
    mail_subject = "Réinitialisation du mot de passe - HyperAnnales"
    current_site = get_current_site(request)
    mail_message = render_to_string('accounts/mail_reset_pass.html',
        {
             'user': user[0].username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token': account_activation_token.make_token(user=user[0]),
        }
    )
    send_mail(mail_subject, mail_message, EMAIL_HOST_USER, [user[0].email], fail_silently=False)

    log_message = render_to_string('accounts/mail_template_log.html',
        {
            'mail': mail_message,
            'timestamp': datetime.now().strftime("%d-%m-%Y_%H:%M:%S"),
            'email': user[0].email,
            'subject': mail_subject,
        }
    )
    send_mail(mail_subject + "_log", log_message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=True)


def registration_view(request):
    context = {}
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
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
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        context = {'mail': "Votre compte a été validé avec succès !"}
    else:
        if user.is_active:
            context = {'error': "Le lien a déjà été utilisé. Le compte est actif."}
        else:
            context = {'error': "Echec de la validation du compte, veuillez contactez un administrateur."}
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

            print(username)
            usermail = Account.object.filter(email__exact=username)
            print(usermail)
            if len(usermail):
                print("here")
                user = authenticate(username=usermail.username, password=password)
                login(request, user)
                return redirect("index")

        context['error'] = 'Nom d\'utilisateur et/ou mot de passe invalide'
        context['login_form'] = form
    return render(request, "accounts/login.html", context)


def reset_password(request):
    context = {}
    if request.POST:
        email = request.POST['email']
        check = Account.object.filter(email__exact=email)
        if not len(check):
            context['error'] = "L'email n'est relié à aucun compte existant"
        else:
            context['message'] = "Un e-mail vient de vous être envoyé pour vous permettre de modifier votre mot de" \
                                 " passe"
            __send_mail_reset_password(request, check)
            return render(request, 'accounts/message_template.html', context)
    return render(request, 'accounts/reset_password.html', context)


def change_password(request, uidb64, token):
    context = {}
    if request.POST:
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            context['error'] = "Les mots de passe sont différents"
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.object.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
            context['error'] = "Le lien n'est pas valide"
        if user is not None and account_activation_token.check_token(user, token):
            user.set_password(password1)
            user.save(using='default')
            context['message'] = "Votre mot de passe a bien été modifié."
            return render(request, 'accounts/message_template.html', context)
    context['uidb64'] = uidb64
    context['token'] = token
    return render(request, 'accounts/change_password.html', context)
