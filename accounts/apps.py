from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import os
        from dotenv import load_dotenv
        from HyperAnnales.settings import env_path
        from accounts.models import Account

        load_dotenv(dotenv_path=env_path)
        if not len(Account.objects.filter(is_superuser=True)):
            Account(username=os.getenv("USER_LOGIN"),
                    password=os.getenv("USER_PASS"),
                    email=os.getenv("USER_EMAIL"),
                    is_active=True,
                    is_superuser=True,
                    is_contributor=True,
                    is_staff=True,
                    is_admin=True).save()
