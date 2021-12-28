from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import os
        from dotenv import load_dotenv
        from HyperAnnales.settings import env_path
        from accounts.models import Account

        load_dotenv(dotenv_path=env_path)
        if not len(Account.object.filter(is_superuser=True)):
            root = Account(username=os.getenv("DJANGO_LOGIN"),
                           email=os.getenv("DJANGO_EMAIL"),
                           is_active=True,
                           is_superuser=True,
                           is_contributor=True,
                           is_staff=True,
                           is_admin=True)
            root.set_password(os.getenv("DJANGO_PASS"))
            root.save()
            esiee = Account(username="esiee",
                            email="remi.maubanc@etu.unilasalle.fr",
                            is_active=True,
                            is_admin=True,
                            is_contributor=True)
            esiee.set_password(os.getenv("DJANGO_PASS"))
            esiee.save()
